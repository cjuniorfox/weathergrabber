from pyquery import PyQuery as pq
from urllib.error import HTTPError
import logging

class WeatherApi:

    def __init__(self):
        self.logging = logging.getLogger(__name__)
        pass

    def get_weather(self,language: str, location: str) -> dict:
        url = f"https://weather.com/{language}/weather/today/l/{location}"
        if location == None:
            url = f"https://weather.com/{language}/weather/today"        
        elif len(location) < 64 :
            raise ValueError("Invalid location")
        if language == None:
            raise ValueError("language must be specified")
        try:
            self.logging.debug(f"Fetching weather data from URL: %s.", url)
            return pq(url=url)
        except HTTPError as e:
            if(e.code == 404):
                self.logging.error(f"HTTP {e.code} error when fetching weather data from URL: {url}. Check for the location_id or lang data.")
                raise ValueError(f"HTTP error {e.code} when fetching weather data. Check for the location_id or lang data.")