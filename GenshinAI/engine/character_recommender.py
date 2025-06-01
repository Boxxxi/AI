"""Engine for providing personalized character recommendations based on user data and meta statistics."""

import os
import sys
from typing import Any, Dict, List

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import utils

# Get logger
logger = utils.setup_logger("character_recommender")


class CharacterRecommender:
    """Recommendation engine for Genshin Impact characters based on meta data and user roster.

    This class analyzes a user's character collection, meta statistics from Spiral Abyss,
    and other game data to provide personalized recommendations for:
    - Which characters to prioritize building
    - Which characters to pull for in future banners
    - Team compositions that maximize synergy

    It uses various scoring algorithms to evaluate characters based on their
    meta relevance, current build status, team synergies, and role coverage.
    """

    def __init__(self, user_id=None):
        """Initialize the character recommender."""
        self.user_id = user_id
        self.user_data = None
        self.abyss_stats = None
        self.character_data = None

        # Load meta data
        self._load_meta_data()

        # Load user data if user_id is provided
        if user_id:
            self._load_user_data(user_id)

    def set_user_id(self, user_id):
        """Set user ID and load associated data."""
        self.user_id = user_id
        self._load_user_data(user_id)

    def get_build_priority(self, count=5) -> List[Dict[str, Any]]:
        """Get recommended character build priorities."""
        if not self.user_data or not self.abyss_stats:
            raise ValueError("User data and meta data must be loaded")

        logger.debug("Calculating build priorities for user %s", self.user_id)
        recommendations = []

        # Get owned characters
        owned_chars = self.user_data.get("characters", {})

        # Calculate priority scores for each owned character
        for char_name, char_data in owned_chars.items():
            # Skip fully-built characters (lvl 90, good artifacts, etc.)
            if self._is_fully_built(char_data):
                continue

            # Calculate priority score based on several factors
            meta_score = self._calculate_meta_score(char_name)
            build_progress = self._calculate_build_progress(char_data)
            team_value = self._calculate_team_value(char_name, owned_chars)

            # Higher meta score is better, lower build progress means more room for improvement
            priority_score = (
                (meta_score * 0.6) + ((1 - build_progress) * 0.2) + (team_value * 0.2)
            )

            # Determine reasons for recommendation
            reasons = []
            if meta_score > 0.7:
                reasons.append("Strong in current meta")
            if build_progress < 0.3:
                reasons.append("Significant improvement potential")
            if team_value > 0.7:
                reasons.append("Synergizes well with your built characters")

            recommendations.append(
                {
                    "name": char_name,
                    "priority_score": priority_score,
                    "meta_score": meta_score,
                    "build_progress": build_progress,
                    "team_value": team_value,
                    "reasons": reasons,
                    "rarity": char_data.get("rarity", 4),
                    "element": char_data.get("element", "Unknown"),
                    "current_level": char_data.get("level", 1),
                }
            )

        # Sort by priority score and return top recommendations
        recommendations.sort(key=lambda x: x["priority_score"], reverse=True)
        return recommendations[:count]

    def get_pull_recommendations(self, count=3) -> List[Dict[str, Any]]:
        """Get recommended characters to pull based on user's account needs."""
        if not self.user_data or not self.abyss_stats or not self.character_data:
            raise ValueError("User data and meta data must be loaded")

        logger.debug("Calculating pull recommendations for user %s", self.user_id)
        recommendations = []

        # Get owned characters
        owned_chars = set(self.user_data.get("characters", {}).keys())
        all_chars = set(self.character_data.get("characters", {}).keys())

        # Find unowned characters
        unowned = all_chars - owned_chars
        logger.debug(
            "User has %s characters, missing %s characters",
            len(owned_chars),
            len(unowned),
        )

        # Calculate recommendation score for each unowned character
        for char_name in unowned:
            if char_name not in self.character_data.get("characters", {}):
                continue

            char_data = self.character_data["characters"][char_name]

            # Skip unreleased characters
            if not char_data.get("released", True):
                continue

            meta_score = self._calculate_meta_score(char_name)
            team_value = self._calculate_team_value(
                char_name, self.user_data.get("characters", {})
            )
            role_need = self._calculate_role_need(char_name)

            # Calculate overall recommendation score
            rec_score = (meta_score * 0.4) + (team_value * 0.3) + (role_need * 0.3)

            # Determine reasons for recommendation
            reasons = []
            if meta_score > 0.7:
                reasons.append("Strong in current meta")
            if team_value > 0.7:
                reasons.append("Synergizes well with your built characters")
            if role_need > 0.7:
                reasons.append("Fills a missing role in your roster")

            recommendations.append(
                {
                    "name": char_name,
                    "recommendation_score": rec_score,
                    "meta_score": meta_score,
                    "team_value": team_value,
                    "role_need": role_need,
                    "reasons": reasons,
                    "rarity": char_data.get("rarity", 4),
                    "element": char_data.get("element", "Unknown"),
                    "weapon_type": char_data.get("weapon_type", "Unknown"),
                }
            )

        # Sort by recommendation score and return top recommendations
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return recommendations[:count]

    def _is_fully_built(self, char_data) -> bool:
        """Determine if a character is fully built."""
        # Simple heuristic for "fully built" - level 80+ and high friendship
        if char_data.get("level", 0) >= 80 and char_data.get("friendship", 0) >= 7:
            return True
        return False

    def _calculate_meta_score(self, char_name) -> float:
        """Calculate meta score for a character based on Spiral Abyss usage."""
        # Default score for characters not found in abyss stats
        default_score = 0.5

        if not self.abyss_stats or "character_usage" not in self.abyss_stats:
            return default_score

        # Find character in abyss stats
        for char in self.abyss_stats.get("character_usage", []):
            if char["name"].lower() == char_name.lower():
                # Use usage rate as meta score
                return char["usage_rate"]

        # Character not found in abyss stats
        return default_score

    def _calculate_build_progress(self, char_data) -> float:
        """Calculate how complete a character's build is."""
        # Simple calculation based on level, talents, and constellations
        level_progress = min(1.0, char_data.get("level", 1) / 90)
        talent_progress = 0.5  # Placeholder, would calculate from actual talent levels
        const_progress = min(1.0, char_data.get("constellation", 0) / 6)

        # Weighted average
        return (level_progress * 0.5) + (talent_progress * 0.3) + (const_progress * 0.2)

    def _calculate_team_value(self, char_name, owned_chars) -> float:
        """Calculate how valuable a character is in team compositions."""
        # Placeholder implementation
        # A full implementation would check if this character works well with
        # characters the user already has built
        return 0.7

    def recommend_characters(self, count=5):
        """Recommend characters based on user's roster and meta data."""
        if not self.user_data or not self.abyss_stats:
            raise ValueError(
                "User data and meta data must be loaded before making recommendations"
            )

        # Get characters the user doesn't have
        user_chars = set(self.user_data.get("characters", {}).keys())
        all_chars = set(self.abyss_stats.get("character_usage", []))
        missing_chars = all_chars - user_chars

        # Score all missing characters
        char_scores = []
        for char_name in missing_chars:
            score = self._calculate_character_score(char_name)
            char_scores.append((char_name, score))

        # Sort by score and return top N
        char_scores.sort(key=lambda x: x[1], reverse=True)
        return char_scores[:count]

    def recommend_team(self, char_name=None):
        """Recommend a team based on a specific character or user's roster."""
        if not self.user_data or not self.abyss_stats:
            raise ValueError(
                "User data and meta data must be loaded before making recommendations"
            )

        # If character name is provided, recommend a team around that character
        if char_name:
            # Check if character exists in abyss stats
            char_exists = False
            for char in self.abyss_stats.get("character_usage", []):
                if char["name"] == char_name:
                    char_exists = True
                    break

            if not char_exists:
                logger.warning("Character %s not found in meta data", char_name)
                return []

            # Get teams that include this character
            teams = []
            for team in self.abyss_stats.get("teams", []):
                if char_name in team.get("characters", []):
                    teams.append(team)

            # Sort teams by usage count
            teams.sort(key=lambda x: x.get("usage_count", 0), reverse=True)

            # Return top team
            return teams[0] if teams else []

        # If no character is specified, recommend based on user's roster
        else:
            # Placeholder logic, in a real system this would be more sophisticated
            user_chars = list(self.user_data.get("characters", {}).keys())
            if not user_chars:
                return []

            # Find teams that include at least one character the user has
            potential_teams = []
            for team in self.abyss_stats.get("teams", []):
                team_chars = team.get("characters", [])
                common_chars = [char for char in team_chars if char in user_chars]
                if common_chars:
                    potential_teams.append(
                        {
                            "team": team,
                            "common_count": len(common_chars),
                            "common_chars": common_chars,
                        }
                    )

            # Sort by number of common characters, then by usage count
            potential_teams.sort(
                key=lambda x: (x["common_count"], x["team"].get("usage_count", 0)),
                reverse=True,
            )

            # Return top team
            return potential_teams[0]["team"] if potential_teams else []

    def get_character_stats(self, char_name):
        """Get detailed stats and recommendations for a specific character."""
        if not self.abyss_stats:
            raise ValueError("Meta data must be loaded before getting character stats")

        # Find character in abyss stats
        char_data = None
        for char in self.abyss_stats.get("character_usage", []):
            if char["name"] == char_name:
                char_data = char
                break

        if not char_data:
            logger.warning("Character %s not found in meta data", char_name)
            return None

        # Get character details from character data
        char_details = self.character_data.get("characters", {}).get(char_name, {})

        # Combine data
        return {
            "name": char_name,
            "usage_rate": char_data.get("usage_rate", 0),
            "rarity": char_data.get("rarity", 0),
            "element": char_data.get("element", "Unknown"),
            "weapon_type": char_details.get("weapon_type", "Unknown"),
            "region": char_details.get("region", "Unknown"),
            "description": char_details.get("description", ""),
            "abilities": char_details.get("abilities", {}),
            "recommended_teams": self.recommend_team(char_name),
        }

    def user_has_character(self, char_name):
        """Check if the user has a specific character."""
        if not self.user_data:
            raise ValueError(
                "User data must be loaded before checking character ownership"
            )

        return char_name in self.user_data.get("characters", {})

    def get_user_characters(self):
        """Get the list of characters the user has."""
        if not self.user_data:
            raise ValueError("User data must be loaded before getting character list")

        return list(self.user_data.get("characters", {}).keys())

    def _calculate_character_score(self, char_name):
        """Calculate a recommendation score for a character."""
        if not self.abyss_stats:
            return 0

        # Find character in abyss stats
        char_data = None
        for char in self.abyss_stats.get("character_usage", []):
            if char["name"] == char_name:
                char_data = char
                break

        if not char_data:
            return 0

        # Calculate score based on multiple factors:
        # 1. Meta relevance (usage rate in Spiral Abyss)
        meta_score = char_data.get("usage_rate", 0)

        # 2. Role need (how much the user needs this character's role)
        role_score = self._calculate_role_need(char_name)

        # 3. Element diversity (add value if user lacks this element)
        element_score = self._calculate_element_diversity(
            char_data.get("element", "Unknown")
        )

        # Calculate weighted final score
        final_score = meta_score * 0.6 + role_score * 0.3 + element_score * 0.1

        return final_score

    def _calculate_element_diversity(self, element):
        """Calculate how much an element would add to roster diversity."""
        if not self.user_data:
            return 0.5  # Default value if no user data

        # Count elements in user's roster
        element_counts = {}
        for char_name, char_data in self.user_data.get("characters", {}).items():
            char_element = char_data.get("element", "Unknown")
            element_counts[char_element] = element_counts.get(char_element, 0) + 1

        # If user doesn't have any character of this element, score higher
        if element not in element_counts:
            return 1.0
        else:
            # More characters of this element means lower score
            return max(0.1, 1.0 - (element_counts[element] / 5))

    def _calculate_role_need(self, char_name) -> float:
        """Calculate how much a character's role is needed in the roster."""
        # This is a placeholder for role analysis
        # A full implementation would consider character roles (DPS, Support, etc.)
        # and evaluate which roles are lacking in the user's roster

        # For now, return a default value
        return 0.6

    def _load_user_data(self, user_id):
        """Load user data from file."""
        profile_path = utils.get_user_data_file(user_id)

        try:
            self.user_data = utils.load_json_file(profile_path)
            if not self.user_data:
                logger.error("User profile data not found or empty for UID %s", user_id)
                raise FileNotFoundError(
                    f"User profile data not found for UID {user_id}"
                )
            logger.info("Loaded user data for UID %s", user_id)
        except Exception as e:
            logger.error("Error loading user data: %s", e)
            raise

    def _load_meta_data(self):
        """Load meta data from files."""
        abyss_path = utils.get_meta_data_file("spiral_abyss_stats")
        character_path = utils.get_meta_data_file("character_data")

        self.abyss_stats = utils.load_json_file(abyss_path)
        self.character_data = utils.load_json_file(character_path)

        if self.abyss_stats:
            logger.info(
                "Loaded Spiral Abyss stats with %s characters",
                len(self.abyss_stats.get("character_usage", [])),
            )
        else:
            logger.warning("Failed to load Spiral Abyss stats")

        if self.character_data:
            logger.info(
                "Loaded character data with %s characters",
                len(self.character_data.get("characters", {})),
            )
        else:
            logger.warning("Failed to load character data")


def main():
    """Test the character recommender with sample data.

    This function demonstrates the usage of the CharacterRecommender class
    by loading available user profiles and generating recommendations.
    It serves as both a test and an example of how to use the recommender.
    """
    # This would normally use real user data
    # For testing, ensure you have meta data and at least one user profile

    try:
        # List available user profiles
        profile_files = [
            f for f in os.listdir(config.USER_DATA_PATH) if f.endswith("_profile.json")
        ]

        if not profile_files:
            logger.error("No user profiles found. Please sync a profile first.")
            return

        # Use the first available profile
        user_id = profile_files[0].split("_")[0]
        recommender = CharacterRecommender(user_id)

        logger.info(f"Analyzing account data for UID {user_id}...")
        build_recs = recommender.get_build_priority(count=5)

        logger.info("Top 5 Character Build Recommendations:")
        for i, rec in enumerate(build_recs):
            logger.info(f"{i+1}. {rec['name']} (Level {rec['current_level']})")
            logger.info(f"   Priority Score: {rec['priority_score']:.2f}")
            logger.info(f"   Reasons: {', '.join(rec['reasons'])}")

        pull_recs = recommender.get_pull_recommendations(count=3)

        logger.info("Top 3 Character Pull Recommendations:")
        for i, rec in enumerate(pull_recs):
            logger.info(f"{i+1}. {rec['name']} ({rec['element']} {rec['weapon_type']})")
            logger.info(f"   Recommendation Score: {rec['recommendation_score']:.2f}")
            logger.info(f"   Reasons: {', '.join(rec['reasons'])}")

    except Exception as e:
        logger.error(f"Error analyzing character data: {e}")


if __name__ == "__main__":
    main()
