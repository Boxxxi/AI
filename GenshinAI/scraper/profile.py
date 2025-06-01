"""Scraper module for retrieving Genshin Impact player profile data from Enka.Network API."""

import asyncio
import os
import sys

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aiohttp
from dotenv import load_dotenv

import config
import utils

# Get logger
logger = utils.setup_logger("profile_scraper")


class ProfileScraper:
    """Scraper for retrieving Genshin Impact player profile data from Enka.Network API.

    This class provides functionality to connect to Enka.Network, fetch character
    showcase data for a specified UID, process the raw API response into structured data,
    and save it in multiple formats for compatibility with different parts of the system.

    Unlike previous HoYoLAB-based scrapers, this uses the public Enka.Network API which
    only requires a Genshin Impact UID without authentication.
    """

    def __init__(self, uid=None):
        """Initialize the profile scraper with a Genshin Impact UID."""
        self.uid = uid

    async def set_uid(self, uid):
        """Set Genshin Impact UID."""
        self.uid = uid

    async def fetch_showcase_data(self):
        """Fetch user character showcase data from Enka.Network API."""
        if not self.uid:
            raise ValueError("UID is required to fetch data from Enka.Network")

        url = f"{config.ENKA_API_BASE_URL}{self.uid}"
        logger.info("Fetching data from Enka.Network: %s", url)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    # Process raw data into a more structured format
                    processed_data = self._process_enka_data(data)

                    # Save showcase data to file
                    self._save_showcase_data(processed_data)

                    # Also create and save a profile-like data structure for compatibility
                    profile_data = self._create_profile_from_showcase(processed_data)
                    self._save_profile_data(profile_data)

                    return processed_data
                else:
                    error_msg = (
                        f"Failed to fetch data from Enka.Network: {response.status}"
                    )
                    logger.error(error_msg)
                    raise Exception(error_msg)

    def _process_enka_data(self, data):
        """Process the raw Enka.Network data into a more readable format."""
        if not data or "playerInfo" not in data:
            return {"error": "No player info found"}

        result = {
            "player_info": {
                "nickname": data["playerInfo"].get("nickname", "Unknown"),
                "level": data["playerInfo"].get("level", 0),
                "signature": data["playerInfo"].get("signature", ""),
                "world_level": data["playerInfo"].get("worldLevel", 0),
                "name_card_id": data["playerInfo"].get("nameCardId", 0),
                "finish_achievement_num": data["playerInfo"].get(
                    "finishAchievementNum", 0
                ),
                "profile_picture": {
                    "avatar_id": data["playerInfo"]
                    .get("profilePicture", {})
                    .get("avatarId", 0)
                },
                "showcase_characters": [],
            }
        }

        # Process showcased characters
        if "avatarInfoList" in data:
            for avatar in data["avatarInfoList"]:
                char_data = {
                    "avatar_id": avatar.get("avatarId", 0),
                    "level": avatar.get("propMap", {}).get("4001", {}).get("val", 0),
                    "constellation": len(avatar.get("talentIdList", [])),
                    "friendship": avatar.get("fetterInfo", {}).get("expLevel", 0),
                    "equipment": self._parse_equipment(avatar),
                }

                result["player_info"]["showcase_characters"].append(char_data)

        return result

    def _parse_equipment(self, avatar_data):
        """Parse equipment data from avatar showcase."""
        equipment = {"weapon": {}, "artifacts": []}

        if "equipList" in avatar_data:
            for equip in avatar_data["equipList"]:
                if "weapon" in equip:
                    # This is a weapon
                    weapon = equip["weapon"]
                    equipment["weapon"] = {
                        "id": weapon.get("itemId", 0),
                        "level": weapon.get("level", 1),
                        "refinement": next(iter(weapon.get("affixMap", {}).values()), 0)
                        + 1
                        if "affixMap" in weapon
                        else 1,
                        "main_stat": equip.get("flat", {})
                        .get("weaponStats", [{}])[0]
                        .get("statValue", 0)
                        if equip.get("flat", {}).get("weaponStats")
                        else 0,
                    }
                elif "flat" in equip and "reliquaryMainstat" in equip.get("flat", {}):
                    # This is an artifact
                    artifact = {
                        "id": equip.get("itemId", 0),
                        "set_id": equip.get("flat", {}).get("setNameTextMapHash", 0),
                        "level": equip.get("reliquary", {}).get("level", 0)
                        - 1,  # Artifact level starts at 1
                        "rarity": equip.get("flat", {}).get("rankLevel", 0),
                        "main_stat": {
                            "prop_id": equip.get("flat", {})
                            .get("reliquaryMainstat", {})
                            .get("mainPropId", ""),
                            "value": equip.get("flat", {})
                            .get("reliquaryMainstat", {})
                            .get("statValue", 0),
                        },
                        "sub_stats": [],
                    }

                    # Add sub stats
                    if "reliquarySubstats" in equip.get("flat", {}):
                        for substat in equip["flat"]["reliquarySubstats"]:
                            artifact["sub_stats"].append(
                                {
                                    "prop_id": substat.get("appendPropId", ""),
                                    "value": substat.get("statValue", 0),
                                }
                            )

                    equipment["artifacts"].append(artifact)

        return equipment

    def _create_profile_from_showcase(self, showcase_data):
        """Create a profile-like data structure from showcase data for compatibility."""
        if "error" in showcase_data:
            return {"error": showcase_data["error"]}

        player_info = showcase_data.get("player_info", {})
        showcase_chars = player_info.get("showcase_characters", [])

        profile_data = {
            "account_info": {
                "nickname": player_info.get("nickname", "Traveler"),
                "level": player_info.get("level", 1),
                "world_level": player_info.get("world_level", 0),
                "signature": player_info.get("signature", ""),
                "achievements": player_info.get("finish_achievement_num", 0),
                "abyss_floor": 0,
                "abyss_level": 0,
                "characters": len(showcase_chars),
            },
            "characters": {},
        }

        # Add character data from showcase
        for char in showcase_chars:
            char_id = char.get("avatar_id", 0)
            # Get character name from ID using config mapping or fallback to Character_ID
            char_name = config.CHARACTER_ID_MAP.get(char_id, f"Character_{char_id}")

            profile_data["characters"][char_name] = {
                "id": char_id,
                "level": int(char.get("level", 1)),
                "constellation": char.get("constellation", 0),
                "friendship": char.get("friendship", 1),
                "weapon": char.get("equipment", {}).get("weapon", {}),
            }

        return profile_data

    def _save_showcase_data(self, showcase_data):
        """Save showcase data to file."""
        if not self.uid:
            return

        file_path = utils.get_user_showcase_file(self.uid)
        if utils.save_json_file(showcase_data, file_path):
            logger.info("Saved showcase data for UID %s", self.uid)
        else:
            logger.error("Failed to save showcase data for UID %s", self.uid)

    def _save_profile_data(self, profile_data):
        """Save profile data to file."""
        if not self.uid:
            return

        file_path = utils.get_user_data_file(self.uid)
        if utils.save_json_file(profile_data, file_path):
            logger.info("Saved profile data for UID %s", self.uid)
        else:
            logger.error("Failed to save profile data for UID %s", self.uid)


async def main():
    """Test function to retrieve user showcase data."""
    # Load environment variables
    load_dotenv()

    # Get UID from environment or prompt user
    uid = os.getenv("GENSHIN_UID")
    if not uid:
        uid = input("Enter your Genshin Impact UID: ").strip()

    if not uid:
        logger.error("Missing UID. Please provide your Genshin Impact UID.")
        return

    scraper = ProfileScraper(uid=uid)

    logger.info("Fetching showcase data from Enka.Network...")
    try:
        showcase_data = await scraper.fetch_showcase_data()

        # Display summary of fetched data
        player_info = showcase_data.get("player_info", {})
        chars = player_info.get("showcase_characters", [])

        logger.info(
            "Retrieved data for %s (AR%s)",
            player_info.get("nickname", "Unknown"),
            player_info.get("level", 0),
        )
        logger.info("Found %s character(s) in showcase", len(chars))

        # List characters found
        for i, char in enumerate(chars, 1):
            logger.info(
                "%s. Character ID: %s, Level: %s, Constellation: %s",
                i,
                char.get("avatar_id"),
                char.get("level"),
                char.get("constellation"),
            )

    except Exception as e:
        logger.error("Error fetching showcase data: %s", e)


if __name__ == "__main__":
    asyncio.run(main())
