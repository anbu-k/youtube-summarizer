import openai
import os
from dotenv import load_dotenv  

load_dotenv()

def transcribe_audio(file_path):
    """Transcribes audio using OpenAI's Whisper model."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"DEBUG: API Key in Flask = {api_key}")  # Debugging line

    if not api_key:
        raise ValueError("Missing OpenAI API key. Make sure .env file is set.")

    client = openai.OpenAI(api_key=api_key)

    with open(file_path, "rb") as file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=file
        )
    
    return response.text
