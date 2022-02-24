from typing import Optional, Type

import configargparse
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.forbid):
    """ Config class for G3ConfigMeta metaclass."""

    auto_typing: bool = True
    """ Automatically determine `type` parameter for 'SIMPLE_TYPES' from type hints if not set explicitly in `Param`."""

    env_prefix: Optional[str] = None
    """ Specify it to automatically enable getting of all your class variables from environment variables.
    This prefix is used only if you didn't specify `env_var` parameter in `Param`."""

    auto_replace_underscores_with_dashes: bool = True
    """ Automatically replace underscores with dashes in CLI argument names."""


class ArgParserConfig(BaseModel, extra=Extra.allow):
    """ ArgParserConfig class that directly process almost all it's fields
    to parser_class's ArgParser arguments at its creation."""

    add_help: Optional[bool] = None
    description: Optional[str] = None

    __service_args_ArgParserConfig__ = {"parse_known_args", "argument_parser_class"}
    argument_parser_class: Optional[Type] = configargparse.ArgParser
    """ Class to use while creating argument parser."""
    parse_known_args: bool = True
    """ Used to specify parse function.
    True: parse_known_args
    False: parse_args"""
