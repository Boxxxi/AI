"""Configuration settings for the GenshinAI application, loaded from environment variables."""

import json
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Bot settings
# -------------------
# Configuration for the Discord bot integration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Discord bot authentication token
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")  # Prefix for text commands

# API Keys
# --------
# Authentication for third-party services
CLAUDE_API_KEY = os.getenv(
    "CLAUDE_API_KEY"
)  # Anthropic Claude API key for GenshinAI advisor
CLAUDE_MODEL = os.getenv(
    "CLAUDE_MODEL", "claude-3-sonnet-20240229"
)  # Default Claude model

# Genshin Impact Account (optional)
# ------------------------------
# Default account for testing without user input
DEFAULT_GENSHIN_UID = os.getenv("GENSHIN_UID")  # Genshin Impact User ID for testing

# Data paths
# ---------
# File system organization for stored data
DATA_DIR = "data"  # Root directory for all data storage
USER_DATA_PATH = os.path.join(DATA_DIR, "users")  # User profile data storage location
META_DATA_PATH = os.path.join(DATA_DIR, "meta")  # Game metadata storage location

# API Endpoints
# ------------
# External service URLs
ENKA_API_BASE_URL = (
    "https://enka.network/api/uid/"  # Enka.Network API for character showcase data
)

# Trusted sources with trust scores
# --------------------------------
# Data sources with reliability ratings
TRUSTED_SOURCES = {
    "spiral_abyss_stats": {
        "url": "https://spiralabyss.org/floor-12",  # Source for Spiral Abyss usage statistics
        "trust_score": 0.9,  # Reliability score (0-1)
    },
    "genshin_wiki": {
        "url": "https://genshin-impact.fandom.com/wiki/",  # Source for character data
        "trust_score": 0.95,  # Reliability score (0-1)
    },
}

# Character ID mapping
# ------------------
# Maps Genshin Impact character IDs to character names
# Default empty dictionary as fallback
CHARACTER_ID_MAP = {}

# Load character mapping from JSON file
CHARACTER_MAPPING_FILE = os.path.join(META_DATA_PATH, "character_mapping.json")
try:
    if os.path.exists(CHARACTER_MAPPING_FILE):
        with open(CHARACTER_MAPPING_FILE, encoding="utf-8") as f:
            mapping_data = json.load(f)
            # Convert string keys to integers
            CHARACTER_ID_MAP = {int(k): v for k, v in mapping_data.items()}
    else:
        print(f"Warning: Character mapping file not found at {CHARACTER_MAPPING_FILE}")
except Exception as e:
    print(f"Error loading character mapping: {e}")
    # Continue with empty mapping, will use Character_ID fallback

# Refresh rates (in hours)
# ----------------------
# How often different data types should be updated
USER_DATA_REFRESH_RATE = 12  # Hours between user data refresh
META_DATA_REFRESH_RATE = 24  # Hours between game metadata refresh
