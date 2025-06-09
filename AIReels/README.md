# AI Reels Generator

A Python application that automatically generates educational coding reels for social media platforms. The application creates short videos with code examples, voice-overs, and visual elements to explain coding best practices.

## Features

- Generates coding practice examples using Hugging Face's StarCoder model
- Creates visual code examples with custom formatting
- Generates AI voice-overs using ElevenLabs API
- Combines audio and visual elements into a video using ffmpeg
- (Optional) Posts directly to Instagram

## Prerequisites

- Python 3.9+
- ffmpeg installed on your system
- API keys for:
  - Hugging Face
  - ElevenLabs
  - (Optional) Meta/Instagram

## Installation

1. Install system dependencies:
```bash
# For macOS
brew install ffmpeg

# For Ubuntu/Debian
sudo apt-get install ffmpeg
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
HUGGINGFACE_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
INSTAGRAM_ACCOUNT_ID=your_account_id
```

## Usage

Run the script:
```bash
python script.py
```

The script will:
1. Select a random coding practice topic
2. Generate code examples using AI
3. Create a visual representation
4. Generate a voice-over
5. Combine everything into a video
6. (Optional) Post to Instagram

## Output

The script generates:
- `examples.txt`: Generated code examples
- `code.png`: Visual representation of the code
- `voice.mp3`: Generated voice-over
- `output.mp4`: Final video

## Contributing

Feel free to submit issues and enhancement requests!
