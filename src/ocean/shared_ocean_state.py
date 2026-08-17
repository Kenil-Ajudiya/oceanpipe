# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
"""ocean.shared_ocean_state - A dataclass to hold shared state across different components of the OCEAN pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from ocean.config_manager import ConfigManager
# from ocean.database import DatabaseConnection

@dataclass
class SharedOceanState:
    """A dataclass to hold shared state across different components of the OCEAN pipeline.
    This class can be used to store configuration settings, database connections,
    and any other shared resources that need to be accessed by multiple parts of the pipeline.

    An instance of this class is automatically shared across all the subcommands of the OCEAN CLI by click's context management system.
    This allows for easy access to shared resources without the need for global variables or complex dependency injection.

    Attributes:
        config_manager (ConfigManager): An instance of the ConfigManager class, which handles loading and managing configuration settings for the OCEAN pipeline.
        database_connection (DatabaseConnection): (In the future) An instance of the DatabaseConnection class, which manages the connection to the transient search database.
    """
    config_manager: ConfigManager
    # database_connection: DatabaseConnection
