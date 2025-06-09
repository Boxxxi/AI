# GenshinAI - Genshin Impact AI Assistant

GenshinAI is a Discord bot that provides personalized Genshin Impact recommendations by analyzing user profile data and game meta statistics. It uses Anthropic's Claude API to deliver natural language responses to player questions.

## 🚀 Features

- AI-powered Genshin Impact recommendations based on your account
- Character building and pull recommendations based on meta trends
- Primogem acquisition recommendations
- Natural language Q&A system for any Genshin-related questions
- Personalized recommendations for:
  - Character prioritization
  - Weapon/character pulls
  - Missing achievements
  - Undiscovered primogem sources

## 💻 Requirements

- Python 3.9+
- Discord bot token (for the Discord bot interface)
- Claude API key (for the AI advisor)
- Genshin Impact UID (your in-game User ID)

## 🔧 Setup

1. Clone this repository

```bash
git clone https://github.com/yourusername/GenshinAI.git
cd GenshinAI
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set up your `.env` file

```bash
cp .env.example .env  # Create from template
# Edit .env with your API keys and UID
```

4. Initialize metadata

```bash
python init_data.py  # Fetches meta statistics
```

5. Fetch your character data from Enka.Network

```bash
python enka_fetch.py  # Enter your UID when prompted
```

6. Run the bot

```bash
python bot/main.py
```

## 📱 Usage

1. **Manually Test Character Recommendations:**

```bash
python test_recommender.py
```

2. **Commands (Discord):**

- `/sync_profile` - Connect your Genshin Impact account (just need your UID)
- `/advise_characters` - Get personalized character recommendations
- `/find_primos` - Discover primogem sources
- `/ask` - Ask any Genshin-related question

## 📋 Data Sources

- **Enka.Network API**: Character showcase data (no login required, just UID)
- **spiralabyss.org**: Spiral Abyss usage statistics
- **Genshin Impact Wiki**: Character data and guides

## 📊 How It Works

1. We fetch your character showcase data from Enka.Network (only what you've showcased in-game)
2. We combine that with meta data from trusted community sources
3. The recommendation engines analyze gaps and priorities in your account
4. Results are delivered via Discord bot or command line

### Data Collection & Trust Categorization

- **Trusted Sources:**
  - Spiral Abyss usage stats
  - HoYoLAB profile data
  - Wiki tables (e.g., Genshin.fandom)
- **Opinion Sources:**
  - Reddit discussions
  - Community tier lists

### User Profile Integration

- **Method 1:** HoYoLAB login cookies (ltuid, ltoken)
- **Method 2 (limited):** Enka.Network API using UID

### Recommendation Engine Modules

1. **Character Development Priority**
   - Ranks owned but undeveloped characters
   - Sorts using meta usage rate, team synergy gaps, and role needs
   - Outputs top 3-5 characters with reasons

2. **Build Gap Suggestions**
   - Analyzes missing roles/weapons
   - Recommends builds/upgrades for under-equipped characters
   - Suggests characters to aim for (future banners)

3. **Easy Achievements**
   - Compares user achievement % vs total
   - Suggests easy/hidden 5-10 primo tasks
   - Uses scraped lists and heuristics

4. **Primogem Source Discovery**
   - Tracks exploration %, Hangouts, Abyss stars
   - Recommends underexplored regions and quest chains
   - Outputs personalized checklist

## Development

To run the development tools:

```bash
# Format code with Black
black .

# Sort imports
isort --profile black .
```

### Code Formatting

This project uses GitHub Actions for automatic code formatting:

- **Code Formatting**: Automatically formats Python code using Black, sorts imports with isort, removes unused imports with Ruff, and formats JSON and Markdown files on push to main branches.
- **Code Format Check**: Checks code formatting on pull requests without making changes.

Formatting is configured in `pyproject.toml` with the following settings:

- Line length: 88 characters
- Black profile for isort compatibility
- Python 3.8+ compatibility
- Ruff for removing unused imports and fixing blank lines
- pydocstyle for checking docstrings
- pyupgrade for Python syntax upgrades

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality before committing. To set up pre-commit:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Run on all files (optional)
pre-commit run --all-files
```

The pre-commit configuration includes:

- Black for Python formatting
- isort for import sorting
- Ruff for removing unused imports and fixing blank lines
- pydocstyle for checking docstrings
- pyupgrade for Python syntax upgrades
- Trailing whitespace removal
- YAML and JSON validation
- Markdown linting

## 📊 Recommended Stack

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
