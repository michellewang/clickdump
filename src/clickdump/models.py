"""Data models for click CLI serialization."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ActionType(str, Enum):
    """Click action types (mirrors argdump.ActionType for schema compat)."""

    STORE = "store"
    STORE_CONST = "store_const"
    STORE_TRUE = "store_true"
    STORE_FALSE = "store_false"
    APPEND = "append"
    APPEND_CONST = "append_const"
    COUNT = "count"
    HELP = "help"
    VERSION = "version"
    PARSERS = "parsers"
    EXTEND = "extend"
    BOOLEAN_OPTIONAL = "boolean_optional"
    UNKNOWN = "unknown"

    @classmethod
    def from_string(cls, value: str) -> ActionType:
        try:
            return cls(value)
        except ValueError:
            return cls.UNKNOWN


@dataclass
class TypeInfo:
    """Type converter information."""

    name: str
    module: str | None = None
    builtin: bool = False
    serializable: bool = True


@dataclass
class FileTypeInfo:
    """File type parameters (like argparse.FileType / click.File)."""

    mode: str = "r"
    bufsize: int = -1
    encoding: str | None = None
    errors: str | None = None


@dataclass
class ActionInfo:
    """Serialized Click Parameter (Option or Argument)."""

    option_strings: list[str]
    dest: str
    action_type: ActionType
    nargs: str | int | None = None
    const: Any = None
    default: Any = None
    type_info: TypeInfo | None = None
    file_type_info: FileTypeInfo | None = None
    choices: list[Any] | None = None
    required: bool = False
    help: str | None = None
    metavar: str | tuple[str, ...] | None = None
    deprecated: bool = False
    version: str | None = None
    subparsers: dict[str, ParserInfo] | None = None
    subparsers_title: str | None = None
    subparsers_description: str | None = None
    subparsers_dest: str | None = None
    subparsers_required: bool = False
    subparsers_aliases: dict[str, list[str]] | None = None
    custom_action_class: str | None = None

    # Click-specific extensions
    hidden: bool = False
    show_default: bool | str | None = None
    show_envvar: bool = False
    prompt: bool | str | None = None
    envvar: str | list[str] | None = None
    is_eager: bool = False
    expose_value: bool = True
    count: bool = False
    is_flag: bool = False
    flag_value: Any = None
    multiple: bool = False

    @property
    def is_optional(self) -> bool:
        return bool(self.option_strings)

    @property
    def is_positional(self) -> bool:
        return not self.option_strings


@dataclass
class MutualExclusionGroup:
    """Mutually exclusive argument group."""

    required: bool
    actions: list[str]


@dataclass
class ArgumentGroup:
    """Argument group for help organization."""

    title: str | None
    description: str | None
    actions: list[str]


@dataclass
class ParserInfo:
    """Complete serialized Click Command or Group."""

    prog: str | None = None
    description: str | None = None
    epilog: str | None = None
    usage: str | None = None
    add_help: bool = True
    allow_abbrev: bool = True
    formatter_class: str | None = None
    prefix_chars: str = "-"
    fromfile_prefix_chars: str | None = None
    argument_default: Any = None
    conflict_handler: str = "error"
    exit_on_error: bool = True
    suggest_on_error: bool = False
    color: bool = True

    actions: list[ActionInfo] = field(default_factory=list)
    argument_groups: list[ArgumentGroup] = field(default_factory=list)
    mutually_exclusive_groups: list[MutualExclusionGroup] = field(default_factory=list)

    # Click-specific extensions
    short_help: str | None = None
    hidden: bool = False
    deprecated: bool = False
    no_args_is_help: bool = False
    invoke_without_command: bool = False
    chain: bool = False
    subcommand_metavar: str | None = None
    allow_extra_args: bool = False
    allow_interspersed_args: bool = True
    ignore_unknown_options: bool = False

    def get_action_by_dest(self, dest: str) -> ActionInfo | None:
        for action in self.actions:
            if action.dest == dest:
                return action
        return None
