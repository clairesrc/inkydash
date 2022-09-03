import pytest
import os
import inkydash
from dotenv import load_dotenv

GEO_API_KEY = os.getenv("IPSTACK_GEOIP_API_SECRET")
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_WEATHER_API_SECRET")

def test_get_weather_success():
    geo = inkydash.get_geo(GEO_API_KEY)
    if geo:
        weather = inkydash.get_weather(WEATHER_API_KEY, geo['lat'], geo['lon'])
        assert weather
    else:
        assert False

def test_get_geo_success():
    assert inkydash.get_geo(GEO_API_KEY)

def test_get_ip_success():
    assert inkydash.get_ip()

def test_get_freebusy_success():
    assert inkydash.get_freebusy()
