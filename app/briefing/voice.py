
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

MODEL_ID = "eleven_multilingual_v2"

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "generated_audio"


def generate_voice(text: str) -> str:
    """
    Convert briefing text into speech using ElevenLabs.
    Save the generated audio as an MP3 file.
    """

    if not API_KEY:
        raise ValueError("ELEVENLABS_API_KEY is missing in .env")

    if not VOICE_ID:
        raise ValueError("ELEVENLABS_VOICE_ID is missing in .env")

    if not text or not text.strip():
        raise ValueError("Briefing text cannot be empty")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75,
            "style": 0.30,
            "use_speaker_boost": True
        }
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "jobpulse_briefing.mp3"

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        params={"output_format": "mp3_44100_128"},
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"ElevenLabs API error ({response.status_code}): "
            f"{response.text[:1000]}"
        )

    output_file.write_bytes(response.content)

    print(f"Voice generated successfully: {output_file}")

    return str(output_file)
