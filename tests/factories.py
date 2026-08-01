"""Factories for building click commands and groups in tests."""

import click


def make_command(*params, **command_kwargs):
    """Build a click Command from option/argument specs."""
    return click.Command("cli", params=list(params), **command_kwargs)


def make_group(*subcommands, **group_kwargs):
    """Build a click Group from subcommand names."""
    group = click.Group("cli", **group_kwargs)
    for name in subcommands:
        group.add_command(click.Command(name))
    return group
