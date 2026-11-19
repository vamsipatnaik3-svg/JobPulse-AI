'''5. Understand the important functions
Function	What it does
get_gmail_service()	Main authentication function
from_authorized_user_file()	Reads previously saved authorization
credentials.expired	Checks whether access token expired
credentials.refresh()	Obtains a fresh access token
run_local_server()	Opens Google's OAuth authorization flow
credentials.to_json()	Saves authorization tokens
build("gmail", "v1")	Creates Gmail API service

Important concept for your GenAI interviews: OAuth access tokens and refresh tokens are different.
Access tokens authorize API requests; refresh tokens help obtain new access tokens without repeatedly 
asking the user to sign in.'''


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Gmail permission: Read emails only
'''Scope	Permission
gmail.readonly	Read emails
gmail.send	Send emails
gmail.modify	Read and modify emails'''

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


# Project root directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")





import os
import json

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def get_gmail_service():

    credentials = None

    # Cloud mode: load token from Railway environment variable
    cloud_token = os.getenv("GMAIL_TOKEN_JSON")

    if cloud_token:
        token_data = json.loads(cloud_token)

        credentials = Credentials.from_authorized_user_info(
            token_data,
            SCOPES
        )

    # Local mode: load token from local file
    elif os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    # Refresh expired credentials
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    # If cloud credentials cannot be refreshed, stop safely
    if not credentials or not credentials.valid:

        if cloud_token:
            raise RuntimeError(
                "Cloud Gmail authentication is invalid. "
                "Reauthorize Gmail and update GMAIL_TOKEN_JSON."
            )

        if not os.path.exists(CREDENTIALS_FILE):
            raise FileNotFoundError(
                "credentials.json not found in project root"
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE,
            SCOPES
        )

        credentials = flow.run_local_server(port=0)

    # Save refreshed token only in local mode
    if not cloud_token:
        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    print("Gmail authentication successful!")

    return service
