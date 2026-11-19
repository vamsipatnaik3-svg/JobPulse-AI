'''to store into superbase database'''
import os
from pathlib import Path

import requests


def upload_latest_briefing(audio_path):

    print("\nUploading briefing audio to Supabase...")

    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not service_role_key:
        raise ValueError("Supabase credentials are missing!")

    audio_file = Path(audio_path)

    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    bucket_name = "jobpulse-audio"
    file_name = "latest-briefing.mp3"

    upload_url = (
        f"{supabase_url.rstrip('/')}/storage/v1/object/"
        f"{bucket_name}/{file_name}"
    )

    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
        "Content-Type": "audio/mpeg",
        "x-upsert": "true"
    }

    with audio_file.open("rb") as audio:
        response = requests.put(
            upload_url,
            headers=headers,
            data=audio,
            timeout=120
        )

    response.raise_for_status()

    print("Audio uploaded successfully to Supabase!")
    print(f"Storage location: {bucket_name}/{file_name}")

    return True
