"""
Path initialization script for GenshinAI.

This module initializes the Python import path to include the project root directory.
Import this module before any other project imports to ensure proper relative imports.

Example:
    from scripts import init_path  # noqa
    import config
"""

import os
import sys

# Add project root to path if not already there
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
