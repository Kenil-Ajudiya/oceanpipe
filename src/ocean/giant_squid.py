# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
"""ocean.giant_squid - Core functionality for fetching data from the MWA Archive using the giant-squid software.
"""

from __future__ import annotations
from datetime import datetime
from prefect import flow, task, get_run_logger
from prefect.runtime import flow_run

def giant_squid_flow_run_name():
    # Retrieve parameters passed to the flow at runtime
    params = flow_run.get_parameters()
    obs_id = params.get("obs_id", "unknown")
    date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"download-{obs_id}-{date_str}"

@task(task_run_name="download-{obs_id}")
def hello(obs_id: str = "ObsID") -> None:
    logger = get_run_logger()
    logger.info(f"I'm ready to fetch data for ObsID {obs_id} from the MWA Archive using the giant-squid software.")

@flow(name="Fetch Giant Dataset", flow_run_name=giant_squid_flow_run_name)
def fetch_giant_dataset(obs_id: str = "ObsID") -> None:
    hello(obs_id)

if __name__ == "__main__":
    fetch_giant_dataset()
