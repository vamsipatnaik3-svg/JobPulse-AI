
from app.database.repository import save_email_analysis


test_result = {
    "email": {
        "gmail_message_id": "test-message-001",
        "sender": "Keyloop <no-reply@hire.lever.co>",
        "subject": "Thank you for your application to Keyloop",
        "body": "We received your application for AI Enablement Engineer.",
        "job_score": 4
    },

    "analysis": {
        "classification": {
            "category": "APPLICATION_REJECTION",
            "is_job_related": True,
            "confidence": 0.99
        },

        "extracted_details": {
            "company": "Keyloop",
            "job_role": "AI Enablement Engineer",
            "application_status": "rejected",
            "action_required": False
        },

        "summary": "Your application for AI Enablement Engineer at Keyloop was rejected."
    },

    "processing_status": "SUCCESS"
}


record_id = save_email_analysis(test_result)

print("\nDatabase test completed!")
print("Saved record ID:", record_id)
