# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
"""ocean.marine_toolkit.query_mwa_archive - Core functionality for querying the MWA Archive to obtain a list of obsids to process based on search criteria.
"""

from __future__ import annotations

from urllib import request, parse, error
import json
import logging
from pathlib import Path
from rich.progress import Progress
from typing import Dict, Any, Optional

logger: logging.Logger = logging.getLogger(__name__)

BASEURL = "http://ws.mwatelescope.org/"

def getmeta(servicetype: str='metadata', service: str='find', params: Optional[Dict[Any, Any]]=None) -> Optional[Dict[Any, Any]]:
    """Given a JSON web servicetype ('observation' or 'metadata'), a service name (eg 'obs', find, or 'con') and a set of parameters as a Python dictionary, return a Python dictionary containing the result.

    Args:
        servicetype (str, optional): Desired webservice data return. Defaults to 'metadata'.
        service (str, optional): Desired webservice end point to query. Defaults to 'find'.
        params (Optional[Dict[Any, Any]]): Additional parameters to pass to webservice. Defaults to None.

    Returns:
        Optional[Dict[Any, Any]]: Returned data structure from the webservice
    """
    
    if params:
        # Turn the dictionary into a string with encoded 'name=value' pairs
        url_params = parse.urlencode(params)
    else:
        url_params = ''

    # Get the data
    try:
        result: Optional[Dict[Any, Any]] = json.load(request.urlopen(BASEURL + servicetype + '/' + service + '?' + url_params))
    except error.HTTPError as err:
        logger.error("HTTP error from server: code=%d, response:\n %s" % (err.code, err.read()))
        raise err
    except error.URLError as err:
        logger.error("URL or network error: %s" % err.reason)
        raise err

    # Return the result dictionary
    return result

def query_MWA_archive(
    minra: float,
    maxra: float,
    mindec: float,
    maxdec: float,
    maxsunel: float = 0.0,
    mode: str = 'MWAX_CORRELATOR',
    contigfreq: int = 1,
    int_time: Optional[float] = None,
    freq_res: Optional[float] = None,
    project_id: Optional[str] = None,
    cent_chan: Optional[int] = None,
    output: Optional[Path] = None,
    verbose: bool = False
) -> None:
    """Query the MWA data archive to obtain a list of obsids to process based on the search criteria.

    Args:
        minra (float): Minimum right ascension (in degrees) of the observations to search for.
        maxra (float): Maximum right ascension (in degrees) of the observations to search for.
        mindec (float): Minimum declination (in degrees) of the observations to search for.
        maxdec (float): Maximum declination (in degrees) of the observations to search for.
        maxsunel (float): Maximum solar elevation (in degrees) of the observations to search for. Defaults to 0.0 (ie only return observations that are below the horizon).
        mode (str): Observation mode to search for.  Defaults to 'MWAX_CORRELATOR'.
        contigfreq (int): Whether to only return observations with contiguous frequency coverage (1) or not (0). Defaults to 1.
        int_time (float | None): Integration time (in seconds) to search for. Defaults to None.
        freq_res (float | None): Frequency resolution (in kHz) to search for. Defaults to None.
        project_id (str, optional): Project code associated with the desired observations. Defaults to None.
        cent_chan (int, optional): Only return the observations at the specified central frequecy. If None no specification is required. Defaults to None.
        output (Path | None, optional): Path to the output file where the list of observation IDs will be written. Defaults to None.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Returns:
        None
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
    obs_id_list: list[int] = []
    
    # Available options are described at
    # https://mwatelescope.atlassian.net/wiki/spaces/MP/pages/24969492/Observation+metadata+web+services
    meta_params = {
            'minra': minra,
            'maxra': maxra,
            'mindec': mindec,
            'maxdec': maxdec,
            'maxsunel': maxsunel,
            'mode': mode,
            'contigfreq': contigfreq,
            'notdeleted': 'on',
            'dataquality': 1,
            'int_time': int_time if int_time is not None else '',
            'freq_res': freq_res if freq_res is not None else '',
            'projectid': (project_id if project_id is not None else ''),
            'cenchan': (cent_chan if cent_chan is not None else ''),
            'dict': 1,
            'nocache': 1
    }

    obs_list = getmeta(service='find', params=meta_params)

    if obs_list is not None:
        with Progress(transient=True) as progress:
                task_id = progress.add_task("Checking ASVO data readiness", total=len(obs_list))

                for obs in obs_list:
                    obs_id: int = obs['mwas.starttime']
                    if obs['mwas.projectid'][0] != 'C':
                        if logger.isEnabledFor(logging.DEBUG):
                            progress.console.log(f"Checking {obs_id=}")

                        # Confirm that ASVO is ready to hand out the data
                        obs_ready = getmeta(service='data_ready', params={'obs_id':obs['mwas.starttime']})

                        if obs_ready is not None:
                            if obs_ready["dataready"] is True:
                                if logger.isEnabledFor(logging.DEBUG):
                                    progress.console.log(f"Data ready {obs_id=} appending")
                                obs_id_list.append(obs_id)
                            elif logger.isEnabledFor(logging.DEBUG):
                                progress.console.log(f"Data for {obs_id=} is not ready")
                        else:
                            progress.console.log(f"Failed to check data readiness for {obs_id=}. Skipping.", style="bold yellow")
                    else:
                        progress.console.log(f"Skipping {obs_id} because it belongs to a commissioning project.", style="bold yellow")

                    progress.advance(task_id)

    if len(obs_id_list) == 0:
        logger.error("Failed to find any matching observations. Please check your search criteria and try again.")
    else:
        logger.info(f"Found {len(obs_id_list)} matching observations.")
        if output:
            logger.info(f"Writing {len(obs_id_list)} obsids to {output}.")
            with open(output, "w") as f:
                for obs_id in obs_id_list:
                    f.write(f"{obs_id}\n")
        else:
            logger.info("Observation IDs:")
            for obs_id in obs_id_list:
                logger.info(obs_id)
