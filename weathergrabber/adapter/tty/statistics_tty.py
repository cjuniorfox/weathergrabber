from weathergrabber.application.usecases.statistics_uc import StatisticsUC
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.output_enum import OutputEnum
from weathergrabber.domain.adapter.mappers.statistics_mapper import statistics_to_dict
from weathergrabber.domain.entities.statistics import Statistics
import logging
import json

class StatisticsTTY:
    def __init__(self, statistics_uc: StatisticsUC):
        self.logger = logging.getLogger(__name__)
        self.statistics_uc = statistics_uc

    def execute(self, params : Params):
        statistics = self.statistics_uc.execute(params)
        print_value = self.json_print(statistics) if (params.output_format == OutputEnum.JSON) else self.tty_print(statistics)
        print(print_value)
            
    def tty_print(self, statistics: Statistics):
        self.logger.info("Preparing TTY output for statistics")
        lines = [
            "",
            "WeatherGrabber Statistics",
            "=========================",
            f"Total Forecasts: {statistics.total_forecasts}",
            f"Unique Locations: {statistics.unique_locations}",
            f"Unique Search Names: {statistics.unique_search_names}",
            f"Database Path: {statistics.database_path}",
            "",
        ]
        return "\n".join(lines)
    
    def json_print(self, statistics: Statistics):
        self.logger.info("Preparing JSON output for statistics")
        return json.dumps(statistics_to_dict(statistics))