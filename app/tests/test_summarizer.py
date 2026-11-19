
from app.intelligence.summarizer import summarize_email

email = {
    "sender": "Keyloop <no-reply@hire.lever.co>",
    "subject": "Thank you for your application to Keyloop",
    "body": """
    Thank you for your interest in Keyloop!

    We received your application for
    AI Enablement Engineer.

    Our team will review your application.
    """
}

category = "APPLICATION_CONFIRMATION"

extracted_details = {
    "company": "Keyloop",
    "job_role": "AI Enablement Engineer",
    "location": None,
    "salary": None,
    "experience_required": None,
    "skills": [],
    "application_status": "RECEIVED",
    "deadline": None,
    "action_required": False,
    "action_details": None
}

summary = summarize_email(
    email,
    category,
    extracted_details
)

print("\nJOB EMAIL SUMMARY")
print(summary)
