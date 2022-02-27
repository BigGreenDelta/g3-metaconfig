from typing import Any, Callable, Optional, List, Union, Tuple

from pydantic import BaseModel, Extra


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

    def __init__(
            self,
            *args,
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
            **kwargs,
    ):
        super().__init__(
            action=action,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar,
            dest=dest,
            env_var=env_var,
            **kwargs,
        )
        self.args = list(args)
