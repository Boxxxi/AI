import os
import sys

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.genshin_bot import main

if __name__ == "__main__":
    print("Starting GenshinAI Discord bot...")
    main()
