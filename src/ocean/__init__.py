# SPDX-FileCopyrightText: 2026-present Kenil Ajudiya <k.ajudiya@postgrad.curtin.edu.au>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

try:
    from ._version import __version__
except ImportError:
    print("Warning: Could not import version information from src/ocean/_version.py. Please run `hatch build` to generate it automatically.")
    pass