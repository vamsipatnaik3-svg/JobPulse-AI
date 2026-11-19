
"""
Gmail email fetcher.

Gmail returns message bodies in Base64 URL-safe encoded format.
We authenticate using get_gmail_service().
"""

import base64
import time

from bs4 import BeautifulSoup
from googleapiclient.errors import HttpError

from app.gmail.authentication import get_gmail_service


def gmail_api_request(request, description="Gmail API request"):
    """
    Execute a Gmail API request with exponential backoff.

    Retries temporary rate-limit and server errors.
    """

    max_attempts = 5

    for attempt in range(max_attempts):

        try:
            return request.execute()

        except HttpError as error:

            status_code = error.resp.status

            # Retry rate limits and temporary server errors
            retryable = (
                status_code == 429
                or status_code >= 500
                or (
                    status_code == 403
                    and "rateLimitExceeded" in str(error)
                )
            )

            if not retryable or attempt == max_attempts - 1:
                raise

            wait_time = 2 ** (attempt + 1)

            print(
                f"{description} temporarily failed "
                f"(HTTP {status_code}). "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


def get_header(headers, header_name):
    """Extract a specific email header."""

    for header in headers:

        if header["name"].lower() == header_name.lower():
            return header["value"]

    return ""


def decode_email_part(part):
    """
    Decode the Base64 URL-safe content of an email part.
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
    Extract readable email content.

    Prefer plain text.
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

    # Prefer plain-text content
    if plain_text:
        return "\n".join(plain_text)

    # Fallback to HTML content
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

    print("\nFetching emails from Gmail...")

    # Step 1: Search Gmail for recent messages
    results = gmail_api_request(
        service.users().messages().list(
            userId="me",
            q="in:anywhere newer_than:2d",
            maxResults=max_results
        ),
        description="Gmail email search"
    )

    # Gmail list API returns message references, not full email content
    messages = results.get("messages", [])

    print(f"\nTotal emails retrieved: {len(messages)}")

    email_list = []

    # Step 2: Retrieve complete details for each email
    for index, message in enumerate(messages, start=1):

        print(
            f"Fetching email {index}/{len(messages)}..."
        )

        email_data = gmail_api_request(
            service.users().messages().get(
                userId="me",
                id=message["id"],
                format="full"
            ),
            description=f"Fetching email {index}"
        )

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

    print(f"\nSuccessfully fetched {len(email_list)} emails.")

    return email_list


if __name__ == "__main__":

    emails = fetch_emails(max_results=10)

    for index, email in enumerate(emails, start=1):

        print(f"\n--- EMAIL {index} ---")
        print("From:", email["sender"])
        print("Subject:", email["subject"])
        print("Date:", email["date"])
        print("Snippet:", email["snippet"])
        print("Body:", email["body"][:500])
