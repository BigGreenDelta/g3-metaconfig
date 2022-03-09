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

    def __init__(self, *args, **kwargs, ):
        super().__init__(**kwargs, )
        self.args = list(args)
