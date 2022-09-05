#!/usr/bin/env python3
import os
import credentials

print("InkyDash Server setup tool")

if os.path.exists(
    credentials.INKYDASH_CREDENTIALS_DIR + credentials.INKYDASH_GOOGLE_CREDENTIALS_FILE
):
    print(
        f"Found credentials: {credentials.INKYDASH_CREDENTIALS_DIR}{credentials.INKYDASH_GOOGLE_CREDENTIALS_FILE}\nCopy this file to the inkydash-credentials directory on your Raspberry Pi."
    )
else:
    print("Credentials not found, starting Oauth flow")
    credentials.get_google_credentials()
