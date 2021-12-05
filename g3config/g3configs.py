from abc import ABCMeta
from typing import Any, Dict, Type, Set, Callable, Optional, List

import configargparse as configargparse
from pydantic import BaseModel, Extra

__ALL__ = ["G3ConfigMetaclass", "Param", "Config", "ParserConfig"]


class Param(BaseModel, extra=Extra.allow):
    args: List[Any] = None
    default: Any = None
    dest: str = None
    help: str = None
    required: bool = None
    type: Optional[Callable[[], Any]] = None
    env_var: str = None
    title: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.args = list(args)


class Config(BaseModel, extra=Extra.forbid):
    env_prefix: str = None


class ParserConfig(BaseModel, extra=Extra.allow):
    add_help: bool = None
    description: str = None


class ClassData(BaseModel, arbitrary_types_allowed=True):
    config: Optional[Config] = None

    actual_class: Type = None
    name: str = None
    bases: Set[Type] = list()
    annotations: Dict[str, Type] = dict()
    fields_values: Dict[str, Any] = dict()
    kwargs: Dict[str, Any] = None

    instance: Any = None

    parser: configargparse.ArgParser = None
    parser_config: Optional[ParserConfig] = None


class G3ConfigMetaclass(ABCMeta):
    _classes: Dict[Type, ClassData] = {}

    def __call__(cls, *args, **kwargs):
        return cls._classes[cls].instance

    def __new__(mcs, name, bases, namespace, **kwargs):
        print(f"__new__: {name=}")
        print(f"__new__: {bases=}")
        print(f"__new__: {namespace=}")
        print(f"__new__: {kwargs=}")

        cls = type.__new__(mcs, name, bases, dict(namespace))

        if cls in cls._classes:
            raise KeyError

        class_data = mcs._prepare_class_data(cls, name, bases, namespace, **kwargs)
        mcs._parse_fields(class_data)
        mcs._parse_args(class_data)

        print(f"__new__: created inst => {class_data.json(encoder=str, indent=4)}")

        return cls

    @staticmethod
    def _prepare_class_data(cls, name: str, bases: Set[Type], namespace: Dict[str, Any], **kwargs) -> ClassData:
        cls._classes[cls] = ClassData(
            config=cls._get_config_inst(Config, namespace),
            actual_class=cls,
            instance=super(G3ConfigMetaclass, cls).__call__(),
            name=name,
            bases=bases,
            annotations=namespace.get("__annotations__", []),
            fields_values=cls._get_class_fields(cls, [Config.__name__, ParserConfig.__name__]),
            kwargs=kwargs,
            parser_config=cls._get_config_inst(ParserConfig, namespace))

        return cls._classes[cls]

    @staticmethod
    def _parse_fields(data: ClassData):
        for name, value in data.fields_values.items():
            if not isinstance(value, Param):
                continue

            print(f"_parse_fields: FieldData found! {value=}")

    @staticmethod
    def _parse_args(data: ClassData):
        parser_configs = data.parser_config.dict(exclude_none=True) if data.parser_config else dict()
        data.parser = configargparse.ArgParser(**parser_configs)

        for name, value in data.fields_values.items():
            param: Param
            if isinstance(value, Param):
                param = value
            else:
                param = Param()
                if value is not None:
                    param.default = value
                # TODO: make init

            if not param.dest:
                param.dest = name
            if not param.args:
                param.args = [f"--{name.lower()}"]

            data.parser.add_argument(*param.args, **param.dict(exclude={"args"}, exclude_unset=True))

        args, other = data.parser.parse_known_args()
        args: configargparse.Namespace
        for name, value in args.__dict__.items():
            print(f"{name} = {value}")
            setattr(data.actual_class, name, value)

    @staticmethod
    def _get_config_inst(parent_config: Type[BaseModel], namespace: Dict[str, Any]) -> object:
        cls = namespace.get(parent_config.__name__, None)
        cls_fields = G3ConfigMetaclass._get_class_fields(cls)
        return parent_config.parse_obj(cls_fields)

    @staticmethod
    def _get_class_fields(cls: Type, excluding: Optional[List[str]] = None) -> dict:
        field_values: dict = dict()
        for k, v in cls.__dict__.items():
            if any([k.startswith("__"), k.endswith("__")]):
                continue
            if excluding and k in excluding:
                continue
            field_values[k] = v
        return field_values


class G3Configs(metaclass=G3ConfigMetaclass):
    class Config:
        env_prefix = "G3_"

    class ParserConfig:
        default_config_files = ["config.yml"]
        description = "Test"

    count: int = Param("--count", help="Help yuorself", default=33)
    condition: bool = Param("-c", "--cond", env_var="TEST_COND")
    text: str = None
    array: list = ["asdsssssss"]


configs0 = G3Configs()
configs1 = G3Configs()
configs2 = G3Configs()
configs3 = G3Configs()

print(f"{configs3.count=}")
print(f"{configs3.condition=}")
print(f"{configs3.text=}")
print(f"{configs3.array=}")
