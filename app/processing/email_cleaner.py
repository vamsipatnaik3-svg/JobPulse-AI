'''
Great! Now we're moving to Phase 3 – Email Processing Engine.
This is where JobPulse AI starts becoming intelligent.
Until now, we have successfully connected Gmail and retrieved emails.
But there's a problem: your inbox contains personal emails, promotions, newsletters, OTPs, job alerts, 
interview invitations and recruiter messages.
We only want job-related emails.
Our objective is to build a pipeline that cleans emails, filters irrelevant messages and removes duplicates before sending anything to GenAI.
'''

'''
Recruitment emails often contain HTML instead of plain text.
We want:
New Job Opportunity!
Company: ABC Technologies
Role: Java Developer
Apply Now

BeautifulSoup helps us convert HTML into readable text.
'''


import re
from bs4 import BeautifulSoup


# This function accepts one email body and returns cleaned text.
def clean_email_body(body):
    """
    Convert email body into clean, readable text.
    """

    if not body:
        return ""

    # Step 1: Parse HTML content
    soup = BeautifulSoup(body, "html.parser")

    # Step 2: Remove scripts and styles
    for element in soup(["script", "style", "head"]):
        element.decompose()

    # Step 3: Extract readable text
    clean_text = soup.get_text(separator=" ")

    # Step 4: Remove unnecessary whitespace
    clean_text = re.sub(r"\s+", " ", clean_text)

    # Step 5: Remove leading and trailing spaces
    clean_text = clean_text.strip()

    return clean_text


def clean_email(email):
    """
    Clean an entire email dictionary.

    Why .copy()?

    Because we don't want to accidentally modify the original dictionary.
    We then clean the subject, sender, snippet and body individually.
    Finally, we return the cleaned dictionary.
    This is an example of data transformation: raw input becomes normalized input.
    """

    cleaned_email = email.copy()

    cleaned_email["subject"] = clean_email_body(
        email.get("subject", "")
    )

    cleaned_email["sender"] = email.get("sender", "").strip()

    cleaned_email["snippet"] = clean_email_body(
        email.get("snippet", "")
    )

    cleaned_email["body"] = clean_email_body(
        email.get("body", "")
    )

    return cleaned_email
