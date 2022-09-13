import pytest
import os
from dotenv import load_dotenv
from inkydash import InkyDash

load_dotenv()


def test_time():
    id = InkyDash({"modules": ["time"]}, {})
    assert len(id.render()[0]["data"]) > 0


def test_freebusy():
    id = InkyDash(
        {"modules": ["freebusy"]},
        {
            "GOOGLE_TOKEN_FILENAME": "credentials/inkydash.json",
            "GOOGLE_CLIENT_SECRET_FILENAME": "config/inkydash.apps.googleusercontent.com.json",
        },
    )
    assert len(id.render()[0]["data"]) > 0


def test_freebusy_no_params():
    errored = False
    try:
        id = InkyDash({"modules": ["freebusy"]}, {})
    except Exception:
        errored = True
    assert errored


def test_weather():
    id = InkyDash(
        {"modules": ["weather"]},
        {
            "OPENWEATHERMAP_WEATHER_API_SECRET": os.getenv(
                "OPENWEATHERMAP_WEATHER_API_SECRET"
            )
        },
    )
    assert len(id.render()[0]["data"]) > 0


def test_weather_no_params():
    errored = False
    try:
        id = InkyDash({"modules": ["weather"]}, {})
    except Exception:
        errored = True
    assert errored


def test_all():
    id = InkyDash(
        {"modules": ["freebusy", "weather", "time"]},
        {
            "GOOGLE_TOKEN_FILENAME": "credentials/inkydash.json",
            "GOOGLE_CLIENT_SECRET_FILENAME": "config/inkydash.apps.googleusercontent.com.json",
            "OPENWEATHERMAP_WEATHER_API_SECRET": os.getenv(
                "OPENWEATHERMAP_WEATHER_API_SECRET"
            ),
        },
    )
    results = id.render()
    assert results[2]["name"] == "time"


def test_weather_bad_params():
    errored = False
    id = InkyDash({"modules": ["weather"]}, {"OPENWEATHERMAP_WEATHER_API_SECRET": "a"})
    try:
        id.render()
    except Exception:
        errored = True
    assert errored
