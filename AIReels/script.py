"""
AI Reels Generator - Creates educational coding reels for social media.
"""

import os
import random
from typing import Tuple

import ffmpeg
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load environment variables
load_dotenv()

# API Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

def get_coding_practice() -> str:
    """
    Select a random coding practice topic.
    
    Returns:
        str: A coding practice topic
    """
    topics = [
        "Use meaningful variable names",
        "Write modular functions",
        "Avoid deep nesting", 
        "Use list comprehensions",
        "Follow DRY (Don't Repeat Yourself) principle"
    ]
    return random.choice(topics)

def generate_code_examples(topic: str) -> str:
    """
    Generate good vs. bad code examples using Hugging Face's StarCoder.
    
    Args:
        topic (str): The coding practice topic
        
    Returns:
        str: Generated code examples
    """
    API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": f"Generate a bad and a good example of {topic} in Python."}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()["generated_text"]

def generate_voiceover(text: str, output_file: str) -> None:
    """
    Generate AI voice-over using ElevenLabs API.
    
    Args:
        text (str): Text to convert to speech
        output_file (str): Path to save the audio file
    """
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {"Authorization": f"Bearer {os.getenv('ELEVENLABS_API_KEY')}"}
    data = {"text": text, "voice": "en-US"}
    
    response = requests.post(tts_url, headers=headers, json=data)
    with open(output_file, "wb") as f:
        f.write(response.content)

def create_code_image(code: str, output_file: str) -> None:
    """
    Create an image with code examples.
    
    Args:
        code (str): Code to display in the image
        output_file (str): Path to save the image
    """
    img = Image.new('RGB', (800, 600), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((50, 50), code, fill=(255, 255, 255), font=font)
    img.save(output_file)

def create_video(image_path: str, audio_path: str, output_video: str) -> None:
    """
    Create a video by combining image and audio using ffmpeg.
    
    Args:
        image_path (str): Path to the image file
        audio_path (str): Path to the audio file
        output_video (str): Path to save the output video
    """
    input_image = ffmpeg.input(image_path, loop=1, t=10)
    input_audio = ffmpeg.input(audio_path)
    output = ffmpeg.output(
        input_image, 
        input_audio, 
        output_video, 
        vcodec='libx264', 
        acodec='aac', 
        strict='experimental', 
        shortest=None
    )
    ffmpeg.run(output)

def main() -> None:
    """Main function to generate the AI reel."""
    # Get topic and generate examples
    topic = get_coding_practice()
    code_examples = generate_code_examples(topic)
    
    # Save examples to file
    with open("examples.txt", "w") as f:
        f.write(code_examples)
    
    # Create visual and audio elements
    create_code_image(code_examples, "code.png")
    generate_voiceover(f"Today's tip: {topic}. Here's why it matters!", "voice.mp3")
    
    # Create final video
    create_video("code.png", "voice.mp3", "output.mp4")

if __name__ == "__main__":
    main()
