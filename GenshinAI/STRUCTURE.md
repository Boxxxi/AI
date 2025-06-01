# GenshinAI Project Structure

## Directories

- **bot/** - Discord bot implementation
- **data/** - Data storage directories
  - **data/meta/** - Game metadata (character stats, Spiral Abyss usage, etc.)
  - **data/users/** - User profile and showcase data
- **engine/** - Recommendation engines (character, primogem, AI advisor)
- **logs/** - Log files
- **scraper/** - Data scraping modules
- **temp/** - Temporary files from data fetching operations

## Key Files

- **.env** - Environment variables (API keys, tokens, etc.)
- **.env.example** - Example environment variables
- **config.py** - Configuration and constants
- **enka_fetch.py** - Script to fetch character data from Enka.Network
- **init_data.py** - Initialize metadata by scraping from trusted sources
- **requirements.txt** - Python dependencies
- **test_recommender.py** - Test script for the character recommender
- **utils.py** - Utility functions for file handling, logging, etc.

## Configuration

- Environment variables are stored in `.env` (see `.env.example` for reference)
- Constants and mappings are in `config.py`
- Logs are stored in the `logs/` directory
- Data is stored in structured JSON files in `data/` subdirectories

## Usage Flow

1. Set up environment variables in `.env`
2. Initialize meta data with `python init_data.py`
3. Fetch character data with `python enka_fetch.py`
4. Test recommendations with `python test_recommender.py`
5. Start the Discord bot with `python bot/main.py`

## Data Flow

1. User profile data is fetched from Enka.Network
2. Data is processed and saved to `data/users/` directory
3. Recommendation engines combine user data with meta data
4. Results are delivered via CLI, Discord bot, or API responses
