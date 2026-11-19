'''
Gmail Email
     |
     v
Email Classifier
     |
     v
APPLICATION_CONFIRMATION
     |
     v
GenAI Extractor
     |
     v
Structured Job Information
     |
     v
Database

We'll use:
- Groq LLM for understanding the email.
- Pydantic for validating the extracted information.
- Python for connecting the components.
'''


import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "openai/gpt-oss-20b"


def extract_job_details(email, category):

    subject = email.get("subject", "")
    sender = email.get("sender", "")
    body = email.get("body", "")

    prompt = f"""
    You are a job application information extraction assistant.

    Extract information from the email below.

    Email category: {category}
    Sender: {sender}
    Subject: {subject}
    Body: {body[:6000]}

    Return ONLY valid JSON with these fields:

    {{
        "company": null,
        "job_role": null,
        "location": null,
        "salary": null,
        "experience_required": null,
        "skills": [],
        "application_status": null,
        "deadline": null,
        "action_required": false,
        "action_details": null
    }}

    Rules:
    - Extract only information supported by the email.
    - Use null when information is not available.
    - Use an empty list when no skills are mentioned.
    - Do not invent salary, location or experience.
    - Set action_required to true only when the email
      explicitly requests an action from the recipient.
    - Keep application_status concise.
    - Return valid JSON only.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "Extract accurate job information. Never invent missing details."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    result = response.choices[0].message.content

    try:
        extracted_details = json.loads(result)
    except json.JSONDecodeError:
        raise ValueError(
            f"Invalid JSON returned by LLM: {result}"
        )

    required_fields = [
        "company",
        "job_role",
        "location",
        "salary",
        "experience_required",
        "skills",
        "application_status",
        "deadline",
        "action_required",
        "action_details"
    ]

    for field in required_fields:
        if field not in extracted_details:
            raise ValueError(
                f"Missing extracted field: {field}"
            )

    if not isinstance(extracted_details["skills"], list):
        raise ValueError("Skills must be a list")

    if not isinstance(extracted_details["action_required"], bool):
        raise ValueError("action_required must be a boolean")

    return extracted_details
