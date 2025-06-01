#!/usr/bin/env python3
"""Script to initialize GenshinAI data directories and scrape initial meta data."""

import argparse
import asyncio
import json
import os
import sys

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import aiohttp

import config
import utils

logger = utils.setup_logger("init_data")


async def scrape_meta_data():
    """Scrape and process game metadata from external resources."""
    # Ensure data directories exist
    utils.ensure_data_dirs()
    logger.info("Initializing data directories and scraping meta data...")

    await init_meta_data()

    logger.info("Meta data initialization complete!")


async def init_meta_data():
    """Initialize metadata by fetching game statistics and character data."""
    meta_file = utils.get_meta_data_file("meta_data")
    abyss_file = utils.get_meta_data_file("spiral_abyss_stats")
    character_file = utils.get_meta_data_file("character_data")

    try:
        # Create base structure if it doesn't exist
        if os.path.exists(meta_file):
            with open(meta_file, encoding="utf-8") as f:
                meta_data = json.load(f)
        else:
            meta_data = {"spiral_abyss_stats": {}, "characters": {}}

        # Fetch spiral abyss usage statistics
        logger.info("Fetching Spiral Abyss usage statistics...")
        try:
            abyss_data = await fetch_spiral_abyss_data()
            meta_data["spiral_abyss_stats"] = abyss_data

            # Save abyss data to its own file as well
            with open(abyss_file, "w", encoding="utf-8") as f:
                json.dump(abyss_data, f, indent=2)
        except Exception as e:
            logger.error("Error fetching Spiral Abyss data: %s", e)

        # Fetch character data
        logger.info("Fetching character data...")
        try:
            character_data = await fetch_character_data()
            meta_data["characters"] = character_data

            # Save character data to its own file as well
            with open(character_file, "w", encoding="utf-8") as f:
                json.dump(character_data, f, indent=2)

            # Update character mapping
            await update_character_mapping()

        except Exception as e:
            logger.error("Error fetching character data: %s", e)

        # Save meta data
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, indent=2)

        logger.info("Meta data initialized and saved successfully")

    except Exception as e:
        logger.error("Error initializing meta data: %s", e)


async def fetch_spiral_abyss_data():
    """Fetch Spiral Abyss usage statistics from external API."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://spiralabyss.org/floor-12") as response:
            if response.status == 200:
                html = await response.text()
                # This would normally involve parsing HTML with BeautifulSoup
                # For now, we're just returning placeholder data
                logger.debug(
                    "Received Spiral Abyss HTML, length: %s characters", len(html)
                )
                return {
                    "most_used_characters": [
                        {"id": 10000002, "name": "Ayaka", "usage_rate": 75.6},
                        {"id": 10000025, "name": "Xingqiu", "usage_rate": 68.2},
                        {"id": 10000030, "name": "Zhongli", "usage_rate": 65.9},
                        {"id": 10000046, "name": "Hu Tao", "usage_rate": 63.1},
                        {"id": 10000033, "name": "Tartaglia", "usage_rate": 60.8},
                    ],
                    "most_used_teams": [
                        {
                            "characters": ["Hu Tao", "Xingqiu", "Zhongli", "Albedo"],
                            "usage_count": 1245,
                        },
                        {
                            "characters": ["Ayaka", "Mona", "Diona", "Venti"],
                            "usage_count": 1120,
                        },
                    ],
                }
            else:
                logger.error(
                    "Failed to fetch Spiral Abyss data, status code: %s",
                    response.status,
                )
                return {}


async def fetch_character_data():
    """Fetch character data from Genshin Impact API."""
    # For now, using placeholder data
    return {
        "10000002": {
            "id": 10000002,
            "name": "Ayaka",
            "rarity": 5,
            "element": "Cryo",
            "weapon_type": "Sword",
            "stats": {
                "hp": 12858,
                "attack": 342,
                "defense": 784,
                "crit_rate": 5.0,
                "crit_dmg": 88.4,
                "energy_recharge": 100.0,
            },
        },
        "10000025": {
            "id": 10000025,
            "name": "Xingqiu",
            "rarity": 4,
            "element": "Hydro",
            "weapon_type": "Sword",
            "stats": {
                "hp": 10222,
                "attack": 202,
                "defense": 758,
                "crit_rate": 5.0,
                "crit_dmg": 50.0,
                "energy_recharge": 100.0,
            },
        },
    }


async def update_character_mapping():
    """Update character mapping from character data."""
    character_file = utils.get_meta_data_file("character_data")
    character_mapping_file = utils.get_meta_data_file("character_mapping")

    try:
        # Load character data
        if os.path.exists(character_file):
            with open(character_file, encoding="utf-8") as f:
                character_data = json.load(f)
        else:
            logger.error("Character data file not found: %s", character_file)
            return False

        # Generate character ID to name mapping from character data
        logger.info("Generating character ID to name mapping...")
        character_mapping = {}
        for char_id, char_info in character_data.items():
            if "name" in char_info:
                character_mapping[char_id] = char_info["name"]

        # Also merge with existing character mapping if it exists
        if os.path.exists(character_mapping_file):
            try:
                with open(character_mapping_file, encoding="utf-8") as f:
                    existing_mapping = json.load(f)
                # Update with new characters but preserve existing mappings
                existing_mapping.update(character_mapping)
                character_mapping = existing_mapping
            except Exception as mapping_error:
                logger.error(
                    "Error reading existing character mapping: %s", mapping_error
                )

        # Default mappings for important characters that might not be in the API
        default_mappings = {
            "10000005": "Traveler",
            "10000006": "Lisa",
            "10000007": "Amber",
            "10000014": "Barbara",
            "10000015": "Kaeya",
            "10000020": "Razor",
            "10000021": "Fischl",
        }
        # Add defaults only if they don't exist yet
        for char_id, char_name in default_mappings.items():
            if char_id not in character_mapping:
                character_mapping[char_id] = char_name

        # Save the character mapping
        with open(character_mapping_file, "w", encoding="utf-8") as f:
            json.dump(character_mapping, f, indent=2, ensure_ascii=False)

        logger.info(
            "Character mapping updated with %s characters", len(character_mapping)
        )
        return True

    except Exception as e:
        logger.error("Error updating character mapping: %s", e)
        return False


def main():
    """Initialize GenshinAI data directories and metadata.

    This function parses command line arguments to determine whether to
    force update metadata or just update character mappings. It ensures
    data directories exist and runs the appropriate initialization routines.
    """
    parser = argparse.ArgumentParser(description="Initialize GenshinAI data")
    parser.add_argument(
        "--force", action="store_true", help="Force update meta data even if it exists"
    )
    parser.add_argument(
        "--update-mapping", action="store_true", help="Update character ID mapping only"
    )
    args = parser.parse_args()

    logger.info("=== GenshinAI Data Initialization ===")

    # Check if required directories exist
    if not os.path.exists(config.DATA_DIR):
        os.makedirs(config.DATA_DIR, exist_ok=True)
        logger.info("Created data directory: %s", config.DATA_DIR)

    if args.update_mapping:
        # Only update character mapping
        asyncio.run(update_character_mapping())
        logger.info("Character mapping update complete!")
    else:
        # Initialize all meta data
        asyncio.run(scrape_meta_data())
        logger.info("Data initialization complete!")

    logger.info("You can now start the bot with: python bot/main.py")


if __name__ == "__main__":
    main()
