import oauth2client
from oauth2client import client, tools, file
import argparse
import os

INKYDASH_CREDENTIALS_DIR = "./inkydash-credentials"
INKYDASH_CONFIG_DIR = "./inkydash-config"
INKYDASH_GOOGLE_CREDENTIALS_FILE = "/inkydash.json"
# oauth2 json credentials from google console
CLIENT_SECRET_FILE = "/inkydash.apps.googleusercontent.com.json"
APPLICATION_NAME = "InkyDash"
SCOPES = "https://www.googleapis.com/auth/calendar"


def get_google_credentials(
    credentials_file=INKYDASH_CREDENTIALS_DIR + INKYDASH_GOOGLE_CREDENTIALS_FILE,
    credentials_secret=INKYDASH_CONFIG_DIR + CLIENT_SECRET_FILE,
):
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    # check for existing credentials
    credential_path = os.path.join(credentials_file)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        # fetch credentials through oauth flow
        flow = client.flow_from_clientsecrets(credentials_secret, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        credentials = tools.run_flow(flow, store, flags)
        # print('Storing credentials to ' + credential_path)
    return credentials
