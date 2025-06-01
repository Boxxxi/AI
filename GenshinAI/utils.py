"""Utility functions for the GenshinAI project, including logging, file I/O, and path management."""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Setup root directory path handling
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import config

# Ensure logs directory exists
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


# Configure logging
def setup_logger(
    name: str, log_file: Optional[str] = None, level=logging.INFO
) -> logging.Logger:
    """Set up a logger with console and optional file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatters
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if log_file is specified
    if log_file:
        # Place log file in the logs directory
        log_path = os.path.join(LOGS_DIR, log_file)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Default logger
default_logger = setup_logger("genshin_ai", "genshin_ai.log")


# Data file handling
def ensure_data_dirs():
    """Ensure all data directories exist."""
    os.makedirs(config.USER_DATA_PATH, exist_ok=True)
    os.makedirs(config.META_DATA_PATH, exist_ok=True)
    default_logger.debug("Ensured data directories exist: %s", config.DATA_DIR)


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON data from a file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        default_logger.error("File not found: %s", file_path)
        return {}
    except json.JSONDecodeError:
        default_logger.error("Failed to parse JSON from file: %s", file_path)
        return {}


def save_json_file(data: Dict[str, Any], file_path: str, pretty: bool = True) -> bool:
    """Save data to a JSON file."""
    try:
        # Make sure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            if pretty:
                json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                json.dump(data, f, ensure_ascii=False)
        return True
    except Exception as e:
        default_logger.error("Failed to save JSON file %s: %s", file_path, e)
        return False


def get_user_data_file(uid: str) -> str:
    """Get the full path to a user's profile data file."""
    return os.path.join(config.USER_DATA_PATH, f"{uid}_profile.json")


def get_user_showcase_file(uid: str) -> str:
    """Get the full path to a user's showcase data file."""
    return os.path.join(config.USER_DATA_PATH, f"{uid}_showcase.json")


def get_meta_data_file(data_type: str) -> str:
    """Get the full path to a meta data file."""
    return os.path.join(config.META_DATA_PATH, f"{data_type}.json")


# Path handling for imports
def add_root_to_path():
    """Add the root directory to sys.path for imports."""
    if str(ROOT_DIR) not in sys.path:
        sys.path.append(str(ROOT_DIR))
        default_logger.debug("Added %s to Python path", ROOT_DIR)


# Initialize important directories
ensure_data_dirs()
