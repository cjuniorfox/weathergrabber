from pyquery import PyQuery
from weathergrabber.domain.city_location import CityLocation
import logging

class ExtractLocationService:
    def __init__(self):
        self.logging = logging.getLogger(__name__)

    def execute(self, weather_data: PyQuery) -> CityLocation:
        self.logging.debug("Extracting location from weather data.")
        try:
            data = weather_data("h1[class*='CurrentConditions--location']").text()
        except Exception as e:
            self.logging.error(f"Error extracting location data: {e}")
            raise ValueError("Could not extract location data")
        
        self.logging.debug(f"Extracted string: {data}")
        city_location = CityLocation.from_string(data)
        self.logging.debug(f"Extracted location: {city_location}")
        return city_location