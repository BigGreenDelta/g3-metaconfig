from typing import Union, Any, Optional, Callable, Tuple, List, Generator

import configargparse
from pydantic import BaseModel, Extra, Field


class Param(BaseModel, extra=Extra.allow):
    args: List[Any] = None
    action: str = None
    nargs: Union[int, str] = None
    const: str = None
    default: Any = None
    type: Optional[Callable[[], Any]] = None
    choices: list = None
    required: bool = None
    help: str = None
    metavar: Union[str, Tuple[str]] = None
    dest: str = None
    env_var: str = None

    _name = Field()

    def __init__(
            self,
            *args,
            name: str = None,
            action: str = None,
            nargs: Union[int, str] = None,
            const: str = None,
            default: Any = None,
            type: Optional[Callable[[], Any]] = None,
            choices: list = None,
            required: bool = None,
            help: str = None,
            metavar: Union[str, Tuple[str]] = None,
            dest: str = None,
            env_var: str = None,
            **kwargs, ):
        ...

    def _iter(self, *args, **kwargs) -> Generator[Tuple[str, Any], None, None]:
        ...

    def set_name(self, param_name: str):
        ...

    def set_dest(self):
        ...

    def set_args(self, auto_replace_underscores_with_dashes: bool):
        ...

    def set_env(self, env_prefix: Optional[str] = None):
        ...

    def set_type(self, auto_typing: bool, annotation: Any, parser: Union[configargparse.ArgParser, Any]):
        ...
