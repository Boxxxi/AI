"""Engine for analyzing player data and recommending optimal primogem acquisition strategies."""

import os
import sys
from typing import Any, Dict, List

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
import utils

# Setup logger
logger = utils.setup_logger("primogem_recommender")


class PrimogemRecommender:
    """Recommendation engine for Genshin Impact primogem acquisition strategies.

    This class analyzes player data to identify the most efficient and
    valuable sources of primogems based on the user's current progression.
    It provides personalized recommendations for:
    - Incomplete content with primogem rewards
    - Unexplored regions with chests and oculi
    - Recurring sources like Spiral Abyss
    - Event participation opportunities

    Each recommendation includes an estimated primogem value, difficulty level,
    and detailed instructions to help players maximize their primogem income.
    """

    def __init__(self, user_id=None):
        """Initialize the primogem source recommender."""
        self.user_id = user_id
        self.user_data = None

        # Load user data if user_id is provided
        if user_id:
            self._load_user_data(user_id)

        # Define primogem sources with approximate values
        self._define_primogem_sources()

    def set_user_id(self, user_id):
        """Set user ID and load associated data."""
        self.user_id = user_id
        self._load_user_data(user_id)

    def get_primogem_recommendations(self, count=5) -> List[Dict[str, Any]]:
        """Get recommended primogem sources based on user's progress."""
        if not self.user_data:
            raise ValueError("User data must be loaded")

        logger.debug("Calculating primogem recommendations for user %s", self.user_id)
        recommendations = []
        account_info = self.user_data.get("account_info", {})

        # Check for incomplete Spiral Abyss
        abyss_floor = account_info.get("abyss_floor", 0)
        abyss_level = account_info.get("abyss_level", 0)

        if abyss_floor < 12 or (abyss_floor == 12 and abyss_level < 3):
            remaining_stars = (12 - abyss_floor) * 9
            if abyss_floor == 12:
                remaining_stars = (3 - abyss_level) * 3

            primo_value = remaining_stars * 50  # 50 primogems per star

            recommendations.append(
                {
                    "source": "Spiral Abyss",
                    "description": "Clear through Floor %s-%s to Floor 12-3"
                    % (abyss_floor, abyss_level),
                    "primogem_value": primo_value,
                    "difficulty": "High",
                    "recurring": True,
                    "details": "You're missing approximately %s stars worth %s primogems. Refreshes every 2 weeks."
                    % (remaining_stars, primo_value),
                }
            )

        # Check achievement completion
        total_achievements = 1000  # Approximate total achievements
        user_achievements = account_info.get("achievements", 0)

        if user_achievements < total_achievements:
            remaining_achievements = total_achievements - user_achievements
            # Estimate 5 primogems per achievement on average
            primo_value = remaining_achievements * 5

            recommendations.append(
                {
                    "source": "Achievements",
                    "description": "Complete missing achievements (%s remaining)"
                    % remaining_achievements,
                    "primogem_value": primo_value,
                    "difficulty": "Medium",
                    "recurring": False,
                    "details": "Focus on easy achievements like cooking recipes or NPC interactions.",
                }
            )

        # Add exploration recommendations based on known regions
        regions = [
            {
                "name": "Mondstadt",
                "total_chests": 520,
                "primo_per_chest": 2,
                "total_oculi": 65,
                "primo_per_oculus": 2,
            },
            {
                "name": "Liyue",
                "total_chests": 1000,
                "primo_per_chest": 2,
                "total_oculi": 131,
                "primo_per_oculus": 2,
            },
            {
                "name": "Inazuma",
                "total_chests": 950,
                "primo_per_chest": 2,
                "total_oculi": 181,
                "primo_per_oculus": 2,
            },
            {
                "name": "Sumeru",
                "total_chests": 1100,
                "primo_per_chest": 2,
                "total_oculi": 271,
                "primo_per_oculus": 2,
            },
            {
                "name": "Fontaine",
                "total_chests": 800,
                "primo_per_chest": 2,
                "total_oculi": 220,
                "primo_per_oculus": 2,
            },
        ]

        # For demo purposes, suggest some regions with low exploration
        # In a real implementation, we'd use actual user exploration data
        for i, region in enumerate(regions):
            # Assume some regions have lower exploration
            exploration_percentage = min(100, max(40, 80 - (i * 15)))

            if exploration_percentage < 90:
                remaining_percentage = 100 - exploration_percentage
                estimated_chests = int(
                    region["total_chests"] * (remaining_percentage / 100)
                )
                estimated_oculi = int(
                    region["total_oculi"] * (remaining_percentage / 100)
                )

                primo_value = (estimated_chests * region["primo_per_chest"]) + (
                    estimated_oculi * region["primo_per_oculus"]
                )

                # Also account for world quests
                estimated_quests = int(
                    10 * (remaining_percentage / 100)
                )  # Assume 10 quests per region
                quest_primo_value = estimated_quests * 40  # Average 40 primos per quest

                total_primo_value = primo_value + quest_primo_value

                recommendations.append(
                    {
                        "source": "%s Exploration" % region["name"],
                        "description": "Explore more of %s (currently %s%%)"
                        % (region["name"], exploration_percentage),
                        "primogem_value": total_primo_value,
                        "difficulty": "Low",
                        "recurring": False,
                        "details": "Find approximately %s chests and %s oculi. Complete about %s world quests."
                        % (estimated_chests, estimated_oculi, estimated_quests),
                    }
                )

        # Check for Hangout Events
        # In a real implementation, we'd check which hangouts are completed
        # For demo, assume some are incomplete
        incomplete_hangouts = 5
        primo_per_hangout = 60

        recommendations.append(
            {
                "source": "Hangout Events",
                "description": "Complete %s remaining character hangouts"
                % incomplete_hangouts,
                "primogem_value": incomplete_hangouts * primo_per_hangout,
                "difficulty": "Low",
                "recurring": False,
                "details": "Each hangout event has multiple endings, with primogems for each ending.",
            }
        )

        # Check for Story Quests
        # In a real implementation, we'd check which story quests are completed
        # For demo, assume some are incomplete
        incomplete_story_quests = 3
        primo_per_story = 60

        recommendations.append(
            {
                "source": "Story Quests",
                "description": "Complete %s remaining character story quests"
                % incomplete_story_quests,
                "primogem_value": incomplete_story_quests * primo_per_story,
                "difficulty": "Low",
                "recurring": False,
                "details": "Character story quests provide primogems and develop the lore.",
            }
        )

        # Sort recommendations by primogem value
        recommendations.sort(key=lambda x: x["primogem_value"], reverse=True)

        logger.debug(
            "Found %s primogem sources for user %s", len(recommendations), self.user_id
        )

        # Return top recommendations
        return recommendations[:count]

    def _define_primogem_sources(self):
        """Define known primogem sources and their values."""
        self.primogem_sources = {
            "spiral_abyss": {
                "name": "Spiral Abyss",
                "primo_per_star": 50,
                "max_stars": 36,
                "max_value": 1800,
                "recurring": True,
                "frequency": "bi-weekly",
            },
            "daily_commissions": {
                "name": "Daily Commissions",
                "primo_per_day": 60,
                "max_value_monthly": 1800,
                "recurring": True,
                "frequency": "daily",
            },
            "character_trials": {
                "name": "Character Trial Events",
                "primo_per_trial": 20,
                "max_value": 60,
                "recurring": True,
                "frequency": "per banner",
            },
            "web_events": {
                "name": "Web Events",
                "average_value": 80,
                "recurring": True,
                "frequency": "monthly",
            },
            "exploration": {
                "name": "Exploration",
                "sources": [
                    {"name": "Chests", "primo_per_unit": 2, "type": "common"},
                    {"name": "Precious Chests", "primo_per_unit": 5, "type": "rare"},
                    {
                        "name": "Luxurious Chests",
                        "primo_per_unit": 10,
                        "type": "very_rare",
                    },
                    {"name": "Oculi", "primo_per_unit": 2, "type": "collectible"},
                ],
                "recurring": False,
            },
            "quests": {
                "name": "Quests",
                "sources": [
                    {
                        "name": "Archon Quests",
                        "primo_per_quest": 60,
                        "type": "main_story",
                    },
                    {
                        "name": "Story Quests",
                        "primo_per_quest": 60,
                        "type": "character_story",
                    },
                    {
                        "name": "World Quests",
                        "primo_per_quest": 30,
                        "type": "side_quest",
                    },
                    {
                        "name": "Hangout Events",
                        "primo_per_ending": 20,
                        "endings_per_hangout": 5,
                        "type": "character_interaction",
                    },
                ],
                "recurring": False,
            },
            "achievements": {
                "name": "Achievements",
                "sources": [
                    {
                        "name": "Regular Achievements",
                        "primo_per_achievement": 5,
                        "type": "common",
                    },
                    {
                        "name": "Special Achievements",
                        "primo_per_achievement": 10,
                        "type": "rare",
                    },
                    {
                        "name": "Series Completion",
                        "primo_per_series": 20,
                        "type": "meta",
                    },
                ],
                "recurring": False,
            },
        }

    def _load_user_data(self, user_id):
        """Load user data from file."""
        profile_path = utils.get_user_data_file(user_id)

        try:
            self.user_data = utils.load_json_file(profile_path)
            if not self.user_data:
                logger.error("User profile data not found or empty for UID %s", user_id)
                raise FileNotFoundError(
                    "User profile data not found for UID %s" % user_id
                )
            logger.info("Loaded user data for UID %s", user_id)
        except Exception as e:
            logger.error("Error loading user data: %s", e)
            raise


def main():
    """Test the primogem recommender with sample data."""
    # This would normally use real user data
    # For testing, ensure you have at least one user profile

    try:
        # List available user profiles
        user_profiles = [
            f for f in os.listdir(config.USER_DATA_PATH) if f.endswith("_profile.json")
        ]

        if not user_profiles:
            logger.error("No user profiles found. Please sync a profile first.")
            return

        # Use the first available profile
        user_id = user_profiles[0].split("_")[0]
        logger.info("Testing primogem recommender with user ID %s", user_id)
        recommender = PrimogemRecommender(user_id)

        # Get recommendations
        recommendations = recommender.get_primogem_recommendations()

        # Display recommendations
        logger.info("Top primogem sources for user %s:", user_id)
        for i, rec in enumerate(recommendations, 1):
            logger.info(
                "%s. %s - %s primogems (%s difficulty)",
                i,
                rec["source"],
                rec["primogem_value"],
                rec["difficulty"],
            )
            logger.info("   %s", rec["description"])

    except Exception as e:
        logger.error("Error testing primogem recommender: %s", e)


if __name__ == "__main__":
    main()
