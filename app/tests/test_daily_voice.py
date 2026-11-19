
from app.briefing.generator import generate_daily_briefing
from app.briefing.voice import generate_voice

# Sample analyzed email
sample_emails = [
    {
        "processing_status": "SUCCESS",
        "analysis": {
            "classification": {
                "category": "INTERVIEW_INVITATION",
                "is_job_related": True,
                "confidence": 0.99
            },
            "extracted_details": {
                "company": "ABC Technologies",
                "job_role": "Generative AI Engineer",
                "application_status": "interview scheduled",
                "action_required": True,
                "action_details": "Prepare for the technical interview."
            },
            "summary": "ABC Technologies has invited you for an interview."
        }
    }
]

# Step 1: Generate briefing text
briefing_text = generate_daily_briefing(sample_emails)

print("\n========== JOBPULSE AI BRIEFING ==========")
print(briefing_text)

# Step 2: Convert briefing text into voice
audio_path = generate_voice(briefing_text)

print("\n========== AUDIO GENERATED ==========")
print(audio_path)
