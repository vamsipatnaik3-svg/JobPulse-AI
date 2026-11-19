
from app.intelligence.intelligence_pipeline import analyze_email


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


result = analyze_email(email)


print("\n========== JOBPULSE AI ANALYSIS ==========")

print("\n1. CLASSIFICATION")
print(result["classification"])

print("\n2. EXTRACTED DETAILS")
print(result["extracted_details"])

print("\n3. EMAIL SUMMARY")
print(result["summary"])
