#!/usr/bin/env python3
"""Script to test the character recommender with the user's data."""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config
from engine.character_recommender import CharacterRecommender


async def main():
    """Test the character recommender with the user's data."""
    print("🔍 Testing Character Recommender")
    print("-----------------------------")

    # Get the user's UID from environment or prompt
    uid = config.DEFAULT_GENSHIN_UID or input("Enter your Genshin Impact UID: ").strip()

    if not uid:
        print("❌ Error: UID is required.")
        return

    # Check if showcase data exists
    showcase_file = Path(f"data/users/{uid}_showcase.json")
    if not showcase_file.exists():
        print(f"❌ Error: No showcase data found for UID {uid}.")
        print("Please run enka_fetch.py first to get your character data.")
        return

    # Load character data to convert IDs to names
    try:
        char_data_file = Path("data/meta/character_data.json")
        if char_data_file.exists():
            with open(char_data_file, encoding="utf-8") as f:
                char_data = json.load(f)
                # Update our mapping with any additional characters from meta data
                for char_id, char_info in char_data.items():
                    if char_info.get("name"):
                        config.CHARACTER_ID_MAP[int(char_id)] = char_info["name"]
    except Exception as e:
        print(f"⚠️ Warning: Could not load character meta data: {e}")

    # Create profile data from showcase if needed
    profile_file = Path(f"data/users/{uid}_profile.json")
    if not profile_file.exists():
        print(f"ℹ️ Creating profile data from showcase for UID {uid}...")

        # Load showcase data
        with open(showcase_file, encoding="utf-8") as f:
            showcase_data = json.load(f)

        # Create minimal profile data
        player_info = showcase_data.get("player_info", {})
        showcase_chars = player_info.get("showcase_characters", [])

        profile_data = {
            "account_info": {
                "nickname": player_info.get("nickname", "Traveler"),
                "level": player_info.get("level", 1),
                "world_level": player_info.get("world_level", 0),
                "achievements": player_info.get("finish_achievement_num", 0),
                "characters": len(showcase_chars),
            },
            "characters": {},
        }

        # Add character data from showcase
        for char in showcase_chars:
            char_id = char.get("avatar_id", 0)
            # Get character name from ID using config mapping
            char_name = config.CHARACTER_ID_MAP.get(char_id, f"Character_{char_id}")

            profile_data["characters"][char_name] = {
                "id": char_id,
                "level": int(char.get("level", 1)),
                "constellation": char.get("constellation", 0),
                "friendship": char.get("friendship", 1),
            }

        # Save profile data
        with open(profile_file, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)

        print(
            f"✅ Created profile data with {len(profile_data['characters'])} characters."
        )

    try:
        # Initialize recommender
        recommender = CharacterRecommender(uid)

        # Get build priority recommendations
        print("\n📊 Getting Character Build Priority Recommendations...")
        build_recommendations = recommender.get_build_priority(count=5)

        if build_recommendations:
            print("\n🔨 Build Priority Recommendations:")
            for i, rec in enumerate(build_recommendations, 1):
                char_id = None
                try:
                    # Try to extract character ID if present in the name (Character_10000022)
                    if rec["name"].startswith("Character_"):
                        char_id = int(rec["name"].split("_")[1])
                        char_name = config.CHARACTER_ID_MAP.get(char_id, rec["name"])
                    else:
                        char_name = rec["name"]
                except (ValueError, IndexError, KeyError):
                    char_name = rec["name"]

                print(f"{i}. {char_name} (Level {rec['current_level']})")
                print(f"   Score: {rec['priority_score']:.2f}")
                if "reasons" in rec and rec["reasons"]:
                    print(f"   Reasons: {', '.join(rec['reasons'])}")
                print()
        else:
            print("❌ No build recommendations could be generated.")

        # Get pull recommendations
        print("\n📊 Getting Character Pull Recommendations...")
        try:
            pull_recommendations = recommender.get_pull_recommendations(count=3)

            if pull_recommendations:
                print("\n🎯 Character Pull Recommendations:")
                for i, rec in enumerate(pull_recommendations, 1):
                    print(
                        f"{i}. {rec['name']} ({rec.get('element', 'Unknown')} {rec.get('weapon_type', 'Unknown')})"
                    )
                    print(f"   Score: {rec['recommendation_score']:.2f}")
                    if "reasons" in rec and rec["reasons"]:
                        print(f"   Reasons: {', '.join(rec['reasons'])}")
                    print()
            else:
                print("❌ No pull recommendations could be generated.")
        except Exception as e:
            print(f"⚠️ Could not generate pull recommendations: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
