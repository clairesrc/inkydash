from datetime import timedelta
from requests import get
import os

from inkymodule import InkyModule

MODULE_NAME = "weather"
REFRESH_INTERVAL = 15
LABEL = "WEATHER"
SIZE = "medium"

class module(InkyModule):
    def __init__(self, config = {}):
        if "weather_api_key" not in config.keys():
            config["weather_api_key"] = os.getenv("OPENWEATHERMAP_WEATHER_API_SECRET")
        if "units" not in config.keys():
            config["units"] = "imperial"
        super().__init__(config, {
            "name": MODULE_NAME,
            "refreshInterval": REFRESH_INTERVAL,
            "label": LABEL,
            "size": SIZE
        })

        # setup
        ip = module.__get_ip()
        geo = module.__get_geo(ip)
        self.__lat = geo["lat"]
        self.__lon = geo["lon"]
    def _hydrate(self):
        self._set_state(self.__get_weather())
        return
    
    def __get_weather(self):
        """Queries OpenWeatherMap for weather"""
        key = self._get_config()["weather_api_key"]
        unit_config = self._get_config()["units"]
        data = get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={self.__lat}&lon={self.__lon}&units={unit_config}&appid={key}"
        ).json()
        weather_feels_like_temp = data["main"]["feels_like"]
        weather_status = data["weather"][0]["main"]
        unit = "F"
        if unit_config == "metric":
            unit = "C"
        return f"{weather_feels_like_temp}°{unit} | {weather_status}"


    def __get_geo(ip):
        """Queries for IP geolocation"""
        geo = get(f"http://ip-api.com/json/{ip}").json()
        if geo["status"] == "success":
            return geo
        else:
            return False


    def __get_ip():
        """Queries IPify for public IPv4"""
        return get(f"https://api.ipify.org").text