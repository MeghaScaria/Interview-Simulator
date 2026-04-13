import os
import io
import asyncio
import edge_tts
from groq import Groq
from dotenv import load_dotenv

load_dotenv() # Loads the .env file

try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    client = None

def generate_tts(text, speed="+25%"):
    """Converts Text to Speech using Microsoft Edge TTS (fast neural voices)."""
    async def _generate():
        # en-US-AriaNeural is a very professional, clean voice.
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural", rate=speed)
        audio_data = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.extend(chunk["data"])
        return bytes(audio_data)
        
    return asyncio.run(_generate())

def transcribe_audio(audio_bytes, file_name="audio.wav"):
    """Transcribes audio bytes using Groq Whisper API (whisper-large-v3-turbo)."""
    if not client:
        return "Error: Groq API Key not found."
    
    # Whisper accepts specific file formats via tuple (filename, bytes)
    file_tuple = (file_name, audio_bytes)
    transcription = client.audio.transcriptions.create(
      file=file_tuple,
      model="whisper-large-v3-turbo",
      response_format="verbose_json",
    )
    return transcription.text
