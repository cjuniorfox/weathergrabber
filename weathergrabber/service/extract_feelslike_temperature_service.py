import logging
from pyquery import PyQuery


class ExtractFeelslikeTemperatureService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pass

    def execute(self, weather_data: PyQuery) -> str:
        try:
            temperature = weather_data("span[class*='TodayDetailsCard--feelsLikeTempValue']").text()
            self.logger.debug(f"Extracted feels like temperature: {temperature}")
            return temperature
            
        except Exception as e:
            self.logger.error(f"Error feels like temperature: {e}")
            raise ValueError("Could not extract feels like temperature.")