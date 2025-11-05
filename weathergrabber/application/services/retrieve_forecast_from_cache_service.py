from weathergrabber.adapter.repository.forecast_repository import ForecastRepository
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.entities.forecast import Forecast
from typing import Optional
import logging

class RetrieveForecastFromCacheService:
    def __init__(self, forecast_repository: ForecastRepository):
        self.forecast_repository = forecast_repository
        self.log = logging.getLogger(__name__)

    def execute(self, params: Params) -> Optional[Forecast]:
        """Retrieve forecast from cache based on parameters."""
        if params.location.id:
            forecast = self.forecast_repository.get_by_location_id(params.location.id)
        elif params.location.search_name:
            forecast = self.forecast_repository.get_by_search_name(params.location.search_name)
        else:
            self.log.debug("No location_id or search_name provided in params; cannot retrieve from cache.")
            raise ValueError("Either location ID or search name must be provided to retrieve forecast from cache.")

        if forecast:
            self.log.debug("Forecast retrieved from cache successfully.")
        else:
            self.log.debug("No forecast found in cache.")
        return forecast