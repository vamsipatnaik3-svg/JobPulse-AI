
from app.database.db import init_db
from app.processing.pipeline import process_emails
from app.briefing.generator import generate_daily_briefing
from app.briefing.voice import generate_voice
from app.briefing.storage import upload_latest_briefing


def run_jobpulse():

    print("\n====================================")
    print("       JOBPULSE AI DAILY RUN")
    print("====================================")

    try:

        # Step 0: Initialize database
        print("\nStep 0: Initializing database...")
        init_db()

        # Step 1: Process Gmail emails
        print("\nStep 1: Processing Gmail emails...")
        analyzed_emails = process_emails()

        # Step 2: Generate daily briefing
        print("\nStep 2: Generating daily briefing...")
        briefing_text = generate_daily_briefing(analyzed_emails)

        print("\n========== DAILY BRIEFING ==========")
        print(briefing_text)

        # Step 3: Generate ElevenLabs audio
        print("\nStep 3: Generating voice briefing...")
        audio_path = generate_voice(briefing_text)

        # Step 4: Upload audio to Supabase
        print("\nStep 4: Uploading audio to Supabase...")
        upload_latest_briefing(audio_path)

        print("\n========== JOBPULSE AI COMPLETED ==========")
        print("Briefing audio generated and uploaded successfully!")
        print(f"Local audio file: {audio_path}")

        return audio_path

    except Exception as error:

        print("\nJobPulse AI execution failed!")
        print(f"Error: {error}")

        raise


if __name__ == "__main__":
    run_jobpulse()
