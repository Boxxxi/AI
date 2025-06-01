"""Discord bot for interacting with GenshinAI services and providing personalized game recommendations."""

import os
import sys

# Add root directory to path for imports
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # noqa: E402

import discord  # noqa: E402
from discord import app_commands  # noqa: E402
from discord.ext import commands  # noqa: E402

import config  # noqa: E402
import utils  # noqa: E402
from engine.ai_advisor import AIAdvisor  # noqa: E402
from engine.character_recommender import CharacterRecommender  # noqa: E402
from engine.primogem_recommender import PrimogemRecommender  # noqa: E402
from scraper.meta import MetaScraper  # noqa: E402
from scraper.profile import ProfileScraper  # noqa: E402

# Set up logger - use just the filename, utils will put it in the logs directory
logger = utils.setup_logger("discord_bot", "discord_bot.log")

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)

# Store user IDs mapped to their Genshin UIDs
user_profiles = {}
# Store AI advisors for each user
ai_advisors = {}


@bot.event
async def on_ready():
    """Event called when bot is ready."""
    logger.info("Logged in as %s (ID: %s)", bot.user, bot.user.id)
    logger.info("------")

    # Sync commands
    try:
        synced = await bot.tree.sync()
        logger.info("Synced %s command(s)", len(synced))
    except Exception as e:
        logger.error("Failed to sync commands: %s", e)


@bot.tree.command(
    name="sync_profile", description="Connect your Genshin Impact account using UID"
)
@app_commands.describe(uid="Your Genshin Impact UID (9-digit number)")
async def sync_profile(interaction: discord.Interaction, uid: str):
    """Sync user profile using Enka.Network API."""
    await interaction.response.defer(ephemeral=True)

    try:
        # Validate UID format (must be 9 digits)
        if not uid.isdigit() or len(uid) != 9:
            await interaction.followup.send(
                "Invalid UID format. UID should be a 9-digit number."
            )
            return

        # Initialize profile scraper with just UID (no cookies needed for Enka)
        scraper = ProfileScraper(uid=uid)

        # Fetch user data from Enka.Network
        await interaction.followup.send(
            "Fetching your Genshin Impact profile data from Enka.Network..."
        )

        try:
            # Fetch showcase data from Enka.Network
            showcase_data = await scraper.fetch_showcase_data()

            # Get profile info
            player_info = showcase_data.get("player_info", {})
            nickname = player_info.get("nickname", "Traveler")
            level = player_info.get("level", 0)
            character_count = len(player_info.get("showcase_characters", []))

            # Store the UID for this Discord user
            user_profiles[interaction.user.id] = uid

            # Create AI advisor for this user
            ai_advisors[interaction.user.id] = AIAdvisor(uid)

            # Send confirmation
            await interaction.followup.send(
                "✅ Profile synced successfully!\n"
                f"Loaded data for {nickname} (AR{level})\n"
                f"Found {character_count} characters in your showcase."
            )

        except Exception as e:
            logger.error("Error fetching Enka data: %s", e)
            await interaction.followup.send(
                f"❌ Error fetching profile: {str(e)}\n"
                "Please check your UID and make sure you have characters in your in-game showcase."
            )

    except Exception as e:
        logger.error("Error in sync_profile command: %s", e)
        await interaction.followup.send(f"❌ An error occurred: {str(e)}")


@bot.tree.command(name="advise_characters", description="Get character building advice")
async def advise_characters(interaction: discord.Interaction):
    """Get character building recommendations."""
    await interaction.response.defer()

    try:
        # Check if user has synced profile
        if interaction.user.id not in user_profiles:
            await interaction.followup.send(
                "⚠️ Please sync your profile first using `/sync_profile`."
            )
            return

        uid = user_profiles[interaction.user.id]
        logger.info(
            "Generating character advice for user %s (UID: %s)",
            interaction.user.id,
            uid,
        )

        # Get character recommendations
        recommender = CharacterRecommender(uid)
        build_priority = recommender.get_build_priority(count=5)
        pull_recommendations = recommender.get_pull_recommendations(count=3)

        # Format response
        embed = discord.Embed(
            title="Character Building Recommendations",
            description="Here are your personalized character recommendations based on meta and current roster.",
            color=discord.Color.blue(),
        )

        # Add build priority section
        priority_text = ""
        for i, char in enumerate(build_priority):
            reasons = ", ".join(char["reasons"])
            priority_text += "{}. **{}** (Level {})\n".format(
                i + 1,
                char["name"],
                char["current_level"],
            )
            priority_text += "   Score: {:.2f} | {}\n\n".format(
                char["priority_score"],
                reasons,
            )

        embed.add_field(
            name="🔨 Build Priority",
            value=priority_text if priority_text else "No recommendations available.",
            inline=False,
        )

        # Add pull recommendations section
        pull_text = ""
        for i, char in enumerate(pull_recommendations):
            reasons = ", ".join(char["reasons"])
            pull_text += "{}. **{}** ({} {})\n".format(
                i + 1,
                char["name"],
                char["element"],
                char["weapon_type"],
            )
            pull_text += "   Score: {:.2f} | {}\n\n".format(
                char["recommendation_score"],
                reasons,
            )

        embed.add_field(
            name="🎯 Pull Recommendations",
            value=pull_text if pull_text else "No recommendations available.",
            inline=False,
        )

        embed.set_footer(
            text="Based on Spiral Abyss usage rates and your current roster"
        )

        await interaction.followup.send(embed=embed)

    except Exception as e:
        logger.error("Error in advise_characters command: %s", e)
        await interaction.followup.send("❌ An error occurred: %s" % str(e))


@bot.tree.command(name="find_primos", description="Discover primogem sources")
async def find_primos(interaction: discord.Interaction):
    """Find primogem sources."""
    await interaction.response.defer()

    try:
        # Check if user has synced profile
        if interaction.user.id not in user_profiles:
            await interaction.followup.send(
                "⚠️ Please sync your profile first using `/sync_profile`."
            )
            return

        uid = user_profiles[interaction.user.id]
        logger.info(
            "Finding primogem sources for user %s (UID: %s)", interaction.user.id, uid
        )

        # Get primogem recommendations
        recommender = PrimogemRecommender(uid)
        primogem_recommendations = recommender.get_primogem_recommendations(count=5)

        # Calculate total value
        total_value = sum(rec["primogem_value"] for rec in primogem_recommendations)
        wish_count = total_value // 160

        # Format response
        embed = discord.Embed(
            title="Primogem Source Recommendations",
            description="Found **%s** primogems (approx. **%s** wishes) you could get from these sources:"
            % (total_value, wish_count),
            color=discord.Color.gold(),
        )

        # Add recommendations
        for i, rec in enumerate(primogem_recommendations):
            name = "{}. {} - {} primos".format(
                i + 1, rec["source"], rec["primogem_value"]
            )
            value = "%s\n" % rec["description"]
            value += "Difficulty: {} | {}".format(rec["difficulty"], rec["details"])

            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text="💎 Happy primogem hunting!")

        await interaction.followup.send(embed=embed)

    except Exception as e:
        logger.error("Error in find_primos command: %s", e)
        await interaction.followup.send("❌ An error occurred: %s" % str(e))


@bot.tree.command(name="ask", description="Ask GenshinAI a question about your account")
@app_commands.describe(question="Your question about your Genshin Impact account")
async def ask(interaction: discord.Interaction, question: str):
    """Ask AI assistant a question."""
    await interaction.response.defer()

    try:
        # Check if user has synced profile
        if interaction.user.id not in user_profiles:
            await interaction.followup.send(
                "⚠️ Please sync your profile first using `/sync_profile`."
            )
            return

        uid = user_profiles[interaction.user.id]
        logger.info(
            "Processing question from user %s (UID: %s): %s",
            interaction.user.id,
            uid,
            question,
        )

        # Check if AI advisor exists for this user
        if interaction.user.id not in ai_advisors:
            ai_advisors[interaction.user.id] = AIAdvisor(uid)

        advisor = ai_advisors[interaction.user.id]

        # Get AI response
        response = await advisor.get_answer(question)

        # Send response
        await interaction.followup.send(f"**Your question:** {question}\n\n{response}")

    except Exception as e:
        logger.error("Error in ask command: %s", e)
        await interaction.followup.send("❌ An error occurred: %s" % str(e))


@bot.tree.command(name="update_meta", description="Update meta data (admin only)")
async def update_meta(interaction: discord.Interaction):
    """Update meta data from sources."""
    await interaction.response.defer()

    # Check if user is admin (you might want to implement proper permission checking)
    # For now, we'll use a simple check
    if interaction.user.id != interaction.guild.owner_id:
        await interaction.followup.send("⚠️ This command is for administrators only.")
        return

    try:
        logger.info("Admin %s requested meta data update", interaction.user.id)

        # Initialize meta scraper
        scraper = MetaScraper()

        # Fetch Spiral Abyss stats
        await interaction.followup.send("Fetching Spiral Abyss usage statistics...")
        abyss_stats = await scraper.fetch_spiral_abyss_stats()

        # Fetch character data
        await interaction.followup.send("Fetching character data from Wiki...")
        char_data = await scraper.fetch_character_data()

        # Send confirmation
        await interaction.followup.send(
            "✅ Meta data updated successfully!\n"
            "Fetched usage stats for %s characters and "
            "detailed data for %s characters."
            % (len(abyss_stats["character_usage"]), len(char_data["characters"]))
        )

    except Exception as e:
        logger.error("Error updating meta data: %s", e)
        await interaction.followup.send("❌ An error occurred: %s" % str(e))


@bot.tree.command(name="help", description="Show available commands")
async def help_command(interaction: discord.Interaction):
    """Show help message with available commands."""
    await interaction.response.defer()

    try:
        # Create embed
        embed = discord.Embed(
            title="GenshinAI Bot Help",
            description="AI-powered Discord bot for personalized Genshin Impact recommendations",
            color=discord.Color.teal(),
        )

        # Command list
        commands = [
            {
                "name": "/sync_profile",
                "description": "Connect your Genshin Impact account using UID",
                "usage": "/sync_profile uid:<your-uid>",
            },
            {
                "name": "/advise_characters",
                "description": "Get personalized character building recommendations",
                "usage": "/advise_characters",
            },
            {
                "name": "/find_primos",
                "description": "Discover primogem sources you haven't collected yet",
                "usage": "/find_primos",
            },
            {
                "name": "/ask",
                "description": "Ask the AI assistant a question about your account",
                "usage": "/ask question:<your-question>",
            },
        ]

        # Add fields for each command
        for cmd in commands:
            embed.add_field(
                name=cmd["name"],
                value=f"{cmd['description']}\n**Usage:** `{cmd['usage']}`",
                inline=False,
            )

        # Add note about Enka.Network
        embed.add_field(
            name="📝 Note about character showcase",
            value="To get the most out of GenshinAI, make sure to set up your in-game character showcase with your favorite or most-used characters before using `/sync_profile`.",
            inline=False,
        )

        # Add footer
        embed.set_footer(text="GenshinAI - Powered by Enka.Network data")

        await interaction.followup.send(embed=embed)

    except Exception as e:
        logger.error("Error in help command: %s", e)
        await interaction.followup.send(f"❌ An error occurred: {str(e)}")


def main():
    """Run the Discord bot."""
    logger.info("Starting GenshinAI Discord bot")
    bot.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
