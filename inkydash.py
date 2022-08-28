#!/usr/bin/env python3

import httplib2
import sys
import os
from apiclient import discovery
import oauth2client
from oauth2client import client, file, tools
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
import pytz
import datetime
import argparse

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

FREE_INDICATOR = "FREE"
BUSY_INDICATOR = "BUSY"

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'inkydash.apps.googleusercontent.com.json' # oauth2 json credentials from google console
APPLICATION_NAME = 'InkyDash'
IMAGE_FILENAME = "/tmp/inkydash.png"
SCREEN_WIDTH=600
SCREEN_HEIGHT=488

def send_to_screen(filename):
    """Sends image file to Inky screen.
    Sets up Inky API, opens given filename, and draws image.
    """
    # setup
    inky = auto(ask_user=True, verbose=True)
    saturation = 0.5

    # open source image
    image = Image.open(filename)
    resizedimage = image.resize(inky.resolution)

    # draw image
    inky.set_image(resizedimage, saturation=saturation)
    inky.show()

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    # check for existing credentials
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'inkydash.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        # fetch credentials through oauth flow
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_data():
    """Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    # setup
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # get upcoming event
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        # determine free/busy status
        now = datetime.datetime.now().astimezone()
        event_start = datetime.datetime.fromisoformat(event['start'].get('dateTime'))
        event_end = datetime.datetime.fromisoformat(event["end"].get("dateTime"))
        if now >= event_start and now >= event_end:
            return BUSY_INDICATOR
        else:
            return FREE_INDICATOR

def draw_image(text, filename):
    # create an image
    out = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), (255, 255, 255))

    # get a font
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)

    # get a drawing context
    d = ImageDraw.Draw(out)

    # draw multiline text
    d.multiline_text((10, 10), text, font=fnt, fill=(0, 0, 0))
    out.save(filename, "PNG")

def main():
    image_text = get_data()
    draw_image(image_text, IMAGE_FILENAME)
    send_to_screen(IMAGE_FILENAME)

if __name__ == '__main__':
    main()