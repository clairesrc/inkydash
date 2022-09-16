#!/usr/bin/env python3
import os
import credentials


if os.path.exists(
    credentials.INKYDASH_CREDENTIALS_DIR + credentials.INKYDASH_GOOGLE_CREDENTIALS_FILE
):
    print(
        f"Found credentials: {credentials.INKYDASH_CREDENTIALS_DIR}{credentials.INKYDASH_GOOGLE_CREDENTIALS_FILE}"
    )
else:
    print("Starting Oauth flow")
    credentials.get_google_credentials()
