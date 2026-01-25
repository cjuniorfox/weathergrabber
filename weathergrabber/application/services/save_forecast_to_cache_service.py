from weathergrabber.adapter.repository.forecast_repository import ForecastRepository
from weathergrabber.domain.entities.forecast import Forecast
import logging


class SaveForecastToCacheService:
    def __init__(self, forecast_repository: ForecastRepository):
        self.forecast_repository = forecast_repository
        self.logger = logging.getLogger(__name__)

    def execute(self, forecast : Forecast) -> None:

        self.logger.info("Saving forecast to cache")
        
        self.forecast_repository.save_forecast(
            location_id=forecast.search.id,
            search_name=forecast.search.search_name,
            forecast_data=forecast
        )
        
        self.logger.debug("Forecast saved to cache successfully")