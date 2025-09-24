import logging
from pyquery import PyQuery
from weathergrabber.domain.weather_icon_enum import WeatherIconEnum


class ExtractIconService:
    def __init__(self):
        self.logging = logging.getLogger(__name__)
        pass

    def execute(self, weather_data: PyQuery) -> WeatherIconEnum:
        try:
            data = weather_data("div[class*='CurrentConditions--tempIconContainer'] svg[class*='CurrentConditions--wxIcon']").attr('name')
            
            self.logging.debug(f"Extracted data for icon: {data}")
            icon = WeatherIconEnum.from_name(data)
            if icon is None:
                raise ValueError(f"Unknown weather icon: {data}")
            self.logging.debug(f"Mapped icon: {icon}")
            
            return icon
            
        except Exception as e:
            self.logging.error(f"Error extracting icon: {e}")
            raise ValueError("Could not extract icon.")