import random
import os
from PIL import Image, ImageDraw, ImageFont
import ffmpeg
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Hugging Face API key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Meta API credentials (for Instagram posting)
# META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

# 1. Select a coding practice topic
def get_coding_practice():
    topics = [
        "Use meaningful variable names",
        "Write modular functions",
        "Avoid deep nesting", 
        "Use list comprehensions",
        "Follow DRY (Don't Repeat Yourself) principle"
    ]
    return random.choice(topics)

# 2. Generate good vs. bad code examples using Hugging Face
def generate_code_examples(topic):
    API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": f"Generate a bad and a good example of {topic} in Python."}
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.json()["generated_text"])
    return response.json()["generated_text"]

# 3. Create AI voice-over
def generate_voiceover(text, output_file):
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech"  # Example API
    headers = {"Authorization": f"Bearer {os.getenv('ELEVENLABS_API_KEY')}"}
    data = {"text": text, "voice": "en-US"}
    response = requests.post(tts_url, headers=headers, json=data)
    with open(output_file, "wb") as f:
        f.write(response.content)

# 4. Create image with code examples
def create_code_image(code, output_file):
    img = Image.new('RGB', (800, 600), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((50, 50), code, fill=(255, 255, 255), font=font)
    img.save(output_file)

# 5. Create video using ffmpeg-python
def create_video(image_path, audio_path, output_video):
    input_image = ffmpeg.input(image_path, loop=1, t=10)
    input_audio = ffmpeg.input(audio_path)
    output = ffmpeg.output(input_image, input_audio, output_video, vcodec='libx264', acodec='aac', strict='experimental', shortest=None)
    ffmpeg.run(output)

# 6. Upload video to Instagram
# def post_to_instagram(video_path, caption):
#     upload_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
#     data = {"video_url": video_path, "caption": caption, "access_token": META_ACCESS_TOKEN}
#     response = requests.post(upload_url, data=data)
#     print(response.json())

if __name__ == "__main__":
    topic = get_coding_practice()
    code_examples = generate_code_examples(topic)
    
    with open("examples.txt", "w") as f:
        f.write(code_examples)
    
    create_code_image(code_examples, "code.png")
    generate_voiceover(f"Today's tip: {topic}. Here's why it matters!", "voice.mp3")
    create_video("code.png", "voice.mp3", "output.mp4")
    # post_to_instagram("output.mp4", f"Today's coding tip: {topic} \n\n #coding #python")
