
from app.intelligence.extractor import extract_job_details

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

result = extract_job_details(email, category)

print("\nEXTRACTED JOB DETAILS")

for key, value in result.items():
    print(f"{key}: {value}")
