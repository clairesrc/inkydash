from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import os

INKYDASH_CREDENTIALS_DIR = "./credentials"
INKYDASH_CONFIG_DIR = "./config"
INKYDASH_GOOGLE_CREDENTIALS_FILE = "/inkydash.json"
# oauth2 json credentials from google console
CLIENT_SECRET_FILE = "/inkydash.apps.googleusercontent.com.json"
APPLICATION_NAME = "InkyDash"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_credentials(
    token_file=INKYDASH_CREDENTIALS_DIR + INKYDASH_GOOGLE_CREDENTIALS_FILE,
    client_secrets_file=INKYDASH_CONFIG_DIR + CLIENT_SECRET_FILE,
):
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    # check for existing credentials
    credentials = None
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES
            )
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(credentials.to_json())

    return credentials
