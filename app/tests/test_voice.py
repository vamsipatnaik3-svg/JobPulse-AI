
from app.briefing.voice import generate_voice

sample_text = """
Good morning! Welcome to your JobPulse AI daily job update.

You have received a new job-related email.
Your application for the AI Enablement Engineer
position at Keyloop was not selected.

That is your JobPulse AI update.
Have a productive day!
"""

audio_path = generate_voice(sample_text)

print("Generated audio:", audio_path)
