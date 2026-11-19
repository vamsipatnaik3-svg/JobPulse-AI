
import re


# Keywords indicating genuine job-related communication
JOB_KEYWORDS = [
    # Job opportunities
    "job opportunity",
    "job opening",
    "job alert",
    "career opportunity",
    "career opening",
    "new opportunity",
    "job vacancy",
    "vacancy",

    # Job roles
    "software engineer",
    "software developer",
    "java developer",
    "python developer",
    "backend developer",
    "frontend developer",
    "full stack developer",
    "ai engineer",
    "ai enablement engineer",
    "generative ai engineer",
    "machine learning engineer",
    "data scientist",

    # Applications
    "application received",
    "application submitted",
    "application confirmation",
    "application update",
    "application status",
    "thank you for applying",
    "your application",

    # Interviews
    "interview invitation",
    "interview scheduled",
    "interview confirmed",
    "interview",
    "technical round",
    "hr round",
    "screening round",
    "schedule a call",

    # Assessments
    "assessment",
    "coding test",
    "coding assessment",
    "online test",
    "technical assessment",
    "hackerrank",
    "codility",

    # Recruiters and hiring
    "recruiter",
    "recruitment",
    "talent acquisition",
    "hiring team",
    "hiring manager",
    "shortlisted",
    "selected for",
    "job offer",
    "offer letter",
    "employment offer",
    "joining date",

    # Application outcomes
    "rejection",
    "unfortunately",
    "moving forward with other candidates",
    "not selected",
    "congratulations",
]


# Strong indicators of irrelevant emails
# These are checked primarily against the subject.
NEGATIVE_KEYWORDS = [
    "subscription confirmed",
    "renewal price",
    "trading bulletin",
    "stock market",
    "nifty",
    "sensex",
    "job post credit",
    "job listing access",
    "ai resume match",
    "screening resumes",
    "promotional offer",
]


def normalize_text(value):
    """
    Safely convert email content into normalized lowercase text.
    """

    if not isinstance(value, str):
        return ""

    value = value.lower()
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def score_job_email(email):
    """
    Calculate a job relevance score using email fields.
    """

    subject = normalize_text(email.get("subject"))
    sender = normalize_text(email.get("sender"))
    snippet = normalize_text(email.get("snippet"))
    body = normalize_text(email.get("body"))

    # Check strong negative signals in the subject only.
    # Do not reject emails just because they contain
    # unsubscribe text in their footer.
    for keyword in NEGATIVE_KEYWORDS:

        if keyword in subject:
            return 0

    score = 0

    # Subject is the strongest signal.
    for keyword in JOB_KEYWORDS:

        if keyword in subject:
            score += 5

    # Sender can indicate recruiters or hiring platforms.
    for keyword in JOB_KEYWORDS:

        if keyword in sender:
            score += 3

    # Email preview/snippet.
    for keyword in JOB_KEYWORDS:

        if keyword in snippet:
            score += 2

    # Email body.
    # Limit the body checked to avoid irrelevant footers
    # and long email signatures dominating the result.
    relevant_body = body[:5000]

    for keyword in JOB_KEYWORDS:

        if keyword in relevant_body:
            score += 1

    return score


def filter_job_related_emails(emails, minimum_score=3):
    """
    Filter potential job-related emails.

    Emails passing this stage are sent to the GenAI
    intelligence pipeline for deeper classification.
    """

    job_emails = []

    for email in emails:

        score = score_job_email(email)

        if score >= minimum_score:

            email_copy = email.copy()
            email_copy["job_score"] = score

            job_emails.append(email_copy)

    return job_emails
