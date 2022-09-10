import pytest
import os
from dotenv import load_dotenv
from inkydash import InkyDash

load_dotenv()

def test_time():
    id = InkyDash()
    id.setup({"modules": ["time"]}, {})
    assert id.render()

def test_freebusy():
    id = InkyDash()
    id.setup({"modules": ["freebusy"]}, {"GOOGLE_TOKEN_FILENAME": "credentials/inkydash.json", "GOOGLE_CLIENT_SECRET_FILENAME": "config/inkydash.apps.googleusercontent.com.json"})
    assert id.render()

def test_freebusy_no_params():
    errored = False
    id = InkyDash()
    try:
        id.setup({"modules": ["freebusy"]}, {})
    except Exception:
        errored = True
    assert errored

def test_weather():
    id = InkyDash()
    id.setup({"modules": ["weather"]}, {"OPENWEATHERMAP_WEATHER_API_SECRET": os.getenv("OPENWEATHERMAP_WEATHER_API_SECRET")})
    assert id.render()

def test_weather_no_params():
    errored = False
    id = InkyDash()
    try:
        id.setup({"modules": ["weather"]}, {})
    except Exception:
        errored = True
    assert errored

def test_all():
    id = InkyDash()
    id.setup({"modules": ["freebusy", "weather", "time"]}, {"GOOGLE_TOKEN_FILENAME": "credentials/inkydash.json", "GOOGLE_CLIENT_SECRET_FILENAME": "config/inkydash.apps.googleusercontent.com.json", "OPENWEATHERMAP_WEATHER_API_SECRET": os.getenv("OPENWEATHERMAP_WEATHER_API_SECRET")})
    results = id.render()
    assert results[2]["name"] == "time"

def test_weather_bad_params():
    errored = False
    id = InkyDash()
    id.setup({"modules": ["weather"]}, {"OPENWEATHERMAP_WEATHER_API_SECRET": "a"})
    try:
        id.render()
    except Exception:
        errored = True
    assert errored