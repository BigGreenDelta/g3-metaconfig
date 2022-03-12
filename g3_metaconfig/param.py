import logging
from typing import Any, Callable, Optional, List, Union, Tuple, Generator

import configargparse
from pydantic import BaseModel, Extra

log = logging.getLogger("g3-param")


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

    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)

        super().__init__(**kwargs, )
        self.args = list(args)

        self._name = name

    def _iter(self, *args, **kwargs) -> Generator[Tuple[str, Any], None, None]:
        exclude: set = kwargs.get("exclude", None) or set()
        exclude.add("_name")
        return super()._iter(*args, **kwargs)

    def set_name(self, param_name: str):
        self._name = param_name

    def set_dest(self):
        if not self.dest:
            self.dest = self._name

    def set_args(self, auto_replace_underscores_with_dashes: bool):
        if not self.args:
            cli_name = self._name.lower()
            if auto_replace_underscores_with_dashes:
                cli_name = cli_name.replace('_', '-')
            self.args = [f"--{cli_name}"]

    def set_env(self, env_prefix: Optional[str] = None):
        if all([env_prefix is not None, self.env_var is None, ]):
            self.env_var = f"{env_prefix}{self._name}".upper()

    def set_type(self, auto_typing: bool, annotation: Optional[Any], parser: Union[configargparse.ArgParser, Any]):
        # Checking auto_typing compatibility with selected action
        if auto_typing and self.action is not None:
            try:
                action_class = parser._registry_get("action", self.action, self.action)
                action_class(
                    option_strings=self.args,
                    type="test",
                    **self.dict(exclude={"args", "action"}, exclude_unset=True),
                )
            except TypeError as e:
                auto_typing = False
                log.warning(
                    f"Param '{self._name}' has action={self.action} "
                    f"which leads to disabling Config.auto_typing for this variable"
                )

        if all([auto_typing, self.type is None, annotation is not None]):
            if isinstance(annotation, type):
                self.type = annotation
