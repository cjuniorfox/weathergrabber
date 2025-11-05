from weathergrabber.application.usecases.weather_forecast_uc import WeatherForecastUC
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.mappers.forecast_mapper import forecast_to_dict
import logging
import json

class JsonTTY:

    def __init__(self, use_case: WeatherForecastUC):
        self.logger = logging.getLogger(__name__)
        self.use_case = use_case
        pass

    def execute(self, params: Params) -> None:
        self.logger.info("Executing JSON output")
        forecast = self.use_case.execute(params)
        output: dict = forecast_to_dict(forecast)
        output_json = json.dumps(output)
        print(output_json)