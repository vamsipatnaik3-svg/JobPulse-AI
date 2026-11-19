'''
The summarizer will combine the original email, classification and extracted details to generate a useful summary.
'''


import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "openai/gpt-oss-20b"


def summarize_email(email, category, extracted_details):

    subject = email.get("subject", "")
    sender = email.get("sender", "")
    body = email.get("body", "")

    prompt = f"""
    You are JobPulse AI, an intelligent job-search assistant.

    Explain the important information in this email.

    Email category: {category}

    Sender: {sender}
    Subject: {subject}
    Email body: {body[:4000]}

    Extracted information:
    {extracted_details}

    Create a concise summary that explains:
    1. What happened?
    2. Which company and role are involved?
    3. What is the current application status?
    4. Does the user need to take any action?

    Rules:
    - Use simple, professional language.
    - Do not invent information.
    - Mention only facts supported by the email.
    - Keep the summary within 3 to 5 sentences.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You generate accurate job-search email summaries."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    summary = response.choices[0].message.content

    return summary.strip()
