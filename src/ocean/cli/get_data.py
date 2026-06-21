# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
"""ocean.cli.get_data - Command-line interface for fetching data from the MWA Archive.
"""

from __future__ import annotations

import click
import logging

from ocean import giant_squid

from ocean.__about__ import __version__

# Time-stamped log file name to prevent overwriting previous logs.
logger: logging.Logger = logging.getLogger(__name__)

@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="ocean")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging (DEBUG level).")
def giant_squid(verbose: bool) -> None:
    """Fetches data from the MWA Archive based on user-specified criteria."""
    if verbose:
        logger.setLevel(logging.DEBUG)
    logger.info("Download data from the MWA Archive using the giant-squid.")
    # Call giant_squid to fetch data