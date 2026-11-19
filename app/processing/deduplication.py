'''
    Now we need to solve another important problem.
    Imagine LinkedIn sends the same job alert twice, or our scheduled application fetches the same message again tomorrow.
    We don't want to process the same email repeatedly.
    We'll implement two checks:
    1. Gmail message ID – identifies an already-seen email.
    2. Content fingerprint – identifies emails with identical sender, subject and body.
'''


import hashlib


def generate_email_fingerprint(email):
    """
    Generate a unique fingerprint based on email content.
    """

    sender = email.get("sender", "").lower().strip()
    subject = email.get("subject", "").lower().strip()
    body = email.get("body", "").lower().strip()

    # Combine important email fields
    email_content = f"{sender}|{subject}|{body}"

    # Generate SHA-256 hash
    fingerprint = hashlib.sha256(
        email_content.encode("utf-8")
    ).hexdigest()

    return fingerprint


def deduplicate_emails(emails):
    """
    Remove duplicate emails from a list.
    """

    unique_emails = []

    seen_ids = set()
    seen_fingerprints = set()

    for email in emails:

        # Check Gmail message ID
        message_id = email.get("id")

        if message_id and message_id in seen_ids:
            continue

        # Generate content fingerprint
        fingerprint = generate_email_fingerprint(email)

        if fingerprint in seen_fingerprints:
            continue

        # Mark this email as processed
        if message_id:
            seen_ids.add(message_id)

        seen_fingerprints.add(fingerprint)

        unique_emails.append(email)

    return unique_emails
