'''base64 is required because Gmail returns message body data in Base64 URL-safe encoded form.

We import get_gmail_service() because email fetching requires authentication.'''
import base64

from app.gmail.authentication import get_gmail_service

# for extracting email headers
def get_header(headers, header_name):
    """Extract a specific email header."""

    for header in headers:
        if header["name"].lower() == header_name.lower():
            return header["value"]

    return ""

'''
Extract email body
This function extracts the readable content of an email.

Gmail messages can have different MIME structures.

For example:
- text/plain: Normal text.
- text/html: HTML-formatted content.
- multipart/alternative: Multiple representations of the same email.
- multipart/mixed: Email body plus attachments.

'''

import base64
from bs4 import BeautifulSoup


def decode_email_part(part):
    """
    Decode the Base64 content of an email part.
    """

    data = part.get("body", {}).get("data")

    if not data:
        return ""

    decoded_bytes = base64.urlsafe_b64decode(data)

    return decoded_bytes.decode(
        "utf-8",
        errors="replace"
    )


def extract_email_body(payload):
    """
    Extract plain-text email content.
    If plain text is unavailable, convert HTML to text.
    """

    plain_text = []
    html_text = []

    def process_part(part):

        mime_type = part.get("mimeType", "")

        if mime_type == "text/plain":

            content = decode_email_part(part)

            if content:
                plain_text.append(content)

        elif mime_type == "text/html":

            content = decode_email_part(part)

            if content:
                html_text.append(content)

        # Process nested MIME parts
        for nested_part in part.get("parts", []):
            process_part(nested_part)

    process_part(payload)

    # Prefer plain text
    if plain_text:
        return "\n".join(plain_text)

    # Fallback to HTML
    if html_text:

        soup = BeautifulSoup(
            "\n".join(html_text),
            "html.parser"
        )

        for element in soup(["script", "style"]):
            element.decompose()

        return soup.get_text(separator=" ", strip=True)

    return ""



def fetch_emails(max_results=10):

    service = get_gmail_service()

    # Search Gmail for recent messages
    '''
    Let's understand each parameter.
    Parameter	Meaning
    userId="me"	Use the authenticated Gmail account
    q	Gmail search query
    maxResults	Maximum number of message IDs to retrieve
    execute()	Actually sends the API request
    '''
    results = service.users().messages().list(
        userId="me",
        q="in:anywhere newer_than:2d",
        maxResults=max_results
    ).execute()

    '''
    The Gmail API initially gives us a list of message references, including IDs.
    It doesn't return all the complete email content in this list operation.
    That's why we need another API call.
    '''
    messages = results.get("messages", [])

    print(f"\nTotal emails retrieved: {len(messages)}")

    email_list = []

    '''
    For every message ID:
        1. We call Gmail's message retrieval endpoint.
        2. We pass the message ID.
        3. We request the full message.
        4. We receive the complete message structure.
        This is important: our implementation makes one list request and then one detail request per email.

        If we retrieve 100 emails, that's approximately 101 API requests.

        We'll optimize pagination and fetching as the project grows.
    '''

    for message in messages:

        # Retrieve complete email details
        email_data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        payload = email_data.get("payload", {})
        headers = payload.get("headers", [])

        email = {
            "id": email_data["id"],
            "thread_id": email_data.get("threadId"),
            "sender": get_header(headers, "From"),
            "subject": get_header(headers, "Subject"),
            "date": get_header(headers, "Date"),
            "snippet": email_data.get("snippet", ""),
            "body": extract_email_body(payload)
        }

        email_list.append(email)

    return email_list


'''
    This is a very important Python concept.
    if __name__ == "__main__" means:
    Execute this section only when the file is run directly as the main program.
    example:python -m app.gmail.email_fetcher
'''
if __name__ == "__main__":

    emails = fetch_emails(max_results=10)

    for index, email in enumerate(emails, start=1):

        print(f"\n--- EMAIL {index} ---")
        print("From:", email["sender"])
        print("Subject:", email["subject"])
        print("Date:", email["date"])
        print("Snippet:", email["snippet"])
        print("Body:", email["body"][:500])
