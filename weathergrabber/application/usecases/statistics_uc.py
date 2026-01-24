import logging
from weathergrabber.application.services.retrieve_statistics_service import RetrieveStatisticsService
from weathergrabber.domain.entities.statistics import Statistics
from weathergrabber.domain.adapter.params import Params

class StatisticsUC:
    def __init__(self, retrieve_statistics_service: RetrieveStatisticsService):
        self.retrieve_statistics_service = retrieve_statistics_service
        self.log = logging.getLogger(__name__)


    def execute(self, params: Params) -> Statistics:
        """Execute the use case to retrieve weather statistics."""
        
        self.log.info("Executing StatisticsUC to retrieve weather statistics...")
        statistics = self.retrieve_statistics_service.execute()
        self.log.info("Weather statistics retrieved successfully.")
        
        return statistics