"""Scraper module for collecting Genshin Impact meta data from trusted external sources."""

import asyncio
import os
import sys
from datetime import datetime

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aiohttp
from bs4 import BeautifulSoup

import config
import utils

# Get logger
logger = utils.setup_logger("meta_scraper")


class MetaScraper:
    """Scraper for collecting Genshin Impact meta data from trusted external sources.

    This class fetches and processes game metadata from various trusted sources like:
    - spiralabyss.org for character usage statistics
    - Genshin Impact Wiki for character details and attributes

    The scraped data is processed into structured formats and stored for use
    by the recommendation engines. Each data source is assigned a trust score
    that indicates the reliability of the information.
    """

    def __init__(self):
        """Initialize the meta data scraper."""
        self.data = {}
        self.last_updated = {}

    async def fetch_spiral_abyss_stats(self):
        """Fetch Spiral Abyss usage statistics from spiralabyss.org."""
        url = config.TRUSTED_SOURCES["spiral_abyss_stats"]["url"]
        trust_score = config.TRUSTED_SOURCES["spiral_abyss_stats"]["trust_score"]

        logger.info("Fetching Spiral Abyss stats from %s", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # Extract abyss cycle information
                    cycle_info = soup.select_one(".spiral-cycle")
                    cycle_text = (
                        cycle_info.get_text() if cycle_info else "Unknown Cycle"
                    )

                    # Extract character usage statistics
                    usage_stats = []
                    char_cards = soup.select(".character-card")

                    for card in char_cards:
                        # Extract character name
                        name_elem = card.select_one(".character-name")
                        name = name_elem.get_text().strip() if name_elem else "Unknown"

                        # Extract usage rate
                        usage_elem = card.select_one(".usage-rate")
                        usage_rate = (
                            float(usage_elem.get_text().strip().replace("%", "")) / 100
                            if usage_elem
                            else 0
                        )

                        # Extract star rating
                        star_container = card.select_one(".star-container")
                        rarity = (
                            len(star_container.select(".star")) if star_container else 0
                        )

                        # Extract element
                        element_class = None
                        for cls in card.get("class", []):
                            if cls.startswith("element-"):
                                element_class = cls.replace("element-", "")
                                break

                        # Extract character image URL
                        img_elem = card.select_one("img")
                        img_url = img_elem.get("src") if img_elem else None

                        usage_stats.append(
                            {
                                "name": name,
                                "usage_rate": usage_rate,
                                "rarity": rarity,
                                "element": element_class,
                                "image_url": img_url,
                            }
                        )

                    # Sort by usage rate
                    usage_stats.sort(key=lambda x: x["usage_rate"], reverse=True)

                    # Prepare metadata
                    abyss_data = {
                        "source": "spiralabyss.org",
                        "trust_score": trust_score,
                        "cycle": cycle_text,
                        "fetch_date": datetime.now().isoformat(),
                        "character_usage": usage_stats,
                    }

                    # Save data
                    self.data["spiral_abyss_stats"] = abyss_data
                    self.last_updated["spiral_abyss_stats"] = datetime.now().isoformat()
                    self._save_meta_data("spiral_abyss_stats", abyss_data)

                    logger.info(
                        "Retrieved usage stats for %s characters", len(usage_stats)
                    )
                    return abyss_data
                else:
                    error_msg = "Failed to fetch Spiral Abyss stats: %s"
                    logger.error(error_msg, response.status)
                    raise Exception(error_msg % response.status)

    async def fetch_character_data(self):
        """Fetch comprehensive character data from Genshin Impact Wiki."""
        base_url = config.TRUSTED_SOURCES["genshin_wiki"]["url"]
        trust_score = config.TRUSTED_SOURCES["genshin_wiki"]["trust_score"]

        # First, fetch the list of playable characters
        character_list_url = f"{base_url}Category:Playable_Characters"
        logger.info("Fetching character list from %s", character_list_url)

        async with aiohttp.ClientSession() as session:
            character_data = {}

            # Fetch character list page
            async with session.get(character_list_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # Extract character links
                    char_links = []
                    char_category = soup.select(".category-page__member-link")

                    for link in char_category:
                        char_name = link.get_text().strip()
                        char_url = link.get("href")

                        # Skip non-character pages
                        if "Traveler" in char_name and char_name != "Traveler":
                            continue  # Skip Traveler element variants as they'll be handled specially

                        char_links.append({"name": char_name, "url": char_url})

                    logger.info("Found %s characters to process", len(char_links))

                    # Process characters in batches to avoid rate limiting
                    batch_size = 5
                    for i in range(0, len(char_links), batch_size):
                        batch = char_links[i : i + batch_size]
                        logger.debug(
                            "Processing batch %s/%s",
                            i // batch_size + 1,
                            (len(char_links) - 1) // batch_size + 1,
                        )
                        tasks = [
                            self._fetch_character_details(
                                session, char["name"], char["url"]
                            )
                            for char in batch
                        ]
                        results = await asyncio.gather(*tasks, return_exceptions=True)

                        for j, result in enumerate(results):
                            if isinstance(result, Exception):
                                logger.error(
                                    "Error fetching %s: %s", batch[j]["name"], result
                                )
                            else:
                                character_data[batch[j]["name"]] = result

                        # Small delay to avoid rate limiting
                        await asyncio.sleep(1)

                    # Prepare metadata
                    wiki_data = {
                        "source": "Genshin Impact Wiki",
                        "trust_score": trust_score,
                        "fetch_date": datetime.now().isoformat(),
                        "characters": character_data,
                    }

                    # Save data
                    self.data["character_data"] = wiki_data
                    self.last_updated["character_data"] = datetime.now().isoformat()
                    self._save_meta_data("character_data", wiki_data)

                    logger.info(
                        "Successfully retrieved data for %s characters",
                        len(character_data),
                    )
                    return wiki_data
                else:
                    error_msg = "Failed to fetch character list: %s"
                    logger.error(error_msg, response.status)
                    raise Exception(error_msg % response.status)

    async def _fetch_character_details(self, session, char_name, char_url):
        """Fetch details for a specific character from the wiki."""
        full_url = f"https://genshin-impact.fandom.com{char_url}"
        logger.debug("Fetching details for %s from %s", char_name, full_url)

        async with session.get(full_url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Extract basic info
                char_data = {
                    "name": char_name,
                    "url": full_url,
                    "rarity": 0,
                    "element": "Unknown",
                    "weapon_type": "Unknown",
                    "region": "Unknown",
                    "description": "",
                    "released": True,
                    "abilities": {},
                }

                # Extract infobox data
                infobox = soup.select_one(".portable-infobox")
                if infobox:
                    # Get rarity
                    rarity_stars = infobox.select(".pi-item .item_rarity")
                    char_data["rarity"] = len(rarity_stars) if rarity_stars else 0

                    # Get element
                    element_img = infobox.select_one('[data-source="element"] img')
                    if element_img and element_img.get("alt"):
                        char_data["element"] = element_img.get("alt").replace(
                            " Element", ""
                        )

                    # Get weapon type
                    weapon_div = infobox.select_one('[data-source="weapon"]')
                    if weapon_div:
                        weapon_text = weapon_div.get_text().strip()
                        char_data["weapon_type"] = weapon_text

                    # Get region
                    region_div = infobox.select_one('[data-source="region"]')
                    if region_div:
                        region_text = region_div.get_text().strip()
                        char_data["region"] = region_text

                    # Get description
                    desc_div = infobox.select_one(".pi-data-value.pi-font")
                    if desc_div:
                        char_data["description"] = desc_div.get_text().strip()

                # Extract ability information
                talent_section = soup.select_one("#Combat_Talents")
                if talent_section:
                    talents_table = talent_section.find_parent("h2").find_next("table")
                    if talents_table:
                        talents = talents_table.select("tr")[1:]  # Skip header row

                        for talent in talents:
                            cells = talent.select("td")
                            if len(cells) >= 2:
                                talent_name = cells[0].get_text().strip()
                                talent_desc = cells[1].get_text().strip()

                                char_data["abilities"][talent_name] = talent_desc

                return char_data
            else:
                error_msg = "Failed to fetch %s details: %s"
                logger.error(error_msg, char_name, response.status)
                raise Exception(error_msg % (char_name, response.status))

    def _save_meta_data(self, data_type, data):
        """Save meta data to file."""
        file_path = utils.get_meta_data_file(data_type)
        if utils.save_json_file(data, file_path):
            logger.info("Saved %s meta data", data_type)
        else:
            logger.error("Failed to save %s meta data", data_type)


async def main():
    """Test function to fetch meta data."""
    scraper = MetaScraper()

    logger.info("Fetching Spiral Abyss usage statistics...")
    try:
        abyss_stats = await scraper.fetch_spiral_abyss_stats()
        logger.info(
            "Retrieved usage stats for %s characters",
            len(abyss_stats["character_usage"]),
        )
        logger.info("Top 5 most used characters:")
        for i, char in enumerate(abyss_stats["character_usage"][:5]):
            logger.info(
                "%s. %s - %.2f%%", i + 1, char["name"], char["usage_rate"] * 100
            )
    except Exception as e:
        logger.error("Error fetching Spiral Abyss stats: %s", e)

    logger.info("Fetching character data from Wiki...")
    try:
        # For testing, limit to just a few characters by commenting out the actual function
        # and replacing with a mock that processes fewer characters
        char_data = await scraper.fetch_character_data()
        logger.info("Retrieved data for %s characters", len(char_data["characters"]))
    except Exception as e:
        logger.error("Error fetching character data: %s", e)


if __name__ == "__main__":
    asyncio.run(main())
