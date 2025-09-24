from weathergrabber.adapter.client.weather_api import WeatherApi
import logging
import os
from pyquery import PyQuery
from typing import Tuple

class ReadWeatherService:
    def __init__(
            self,
            weather_api: WeatherApi
        ):
        self.weather_api = weather_api
        self.logging = logging.getLogger(__name__)

    def _define_language_location(self, language: str, location: str) -> Tuple[str, str]:
        lang = language if language != None else os.getenv("LANG","en_IL.UTF-8").split(".")[0].replace("_","-")
        loc = location if location != None else os.getenv('WEATHER_LOCATION_ID')
        return lang, loc
        

    def execute(self, language: str, location: str) -> PyQuery:

        lang, loc = self._define_language_location(language, location)

        self.logging.debug(f"Executing WeatherDataService with language: {lang}, location: {loc}")
        
        weather_data = self.weather_api.get_weather(lang, loc)

        self.logging.debug(f"Weather data retrieved.")

        return weather_data

        