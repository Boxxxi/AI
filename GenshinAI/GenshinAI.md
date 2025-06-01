# Genshin Impact AI Assistant – Project Roadmap

## ✨ Goal

Build a **Discord bot** that reduces Genshin Impact grind by using AI to:

- Scrape trusted public game data
- Integrate user profile data (via HoYoLAB or UID)
- Provide personalized recommendations for:
  - Character prioritization
  - Weapon/character pulls
  - Missing achievements
  - Undiscovered primogem sources

All recommendations will be delivered via chat-based Q&A, powered by AI agents.

---

## ⚙️ Step-by-Step Workflow

### 1. **Data Collection & Trust Categorization**

- **Trusted Sources:**
  - Spiral Abyss usage stats
  - HoYoLAB profile data
  - Wiki tables (e.g., Genshin.fandom)
- **Opinion Sources:**
  - Reddit discussions
  - Community tier lists

- **Tools:** `requests`, `BeautifulSoup`, `genshin.py`, Enka API
- **Approach:** Scrape/parse each data source into JSON with a trust score field

---

### 2. **User Profile Integration**

- **Method 1:** HoYoLAB login cookies (ltuid, ltoken)
- **Method 2 (limited):** Enka.Network API using UID

- **Library:** `genshin.py` (async + HoYoLAB wrapper)
- **Data Points:**
  - Owned characters
  - Levels/ascensions
  - Weapons/artifacts
  - Exploration %
  - Abyss floors/stars
  - Achievements count

---

### 3. **Data Structuring**

- **User Data:**

  ```python
  user_chars = {
    "Zhongli": {"level": 20, "built": False, "role": "Shield"}
  }
  ```

- **Meta Data:**

  ```python
  character_meta = {
    "Zhongli": {"usage_rate": 0.93, "role": "Shield", "source": "AbyssStats"}
  }
  ```

- **Achievements, exploration, quests**: parsed and stored with difficulty/primo value tags

---

### 4. **Recommendation Engine Modules**

#### 4.1 📈 Character Development Priority

- Rank owned but undeveloped characters
- Sort using meta usage rate, team synergy gaps, and role needs
- Output: Top 3-5 characters with reasons

#### 4.2 🕵️ Build Gap Suggestions

- Analyze missing roles/weapons
- Recommend builds/upgrades for under-equipped characters
- Suggest characters to aim for (future banners)

#### 4.3 🌟 Easy Achievements

- Compare user achievement % vs total
- Suggest easy/hidden 5-10 primo tasks
- Use scraped lists and heuristics ("cook a suspicious dish")

#### 4.4 🚀 Primogem Source Discovery

- Exploration %, Hangouts, Abyss stars
- Recommend underexplored regions and quest chains
- Output: checklist with ~4-5 personalized sources

---

### 5. **AI-Powered Q&A Layer**

- **Library:** OpenAI GPT-3.5 / GPT-4 (or HF Transformers + LangChain)
- **Prompt Construction:**
  - Inject structured profile/meta data
  - Ask LLM to answer: "Who should I level next?"
- **LangChain Agents (optional):**
  - Tools like `fetch_profile`, `lookup_meta(char)`
  - Agent decides which tools to call

- **Memory Support:** Multi-turn follow-up context via LangChain conversation memory

---

### 6. **Discord Bot Integration**

- **Library:** `discord.py` (with slash commands)
- **Command Examples:**
  - `/sync_profile`
  - `/advise characters`
  - `/recommend weapons`

- **Format:** Markdown-rich Discord replies
- **Performance:** Cache results, avoid repeated API calls, use cron for regular updates

---

### 7. **Automation + Open Source Setup**

- **Project Structure:**
  - `scraper/` - trusted + opinion source scrapers
  - `engine/` - recommend logic modules
  - `bot/` - Discord bot handlers
  - `data/` - JSON datasets, vector embeddings, etc.

- **Dev Tools:**
  - `pytest`, `flake8`, `black`
  - `.env` for tokens/secrets

- **Open Source Guide:**
  - Clear setup instructions (10-min setup)
  - Data injection options (cookie, UID)
  - GitHub template + issue board

---

## 📊 Recommended Stack Summary

| Purpose                  | Tool/Library             |
|--------------------------|--------------------------|
| User Profile API         | `genshin.py`             |
| Public Showcase          | Enka.Network API         |
| Scraping Static Pages    | `requests` + `bs4`       |
| LLM Agent Framework      | LangChain (optional)     |
| Q&A Model                | GPT-3.5 / HF Transformers|
| Discord Bot              | `discord.py`             |
| Storage                  | JSON / SQLite / TinyDB   |
| Scheduler (optional)     | `APScheduler`            |

---

## 🚀 Final Notes

- Start with your profile + one data source
- Develop and test logic locally first
- Use AI for natural language response formatting
- Incrementally add new questions / modules
- Document the hell out of it for open source adoption

You're building a smart co-traveler for Teyvat — one that plays as hard (and smart) as you do.

**Let the grind be optimized. 😎**
