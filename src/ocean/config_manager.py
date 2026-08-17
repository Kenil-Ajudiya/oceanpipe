# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
"""ocean.config_manager - A class to manage configuration settings for the OCEAN pipeline."""

from __future__ import annotations

import logging
import yaml
from pathlib import Path
from typing import Dict, Any

logger: logging.Logger = logging.getLogger(__name__)

class ConfigManager:
    """A class to manage configuration settings for the OCEAN pipeline."""

    def __init__(self, config_file: Path | None) -> None:
        """Initialize the ConfigManager with a path to the configuration file."""
        if config_file is not None:
            self.config_file = config_file
            if config_file.exists():
                self.configuration = self.load_config()
            else:
                logger.warning(f"Configuration file {config_file} not found. Creating an example configuration file.")
                self.write_example_config()
                exit(1)

    def load_config(self) -> Dict[str, Any]:
        """Load the configuration from the YAML file."""
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value by key."""
        self.configuration[key] = value
        self.save_config()

    def save_config(self) -> None:
        """Save the current configuration back to the YAML file."""
        with open(self.config_file, 'w') as f:
            yaml.safe_dump(self.configuration, f)

    def view_config(self) -> None:
        """View the current configuration on the console."""
        logger.info(f"Configuration loaded from {self.config_file}:")
        for key, value in self.configuration.items():
            logger.info(f"{key}: {value}")

    def write_example_config(self, output_file = Path("example_config.yaml")) -> None:
        """Write an example configuration file with default values."""
        example_config = {
            "ObsID list": "/absolute/path/to/obs_ids.txt",
            "Data directory": "/absolute/path/to/data/directory/",
            "Log directory": "/absolute/path/to/logs/directory/",
            "Log level": "INFO"
        }
        with open(output_file, 'w') as f:
            yaml.safe_dump(example_config, f)
