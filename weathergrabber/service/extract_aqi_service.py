import logging
from weathergrabber.domain.air_quality_index import AirQualityIndex
from pyquery import PyQuery

class ExtractAQIService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pass

    def execute(self, weather_data: PyQuery) -> AirQualityIndex | None:

        self.logger.debug("Extracting Air Quality Index (AQI)...")

        try:
            # '26\nGood\nAir quality is considered satisfactory, and air pollution poses little or no risk.'
            data = weather_data("div[data-testid='AirQualityCard']").text()
            
            air_quality_index = AirQualityIndex.from_string(data) if data else None
            
            self.logger.debug(f"Extracted AQI data: {air_quality_index}")
            
            return air_quality_index
        except Exception as e:
            self.logger.error(f"Error extracting AQI data: {e}")
            raise ValueError("Could not extract AQI data") from e
        