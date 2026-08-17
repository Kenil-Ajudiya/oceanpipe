# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
"""ocean.cli.fetch_data - Command-line interface for fetching data from the MWA Archive.
"""

from __future__ import annotations

import click
import logging

from ocean import giant_squid
from ocean.config_manager import ConfigManager
from ocean.shared_ocean_state import SharedOceanState
from ocean.__about__ import __version__

@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging (DEBUG level).")
@click.pass_context
def call_giant_squid(click_context: click.Context, verbose: bool) -> None:
    """Fetches data from the MWA Archive based on user-specified criteria."""
    # Time-stamped log file name to prevent overwriting previous logs.
    logger: logging.Logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)
    shared_state: SharedOceanState = click_context.obj
    config_manager: ConfigManager = shared_state.config_manager
    logger.info("Download data from the MWA Archive using the giant-squid.")
    # Call giant_squid to fetch data
    giant_squid.fetch_giant_dataset("1234567890")
