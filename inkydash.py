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
from requests import get
from dotenv import load_dotenv
load_dotenv()  
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()


FREE_INDICATOR = 'FREE'
BUSY_INDICATOR = 'BUSY'

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'inkydash.apps.googleusercontent.com.json' # oauth2 json credentials from google console
APPLICATION_NAME = 'InkyDash'
IMAGE_FILENAME = "/tmp/inkydash.png"
SCREEN_WIDTH=600
SCREEN_HEIGHT=488
FONT_FILENAME = 'Pillow/Tests/fonts/NotoSansMono-Regular.ttf'

GEO_API_KEY = os.getenv("IPSTACK_GEOIP_API_SECRET")
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_WEATHER_API_SECRET")

dashboard_state = {}

def send_to_screen():
    """Sends image file to Inky screen.
    Sets up Inky API, opens given filename, and draws image.
    """
    # setup
    inky = auto(ask_user=True, verbose=True)
    saturation = 0.5

    # open source image
    image = Image.open(IMAGE_FILENAME)
    resizedimage = image.resize(inky.resolution)

    # draw image
    inky.set_image(resizedimage, saturation=saturation)
    inky.show()

def get_google_credentials():
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

def get_freebusy():
    """Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    # setup
    credentials = get_google_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.now().astimezone()

    # get upcoming event
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now.isoformat(), maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        # determine free/busy status
        event_start = datetime.datetime.fromisoformat(event['start'].get('dateTime'))
        event_end = datetime.datetime.fromisoformat(event['end'].get('dateTime'))
        if now >= event_start and now >= event_end:
            return BUSY_INDICATOR
        else:
            return FREE_INDICATOR

def get_weather(secret, lat, lon):
    """Queries OpenWeatherMap
    """
    return get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={secret}").json()['main']

def get_geo(secret):
    """Queries IPStack for IP geolocation
    """
    return get(f"http://api.ipstack.com/{get_ip()}?access_key={secret}").json()

def get_ip():
    """Queries IPify for public IPv4
    """
    return get(f"https://api.ipify.org").text

def get_state():
    """Refresh & get dashboard state.
    """
    geo = get_geo(GEO_API_KEY)
    return {
        'freebusy': get_freebusy(),
        'weather': get_weather(WEATHER_API_KEY, geo['latitude'], geo['longitude'])
    }

def draw_image(state):
    """Create PNG image from dashboard state.
    """
    freebusy = state['freebusy']
    weather_feels_like_temp = state['weather']['feels_like']

    # create an image
    out = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0, 0))

    # font
    font_big = ImageFont.truetype(FONT_FILENAME, 90)
    font_medium = ImageFont.truetype(FONT_FILENAME, 48)
    font_small = ImageFont.truetype(FONT_FILENAME, 24)

    # get a drawing context
    d = ImageDraw.Draw(out)

    # draw labels
    d.multiline_text((10, 0), 'STATUS', font=font_small, fill=(200, 200, 200))
    d.multiline_text((10, 110), 'WEATHER', font=font_small, fill=(200, 200, 200))

    # draw freebusy
    d.multiline_text((5, 10), f"{freebusy}", font=font_big, fill=(255, 255, 255))

    # draw freebusy
    d.multiline_text((5, 120), f"{weather_feels_like_temp}°F", font=font_medium, fill=(255, 255, 255))

    # save image
    out.save(IMAGE_FILENAME, 'PNG')

def main():
    draw_image(get_state())
    send_to_screen()

if __name__ == '__main__':
    main()