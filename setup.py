#!/usr/bin/env python3
import os
import oauth2client
from oauth2client import client, tools
import argparse

INKYDASH_CREDENTIALS_DIR = "./inkydash-credentials"
INKYDASH_CONFIG_DIR = "./inkydash-config"
INKYDASH_GOOGLE_CREDENTIALS_FILE = INKYDASH_CREDENTIALS_DIR + "/inkydash.json"
# oauth2 json credentials from google console
CLIENT_SECRET_FILE = INKYDASH_CONFIG_DIR + "/inkydash.apps.googleusercontent.com.json"
APPLICATION_NAME = "InkyDash"
SCOPES = "https://www.googleapis.com/auth/calendar"


def get_google_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    # check for existing credentials
    home_dir = os.path.expanduser("~")
    if not os.path.exists(INKYDASH_CREDENTIALS_DIR):
        os.makedirs(INKYDASH_CREDENTIALS_DIR)
    credential_path = os.path.join(INKYDASH_GOOGLE_CREDENTIALS_FILE)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        # fetch credentials through oauth flow
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        credentials = tools.run_flow(flow, store, flags)
        # print('Storing credentials to ' + credential_path)
    return credentials


print("InkyDash Server setup tool")

if os.path.exists(INKYDASH_GOOGLE_CREDENTIALS_FILE):
    print(
        "Found credentials: "
        + INKYDASH_GOOGLE_CREDENTIALS_FILE
        + "\nCopy this file to the inkydash-credentials directory on your Raspberry Pi."
    )
else:
    print("Credentials not found, starting Oauth flow")
    get_google_credentials()
