"""AI-powered advisor for providing personalized Genshin Impact recommendations and answers."""

import json
import os
import sys
from typing import Any, Dict, List

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx

import config
import utils
from engine.character_recommender import CharacterRecommender
from engine.primogem_recommender import PrimogemRecommender

# Set up logger
logger = utils.setup_logger("ai_advisor")


class AIAdvisor:
    """AI-powered advisor for providing personalized Genshin Impact recommendations and answers.

    This class integrates with AI models to provide contextual, personalized responses to
    questions about Genshin Impact based on the user's profile data. It leverages specialized
    recommender engines to generate character building suggestions and primogem acquisition advice.
    """

    def __init__(self, user_id=None):
        """Initialize the AI advisor for Genshin Impact recommendations."""
        self.user_id = user_id
        self.user_data = None
        self.character_recommender = None
        self.primogem_recommender = None
        self.conversation_history = []

        # Load user data and initialize recommenders if user_id is provided
        if user_id:
            self._load_user_data(user_id)
            self._initialize_recommenders(user_id)

    def set_user_id(self, user_id):
        """Set user ID and load associated data."""
        self.user_id = user_id
        self._load_user_data(user_id)
        self._initialize_recommenders(user_id)

    async def get_answer(self, question: str) -> str:
        """Get AI-generated answer to a Genshin Impact related question."""
        if not self.user_id or not self.user_data:
            return "Please sync your profile first using `/sync_profile`."

        # Prepare context based on the question
        context = self._prepare_context(question)

        # Add question to conversation history
        self.conversation_history.append({"role": "user", "content": question})

        # Get system prompt
        system_prompt = self._get_system_prompt()

        # Prepare the messages for the language model
        messages = [
            {
                "role": "user",
                "content": f"Context information: {json.dumps(context)}\n\nUser question: {question}",
            }
        ]

        # Add conversation history (limited to last 5 exchanges for context length)
        if len(self.conversation_history) > 2:  # Only add if there's meaningful history
            history_context = "Previous conversation:\n"
            for msg in self.conversation_history[-5:]:
                history_context += f"{msg['role']}: {msg['content']}\n"

            messages[0]["content"] = f"{history_context}\n{messages[0]['content']}"

        try:
            # Call Claude API
            logger.info("Sending question to Claude: %s", question)

            # Convert messages to Claude format
            claude_messages = []
            for msg in messages:
                if msg["role"] == "user":
                    claude_messages.append({"role": "user", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    claude_messages.append(
                        {"role": "assistant", "content": msg["content"]}
                    )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": config.CLAUDE_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": config.CLAUDE_MODEL,
                        "system": system_prompt,
                        "messages": claude_messages,
                        "max_tokens": 1000,
                        "temperature": 0.7,
                    },
                )

                response_data = response.json()
                answer = response_data["content"][0]["text"]
                logger.debug(
                    "Received response from Claude, length: %s characters", len(answer)
                )

            # Add response to conversation history
            self.conversation_history.append({"role": "assistant", "content": answer})

            return answer

        except Exception as e:
            logger.error("Error getting AI response: %s", e)
            return (
                f"Sorry, I encountered an error while generating a response: {str(e)}"
            )

    def _prepare_context(self, question: str) -> Dict[str, Any]:
        """Prepare relevant context based on the question."""
        context = {
            "user_info": {
                "nickname": self.user_data.get("account_info", {}).get(
                    "nickname", "Traveler"
                ),
                "adventure_rank": self.user_data.get("account_info", {}).get(
                    "level", 1
                ),
                "character_count": len(self.user_data.get("characters", {})),
            }
        }

        # Add character recommendations if the question is about characters
        if any(
            keyword in question.lower()
            for keyword in [
                "character",
                "build",
                "level",
                "who",
                "which",
                "team",
                "comp",
            ]
        ):
            if self.character_recommender:
                try:
                    context[
                        "build_recommendations"
                    ] = self.character_recommender.get_build_priority(count=5)
                    context[
                        "pull_recommendations"
                    ] = self.character_recommender.get_pull_recommendations(count=3)
                except Exception as e:
                    logger.error("Error getting character recommendations: %s", e)
                    context["recommender_error"] = str(e)

        # Add primogem recommendations if the question is about primogems
        if any(
            keyword in question.lower()
            for keyword in ["primo", "gem", "wish", "pull", "roll", "summon", "gacha"]
        ):
            if self.primogem_recommender:
                try:
                    context[
                        "primogem_recommendations"
                    ] = self.primogem_recommender.get_primogem_recommendations(count=5)
                except Exception as e:
                    logger.error("Error getting primogem recommendations: %s", e)
                    context["recommender_error"] = str(e)

        # Add character details if asking about specific characters
        character_names = self._extract_character_names(question)
        if character_names and "characters" in self.user_data:
            context["character_details"] = {}
            for name in character_names:
                if name in self.user_data["characters"]:
                    context["character_details"][name] = self.user_data["characters"][
                        name
                    ]

        return context

    def _extract_character_names(self, text: str) -> List[str]:
        """Extract character names from text."""
        # Simple extraction based on character list
        # A more sophisticated implementation would use NER or fuzzy matching
        found_characters = []

        if not self.user_data or "characters" not in self.user_data:
            return found_characters

        # Normalize text
        text_lower = text.lower()

        for char_name in self.user_data["characters"].keys():
            if char_name.lower() in text_lower:
                found_characters.append(char_name)

        return found_characters

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the language model."""
        return """
        You are GenshinAI, an AI assistant specialized in providing personalized Genshin Impact advice.

        You have access to the user's HoYoLAB profile data and can provide recommendations on:
        1. Character building priorities
        2. Character pull recommendations
        3. Primogem source discovery
        4. Team compositions
        5. General Genshin Impact advice

        User's profile data and recommendations will be provided in the context. Use this information
        to give personalized advice. If specific information is not available, you can still provide
        general advice based on the game meta.

        Keep responses helpful, accurate, and concise. Focus on actionable advice that helps the user
        progress efficiently in Genshin Impact.

        Format your responses in a clean, easy-to-read manner. Use Markdown formatting when appropriate.
        """

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

    def _initialize_recommenders(self, user_id):
        """Initialize recommendation engines."""
        self.character_recommender = CharacterRecommender(user_id)
        self.primogem_recommender = PrimogemRecommender(user_id)
        logger.info("Initialized recommenders for UID %s", user_id)


async def main():
    """Test the AI advisor with sample questions."""
    import asyncio

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
        logger.info("Testing AI advisor with user ID %s", user_id)
        advisor = AIAdvisor(user_id)

        # Sample questions to test
        questions = [
            "Which characters should I prioritize building?",
            "What's the best way for me to get more primogems?",
            "Should I pull for new characters or weapons?",
            "What team compositions would work well with my characters?",
            "How can I improve my Spiral Abyss performance?",
        ]

        for question in questions:
            logger.info("Question: %s", question)
            answer = await advisor.get_answer(question)
            logger.info("Answer length: %s characters", len(answer))

            # Short delay between questions
            await asyncio.sleep(1)

    except Exception as e:
        logger.error("Error testing AI advisor: %s", e)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
