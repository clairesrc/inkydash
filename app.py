import httplib2
from dateutil import parser
import os
from apiclient import discovery
import datetime
from flask import Flask
from requests import get
from dotenv import load_dotenv
import credentials

load_dotenv()

FREE_INDICATOR = "FREE"
BUSY_INDICATOR = "BUSY"

APPLICATION_NAME = "InkyDash"
SCOPES = "https://www.googleapis.com/auth/calendar"

TIMEZONE = os.getenv("TZ")
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_WEATHER_API_SECRET")

api_cache = {}

dashboard_state = {"data": {}}

app = Flask(__name__)

# this is inside docker, so adjust config paths
INKYDASH_GOOGLE_CREDENTIALS_FILE = (
    "/root/.credentials" + credentials.INKYDASH_GOOGLE_CREDENTIALS_FILE
)
CLIENT_SECRET_FILE = "/inkydash/config" + credentials.CLIENT_SECRET_FILE


def get_freebusy():
    """Creates a Google Calendar API service object and outputs free/busy status"""
    # setup
    creds = credentials.get_google_credentials(
        credentials_file=INKYDASH_GOOGLE_CREDENTIALS_FILE,
        credentials_secret=CLIENT_SECRET_FILE,
    )
    http = creds.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)
    now = datetime.datetime.now().astimezone()

    eventsResult = (
        service.freebusy()
        .query(
            body={
                "timeMin": datetime.datetime.combine(now, datetime.datetime.min.time())
                .astimezone()
                .isoformat(),
                "timeMax": datetime.datetime.combine(now, datetime.datetime.max.time())
                .astimezone()
                .isoformat(),
                "timeZone": TIMEZONE,
                "items": [{"id": "primary"}],
            }
        )
        .execute()
    )
    busy = eventsResult["calendars"]["primary"]["busy"]
    if len(busy) == 0:
        return {"status": FREE_INDICATOR, "next": False}

    event = busy[0]
    event_start = parser.parse(event["start"]).astimezone()

    if event_start <= now:
        return {"status": BUSY_INDICATOR, "next": event}
    else:
        return {"status": FREE_INDICATOR, "next": event}


def get_time():
    """Gets current time in AM/PM format"""
    return datetime.datetime.now().strftime("%I:%M %p")


def get_weather(secret: str, lat: str, lon: str):
    """Queries OpenWeatherMap for weather"""
    return get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={secret}"
    ).json()


def get_geo():
    """Queries for IP geolocation"""
    geo = get(f"http://ip-api.com/json/{get_ip()}").json()
    if geo["status"] == "success":
        return geo
    else:
        return False


def get_ip():
    """Queries IPify for public IPv4"""
    return get(f"https://api.ipify.org").text


def refresh_state():
    """Refreshes state dict from external APIs"""
    geo = get_geo()
    weather = False
    if geo:
        weather = get_weather(WEATHER_API_KEY, geo["lat"], geo["lon"])
    write_state({"freebusy": get_freebusy(), "weather": weather, "time": ""})


def write_state(data: dict):
    """Updates in-memory state cache"""
    dashboard_state["data"] = data


def get_state():
    """Gets dashboard state"""
    if len(dashboard_state["data"]) == 0:
        refresh_state()
    dashboard_state["data"]["time"] = get_time()
    return dashboard_state


@app.route("/")
def api_get_state():
    return get_state()


@app.route("/refresh")
def api_refresh_state():
    refresh_state()
    return {"success": True}
