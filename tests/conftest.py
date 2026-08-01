"""Test fixtures for clickdump tests."""

from __future__ import annotations

import json
from pathlib import Path

import click
import pytest
from factories import make_command, make_group

SCHEMA_PATH = Path(__file__).parent / "schema" / "schema-v1.json"


@pytest.fixture
def argdump_schema():
    """Load the argdump JSON schema."""
    return json.loads(SCHEMA_PATH.read_text())


@pytest.fixture
def simple_command():
    """Basic command with positional and optional args."""

    @click.command()
    @click.option("-v", "--verbose", count=True, help="Verbosity level")
    @click.option("--name", default="world", help="Who to greet")
    @click.argument("files", nargs=-1)
    def cli(name, verbose, files):
        """A simple CLI tool."""

    return cli


@pytest.fixture
def command_with_types():
    """Command with various Click types."""

    @click.command()
    @click.option("--count", type=int, default=1)
    @click.option("--pi", type=float)
    @click.option("--flag/--no-flag", default=True)
    @click.option("--switch", is_flag=True)
    @click.option("--color", type=click.Choice(["red", "green", "blue"]))
    @click.option("--path", type=click.Path(exists=True))
    @click.option("--num", type=click.IntRange(0, 100))
    @click.option("--uid", type=click.UUID)
    @click.option("--since", type=click.DateTime())
    @click.option("--ratio", type=click.FloatRange(0.0, 1.0))
    @click.option("--point", type=(float, float))
    @click.argument("input", type=click.File("r"))
    def cli(count, pi, flag, switch, color, path, num, uid, since, ratio, point, input):
        """Command with types."""

    return cli


@pytest.fixture
def command_with_envvar():
    """Command with envvar."""
    return make_command(
        click.Option(["--host"], envvar="HOST", default="localhost"),
        click.Option(["--port"], envvar="PORT", type=int, default=8080),
    )


@pytest.fixture
def command_with_hidden():
    """Command with hidden option."""
    return make_command(
        click.Option(["--visible"], help="I am visible"),
        click.Option(["--hidden"], hidden=True, help="I am hidden"),
    )


@pytest.fixture
def simple_group():
    """Group with subcommands."""

    @click.group()
    @click.option("--debug/--no-debug", default=False)
    def cli(debug):
        """A CLI with subcommands."""

    @cli.command()
    @click.option("--output", "-o", default="out.txt")
    @click.argument("src")
    def build(output, src):
        """Build the project."""

    @cli.command()
    @click.option("--all", is_flag=True)
    def clean(all):
        """Clean the project."""

    return cli


@pytest.fixture
def nested_group():
    """Group with nested subcommands."""

    @click.group()
    def cli():
        """Top-level CLI."""

    @cli.group()
    @click.option("--format", type=click.Choice(["json", "yaml"]))
    def config(format):
        """Configuration commands."""

    @config.command()
    @click.argument("key")
    def get(key):
        """Get a config value."""

    @config.command()
    @click.argument("value")
    def set(value):
        """Set a config value."""

    return cli


@pytest.fixture
def command_no_help():
    """Command with add_help_option=False."""
    return make_command(add_help_option=False)


@pytest.fixture
def deprecated_command():
    """Command with deprecated=True."""
    return make_command(deprecated=True)


@pytest.fixture
def chain_group():
    """Group with chain=True."""
    return make_group("step_a", "step_b", chain=True)


@pytest.fixture
def command_prompt_true():
    """Command with prompt=True."""
    return make_command(click.Option(["--name"], prompt=True))


@pytest.fixture
def command_required():
    """Command with required=True."""
    return make_command(click.Option(["--token"], required=True))


@pytest.fixture
def group_with_hidden_subcommand():
    """Group with a hidden subcommand."""

    @click.group()
    def cli():
        """CLI."""

    @cli.command(hidden=True)
    def secret():
        """Secret."""

    @cli.command()
    def visible():
        """Visible."""

    return cli


@pytest.fixture
def empty_command():
    """Command with no parameters."""
    return make_command()
