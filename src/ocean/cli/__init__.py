# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
"""ocean.cli: Command-line interface for OCEAN.

This module serves as the entry point for the OCEAN command-line tool,
providing a user-friendly interface to access various functionalities of the OCEAN pipeline,
including data fetching, imaging, candidate classification and transient search database management.
Each subcommand corresponds to a specific task within the pipeline,
allowing users to easily execute complex workflows with simple commands.

The CLI is built using the Click library, which provides a powerful and flexible framework for creating command-line interfaces.
The logging system is configured to provide rich, informative output to the console using the Rich library,
while also maintaining detailed logs in a file for later analysis and debugging.
"""

from __future__ import annotations

import click
import logging
from pathlib import Path

from .logger_design import setup_logger
from .config_cli import configure
from .query_archive import find_obsids
from .fetch_data import call_giant_squid

from ocean.config_manager import ConfigManager
from ocean.shared_ocean_state import SharedOceanState
from ocean.__about__ import __version__

@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="ocean")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging (DEBUG level).")
@click.option("--config-file", "-c", type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path), help="Path to the configuration file (YAML format).")
@click.pass_context
def ocean(click_context: click.Context, verbose: bool, config_file: Path) -> None:
    """OCEAN - A pipeline to scour for Outbursts of Coherent Emission Amidst Noise in the MWA Archive."""
    # Time-stamped log file name to prevent overwriting previous logs. Format: ocean_2024-06-01_12-00-00.log
    log_file = Path(f"deep_logs/ocean_{logging.Formatter(datefmt='%Y-%m-%d_%H%M%S').formatTime(logging.LogRecord('', 0, '', 0, '', None, None))}.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    setup_logger(log_file=log_file)
    logger: logging.Logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)
    if click_context.invoked_subcommand is None:
        logger.info("Welcome to a rich OCEAN - Outbursts of Coherent Emission Amidst Noise!")
        logger.info("Use --help to see available subcommands and options.")

    # Initialize the configuration manager and store it in the shared state for seamless access across all the subcommands of the OCEAN CLI.
    config_manager = ConfigManager(config_file)
    click_context.obj = SharedOceanState(config_manager)

ocean.add_command(configure)
ocean.add_command(find_obsids)
ocean.add_command(call_giant_squid)
