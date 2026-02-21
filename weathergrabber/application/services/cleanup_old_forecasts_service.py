import logging
from weathergrabber.adapter.repository.forecast_repository import ForecastRepository

class CleanupOldForecastsService:
    def __init__(self, forecast_repository: ForecastRepository):
        self.forecast_repository = forecast_repository
        self.logger = logging.getLogger(__name__)

    def execute(self, hours_threshold: int = 24) -> None:
        try:
            self.logger.info(f"Cleaning up forecasts older than {hours_threshold} hours")
            
            self.forecast_repository.delete_old_forecasts(hours_threshold=hours_threshold)
            
            self.logger.debug(f"Old forecasts cleaned up successfully for forecasts older than {hours_threshold} hours")
        except Exception as e:
            self.logger.error(f"Error cleaning up old forecasts: {e}")