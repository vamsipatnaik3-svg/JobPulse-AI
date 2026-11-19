'''

Component	Purpose
load_dotenv()	Loads environment variables from .env
Groq()	Creates the LLM client
MODEL_NAME	Selects the language model
classify_email()	Main classification function
prompt	Gives the LLM its instructions and email
chat.completions.create()	Sends the request to Groq
json.loads()	Converts the LLM response into a Python dictionary
Validation	Checks that the category and confidence are valid

One important distinction: the LLM is making a semantic decision. 
It can understand that "we received your application" means an application confirmation even
if the email never uses the exact phrase "job application confirmation."

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


EMAIL_CATEGORIES = [
    "JOB_OPPORTUNITY",
    "JOB_RECOMMENDATION",
    "APPLICATION_CONFIRMATION",
    "INTERVIEW_INVITATION",
    "ASSESSMENT",
    "APPLICATION_REJECTION",
    "OFFER",
    "RECRUITER_MESSAGE",
    "RESUME_UPDATE",
    "IRRELEVANT"
]


def classify_email(email):

    subject = email.get("subject", "")
    sender = email.get("sender", "")
    body = email.get("body", "")

    prompt = f"""
    You are an intelligent job email classification assistant.

    Analyze the email and identify its category.

    Allowed categories:
    {EMAIL_CATEGORIES}

    Email:
    Sender: {sender}
    Subject: {subject}
    Body: {body[:5000]}

    Return ONLY valid JSON in this format:

    {{
        "category": "APPLICATION_CONFIRMATION",
        "is_job_related": true,
        "confidence": 0.95
    }}

    Rules:
    - Select exactly one allowed category.
    - Do not invent information.
    - Job application updates are job-related.
    - Promotional emails unrelated to the user's job search are IRRELEVANT.
    - Confidence must be between 0 and 1.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You classify job-related emails accurately."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    try:
        classification = json.loads(result)
    except json.JSONDecodeError:
        raise ValueError(
            f"LLM returned invalid JSON: {result}"
        )

    if classification.get("category") not in EMAIL_CATEGORIES:
        raise ValueError("LLM returned an unsupported category")

    if not isinstance(classification.get("is_job_related"), bool):
        raise ValueError("Invalid is_job_related value")

    confidence = classification.get("confidence")

    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        raise ValueError("Invalid confidence score")

    return classification
