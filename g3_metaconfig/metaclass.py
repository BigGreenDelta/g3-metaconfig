import logging
import sys
from abc import ABCMeta
from typing import Any, Dict, Type, Set, Optional, List, Union

import configargparse as configargparse
from pydantic import BaseModel

from .configs import Config, ArgParserConfig, SIMPLE_TYPES
from .param import Param

__ALL__ = ["G3ConfigMeta"]

log = logging.getLogger("g3-config")


class ClassData(BaseModel, arbitrary_types_allowed=True):
    config: Optional[Config] = None

    actual_class: Type = None
    name: str = None
    bases: Set[Type] = list()
    annotations: Dict[str, Any] = dict()
    fields_values: Dict[str, Any] = dict()
    kwargs: Dict[str, Any] = None

    instance: Any = None

    arg_parser_config: Optional[ArgParserConfig] = None
    parser: Union[configargparse.ArgParser, Any] = None


class G3ConfigMeta(ABCMeta):
    _classes: Dict[Type, ClassData] = {}

    def __call__(cls, *args, **kwargs):
        return cls._classes[cls].instance

    def __new__(mcs, name, bases, namespace, **kwargs) -> type:
        log.debug(f"__new__: {name=}")
        log.debug(f"__new__: {bases=}")
        log.debug(f"__new__: {namespace=}")
        log.debug(f"__new__: {kwargs=}")

        cls = type.__new__(mcs, name, bases, dict(namespace))

        if cls in cls._classes:
            raise KeyError

        class_data = mcs._prepare_class_data(cls, name, bases, namespace, **kwargs)
        mcs._parse_fields(class_data)
        mcs._parse_args(class_data)

        log.debug(f"__new__: created inst => {class_data.json(encoder=str, indent=4)}")

        return cls

    @staticmethod
    def _prepare_class_data(cls, name: str, bases: Set[Type], namespace: Dict[str, Any], **kwargs) -> ClassData:
        cls._classes[cls] = ClassData(
            config=cls._get_config_inst(Config, namespace),
            actual_class=cls,
            instance=super(G3ConfigMeta, cls).__call__(),
            name=name,
            bases=bases,
            annotations=namespace.get("__annotations__", {}),
            fields_values=cls._get_class_fields(cls, [Config.__name__, ArgParserConfig.__name__]),
            kwargs=kwargs,
            arg_parser_config=cls._get_config_inst(ArgParserConfig, namespace),
        )

        return cls._classes[cls]

    @staticmethod
    def _parse_fields(data: ClassData):
        for name, value in data.fields_values.items():
            if not isinstance(value, Param):
                continue

            log.debug(f"_parse_fields: FieldData found! {value=}")

    @staticmethod
    def _parse_args(data: ClassData):
        parser_configs = dict()
        if data.arg_parser_config is not None:
            parser_configs = data.arg_parser_config.dict(
                exclude_none=True,
                exclude=ArgParserConfig.__service_args_ArgParserConfig__,
            )
        data.parser = data.arg_parser_config.argument_parser_class(**parser_configs)

        for name, value in data.fields_values.items():
            param: Param
            if isinstance(value, Param):
                param = value
            else:
                param = Param()
                if value is not None:
                    param.default = value

                    if data.config.auto_typing:
                        param_type = type(value)
                        if param_type in SIMPLE_TYPES:
                            param.type = param_type

            if not param.dest:
                param.dest = name

            if not param.args:
                cli_name = name.lower()
                if data.config.auto_replace_underscores_with_dashes:
                    cli_name = cli_name.replace('_', '-')
                param.args = [f"--{cli_name}"]

            if all([data.config.auto_typing, param.type is None, name in data.annotations]):
                if isinstance(data.annotations[name], type):
                    param.type = data.annotations[name]

            if all([data.config is not None, data.config.env_prefix is not None, param.env_var is None, ]):
                param.env_var = f"{data.config.env_prefix}{name}".upper()

            log.debug(
                f"{name} ({type(value).__name__}): "
                f"{param.args} {param.dict(exclude={'args'}, exclude_unset=True)}"
            )

            data.parser.add_argument(*param.args, **param.dict(exclude={"args"}, exclude_unset=True))

        log.debug(f"{sys.argv=}")

        if data.arg_parser_config.parse_known_args:
            args, other = data.parser.parse_known_args()
            log.debug(f"{args=}")
            log.debug(f"{other=}")
        else:
            args = data.parser.parse_args()
            log.debug(f"{args=}")

        args: configargparse.Namespace
        for name, value in args.__dict__.items():
            log.debug(f"{name} = {value}")
            setattr(data.actual_class, name, value)

    @staticmethod
    def _get_config_inst(parent_config: Type[BaseModel], namespace: Dict[str, Any]) -> object:
        cls = namespace.get(parent_config.__name__, None)
        cls_fields = G3ConfigMeta._get_class_fields(cls) if cls is not None else dict()
        return parent_config.parse_obj(cls_fields)

    @staticmethod
    def _get_class_fields(cls: Type, excluding: Optional[List[str]] = None) -> dict:
        field_values: dict = dict()
        for k, v in cls.__dict__.items():
            if all([k.startswith("__"), k.endswith("__")]):
                continue
            if excluding and k in excluding:
                continue
            field_values[k] = v
        return field_values
