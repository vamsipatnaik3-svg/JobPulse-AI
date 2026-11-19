
from app.intelligence.classifier import classify_email

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

result = classify_email(email)

print("\nCLASSIFICATION RESULT")
print(result)

# you can run this file
# python -m app.tests.test_classifier
