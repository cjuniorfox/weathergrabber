from weathergrabber.adapter.repository.forecast_repository import ForecastRepository
from weathergrabber.domain.entities.statistics import Statistics
from weathergrabber.domain.adapter.mappers.statistics_mapper import dict_to_statistics
import logging

class RetrieveStatisticsService:
    def __init__(self, weather_repository: ForecastRepository):
        self.log = logging.getLogger(__name__)
        self.weather_repository = weather_repository
    
    def execute(self) -> Statistics:
        """Retrieve and process database."""
        self.log.debug("Retrieving statistics from repository...")
        
        result = self.weather_repository.get_cache_stats()
        statistics = dict_to_statistics(result)
        
        self.log.debug(f"Statistics retrieved successfully: {statistics}")
        return statistics
        