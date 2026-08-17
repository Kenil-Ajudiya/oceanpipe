# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
"""Defines the 'find_obsids' subcommand for the OCEAN CLI, allowing users to find observation IDs in the MWA archive."""

from __future__ import annotations

import click
import logging
from pathlib import Path
from astropy.coordinates import Angle
from astropy.units import hourangle, deg

from ocean.marine_toolkit.scour_mwa_archive import query_MWA_archive
from ocean.config_manager import ConfigManager
from ocean.shared_ocean_state import SharedOceanState

logger: logging.Logger = logging.getLogger(__name__)

def hms_to_deg(hms: str) -> float:
    """Convert a string in the format 'HH:MM:SS' to degrees

    Args:
        hms (str): String in the format 'HH:MM:SS'

    Returns:
        float: The equivalent value in degrees
    """
    try:
        return Angle(hms, unit=hourangle).degree
    except ValueError as err:
        logger.error(f"Invalid HMS format for RA: {hms}. Expected format is 'HH:MM:SS'. Error details: {err}")
        raise err

def dms_to_deg(dms: str) -> float:
    """Convert a string in the format 'DD:MM:SS' to degrees

    Args:
        dms (str): String in the format 'DD:MM:SS'

    Returns:
        float: The equivalent value in degrees
    """
    try:
        return Angle(dms, unit=deg).degree
    except ValueError as err:
        logger.error(f"Invalid DMS format for Dec: {dms}. Expected format is 'DD:MM:SS'. Error details: {err}")
        raise err

def parse_ra(value: str) -> float:
    """Parse RA as degrees or HH:MM:SS and return degrees."""
    try:
        return float(value)
    except ValueError:
        try:
            return hms_to_deg(value)
        except ValueError as err:
            raise click.BadParameter(
                f"Invalid --minra/--maxra value '{value}'. Use degrees or 'HH:MM:SS'."
            ) from err

def parse_dec(value: str) -> float:
    """Parse Dec as degrees or DD:MM:SS and return degrees."""
    try:
        return float(value)
    except ValueError:
        try:
            return dms_to_deg(value)
        except ValueError as err:
            raise click.BadParameter(
                f"Invalid --mindec/--maxdec value '{value}'. Use degrees or 'DD:MM:SS'."
            ) from err

@click.command()
@click.option("--minra", "-lr", type=parse_ra, help="Minimum right ascension to search for (format: 'HH:MM:SS' or in degrees).")
@click.option("--maxra", "-ur", type=parse_ra, help="Maximum right ascension to search for (format: 'HH:MM:SS' or in degrees).")
@click.option("--mindec", "-ld", type=parse_dec, help="Minimum declination to search for (format: 'DD:MM:SS' or in degrees).")
@click.option("--maxdec", "-ud", type=parse_dec, help="Maximum declination to search for (format: 'DD:MM:SS' or in degrees).")
@click.option("--maxsunel", "-s", type=float, default=0.0, help="Maximum elevation of the sun (in degrees). Defaults to 0.0.")
@click.option("--mode", "-m", type=str, default='MWAX_CORRELATOR', help="Observation mode to search for (eg: 'HW_LFILES', 'MWAX_BEAMFORMER', 'MWAX_VCS'). Defaults to MWAX_CORRELATOR.")
@click.option("--contigfreq", "-c", type=int, default=1, help="Only return observations with contiguous frequency coverage (1) or include both contiguous and non-contiguous (0). Defaults to 1.")
@click.option("--int-time", "-i", type=float, default=None, help="Integration time (in seconds) to search for. Defaults to None (i.e., include all integration times).")
@click.option("--freq-res", "-f", type=float, default=None, help="Frequency resolution (in kHz) to search for. Defaults to None (i.e., include all frequency resolutions).")
@click.option("--project-id", "-p", type=str, default=None, help="MWA observing project ID. Defaults to None (i.e., all projects).")
@click.option("--cent-chan", "-ch", type=int, default=None, help="Limit search to the specified central channel. Defaults to None (i.e., include all central channels).")
@click.option("--output", "-o", type=click.Path(writable=True, resolve_path=True, path_type=Path), default=None, help="Output directory or file path. If a directory is specified, a file named 'obs_ids.txt' will be created. If a file is specified, the list of observation IDs will be written to this file.")
@click.option("--update-config", "-u", is_flag=True, help="Whether to update the configuration file with the path to the obsid list output file. Defaults to False.")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging (DEBUG level).")
@click.pass_context
def find_obsids(
    click_context: click.Context,
    minra: float,
    maxra: float,
    mindec: float,
    maxdec: float,
    maxsunel: float,
    mode: str,
    contigfreq: int,
    int_time: float | None,
    freq_res: float | None,
    project_id: str | None,
    cent_chan: int | None,
    output: Path | None,
    verbose: bool,
    update_config: bool,
) -> None:
    """
    Query the MWA archive to find observation IDs based on search criteria.
    
    Visit https://ws.mwatelescope.org/metadata/find and https://mwatelescope.atlassian.net/wiki/spaces/MP/pages/24969492/Observation+metadata+web+services
    for more details on search options and their acceptable values.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("Querying MWA archive with the specified criteria...")

    shared_state: SharedOceanState = click_context.obj
    config_manager: ConfigManager = shared_state.config_manager

    if output is None:
        output = Path.cwd() / "obs_ids.txt"
    else:
        if output.is_dir():
            output = output / "obs_ids.txt"
        output.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Observation IDs will be written to: {output}")
    if update_config:
        logger.info("Updating configuration with the output file path for ObsID list...")
        config_manager.set("ObsID list", str(output))

    query_MWA_archive(
        minra,
        maxra,
        mindec,
        maxdec,
        maxsunel,
        mode,
        contigfreq,
        int_time,
        freq_res,
        project_id,
        cent_chan,
        output,
        verbose
    )
