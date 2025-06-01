#!/usr/bin/env python3
"""Script to fetch Genshin Impact character showcase data from Enka.Network API."""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import aiohttp

import config
import utils


async def fetch_enka_data(uid):
    """Fetch user data from Enka.Network API."""
    url = f"{config.ENKA_API_BASE_URL}{uid}"
    print(f"📡 Fetching data from Enka.Network: {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to fetch data: HTTP {response.status}")


def process_enka_data(data):
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
            "finish_achievement_num": data["playerInfo"].get("finishAchievementNum", 0),
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
            avatar_id = avatar.get("avatarId", 0)
            char_name = config.CHARACTER_ID_MAP.get(avatar_id, f"Character_{avatar_id}")

            char_data = {
                "avatar_id": avatar_id,
                "name": char_name,
                "level": avatar.get("propMap", {}).get("4001", {}).get("val", 0),
                "constellation": len(avatar.get("talentIdList", [])),
                "friendship": avatar.get("fetterInfo", {}).get("expLevel", 0),
                "equipment": {"weapon": {}, "artifacts": []},
            }

            # Process equipment (weapon and artifacts)
            if "equipList" in avatar:
                for equip in avatar["equipList"]:
                    if "weapon" in equip:
                        # This is a weapon
                        weapon = equip["weapon"]
                        char_data["equipment"]["weapon"] = {
                            "id": weapon.get("itemId", 0),
                            "level": weapon.get("level", 1),
                            "refinement": next(
                                iter(weapon.get("affixMap", {}).values()), 0
                            )
                            + 1
                            if "affixMap" in weapon
                            else 1,
                            "main_stat": equip.get("flat", {})
                            .get("weaponStats", [{}])[0]
                            .get("statValue", 0)
                            if equip.get("flat", {}).get("weaponStats")
                            else 0,
                        }
                    elif "flat" in equip and "reliquaryMainstat" in equip["flat"]:
                        # This is an artifact
                        artifact = {
                            "id": equip.get("itemId", 0),
                            "set_id": equip.get("flat", {}).get(
                                "setNameTextMapHash", 0
                            ),
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

                        char_data["equipment"]["artifacts"].append(artifact)

            result["player_info"]["showcase_characters"].append(char_data)

    return result


async def main():
    """Fetch and process Enka.Network data for a Genshin Impact user.

    This function prompts for a UID if not provided in the config,
    fetches the user's showcase data from Enka.Network, processes it,
    and saves both raw and processed data to files.
    """
    print("🔍 Genshin Impact Enka.Network Data Fetcher")
    print("----------------------------------------")

    # Get UID from environment or prompt
    uid = config.DEFAULT_GENSHIN_UID or input("Enter your Genshin Impact UID: ").strip()

    if not uid:
        print("❌ Error: UID is required.")
        return

    try:
        int(uid)
        if len(uid) != 9:
            print("⚠️ Warning: UID should be a 9-digit number. Continuing anyway...")
    except ValueError:
        print("❌ Error: UID should be numeric")
        return

    try:
        # Make sure data directories exist
        utils.ensure_data_dirs()

        # Create a temp directory for raw data if needed
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)

        # Fetch data from Enka.Network
        data = await fetch_enka_data(uid)

        # Process the data
        processed_data = process_enka_data(data)

        # Save raw data to temp directory
        raw_file = temp_dir / f"{uid}_enka_raw.json"
        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Raw Enka.Network data saved to {raw_file}")

        # Save processed data to temp directory
        processed_file = temp_dir / f"{uid}_enka_processed.json"
        with open(processed_file, "w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Processed Enka.Network data saved to {processed_file}")

        # Show summary
        print("\n📊 Player Summary:")
        print(f"Nickname: {processed_data['player_info']['nickname']}")
        print(f"Adventure Rank: {processed_data['player_info']['level']}")
        print(f"World Level: {processed_data['player_info']['world_level']}")
        print(
            f"Achievements: {processed_data['player_info']['finish_achievement_num']}"
        )

        # Show showcased characters
        showcase_chars = processed_data["player_info"]["showcase_characters"]
        if showcase_chars:
            print(f"\n⭐ Showcased Characters ({len(showcase_chars)}):")
            for i, char in enumerate(showcase_chars, 1):
                char_name = char.get("name", f"Character {char['avatar_id']}")
                print(
                    f"{i}. {char_name} (Level {char['level']}, Constellation {char['constellation']})"
                )
        else:
            print("\n⚠️ No characters are currently showcased.")

        # Ask if user wants to see full JSON
        show_json = input("\nDo you want to see the processed JSON? (y/n): ").lower()
        if show_json == "y":
            print("\n📋 Processed Data (JSON):")
            formatted_json = json.dumps(processed_data, indent=2, ensure_ascii=False)
            print(formatted_json)

        # Save to proper data directory using utils
        showcase_file = utils.get_user_showcase_file(uid)
        utils.save_json_file(processed_data, showcase_file)
        print(f"\n💾 Data saved to {showcase_file} for use with GenshinAI")

        # Also create a profile-like data structure for compatibility
        profile_data = create_profile_from_showcase(processed_data)
        profile_file = utils.get_user_data_file(uid)
        utils.save_json_file(profile_data, profile_file)
        print(f"💾 Profile data saved to {profile_file}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n⚠️ Troubleshooting tips:")
        print("1. Make sure your UID is correct")
        print(
            "2. Make sure you have characters showcased in your Genshin Impact profile"
        )
        print("3. The Enka.Network API might be down or experiencing issues")


def create_profile_from_showcase(showcase_data):
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
        char_name = char.get(
            "name", config.CHARACTER_ID_MAP.get(char_id, f"Character_{char_id}")
        )

        profile_data["characters"][char_name] = {
            "id": char_id,
            "level": int(char.get("level", 1)),
            "constellation": char.get("constellation", 0),
            "friendship": char.get("friendship", 1),
            "weapon": char.get("equipment", {}).get("weapon", {}),
        }

    return profile_data


if __name__ == "__main__":
    asyncio.run(main())
