# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
"""ocean.cli.config_cli - Command-line interface for oceanpipe configuration management.
"""

from __future__ import annotations

import click
from pathlib import Path

from ocean.config_manager import ConfigManager
from ocean.__about__ import __version__

@click.group(invoke_without_command=False)
def configure() -> None:
    """Configuration manager for oceanpipe.

    This command exposes functionalities from the ConfigManager class, allowing users to view, set, 
    and manage configuration settings for the OCEAN pipeline."""
    pass

@configure.command("write-example-config")
@click.option("--output-file", "-o", type=click.Path(resolve_path=True, path_type=Path), default="example_config.yaml", help="Path to the output example configuration file (YAML format).")
def write_example_config(output_file: Path) -> None:
    """Write an example configuration file with default values."""
    config_manager = ConfigManager(None)  # Initialize with None since we are creating a new config
    config_manager.write_example_config(output_file)

@configure.command("view")
@click.option("--config-file", "-c", type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path), default="./configuration/config.yaml", help="Path to the configuration file (YAML format).")
def view(config_file: Path) -> None:
    """View the current configuration."""
    config_manager = ConfigManager(config_file)
    config_manager.view_config()

@configure.command("set")
@click.option("--config-file", "-c", type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path), default="./configuration/config.yaml", help="Path to the configuration file (YAML format).")
@click.argument("key")
@click.argument("value")
def set(config_file: Path, key: str, value: str) -> None:
    """Set a configuration value by key."""
    config_manager = ConfigManager(config_file)
    config_manager.set(key, value)