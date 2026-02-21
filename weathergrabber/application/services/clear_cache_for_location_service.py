import logging
from weathergrabber.adapter.repository.forecast_repository import ForecastRepository


class ClearCacheForLocationService:
    def __init__(self, forecast_repository: ForecastRepository):
        self.forecast_repository = forecast_repository
        self.logger = logging.getLogger(__name__)

    def execute(self, location_id: str) -> None:
        self.logger.info(f"Clearing cache for location_id: {location_id}")
        
        if not location_id:
            self.logger.warning("No location_id provided, skipping cache clear")
            return
        
        self.forecast_repository.clear_cache_for_location(location_id)
        self.logger.debug(f"Cache cleared for location_id: {location_id} successfully")