import logging
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.output_enum import OutputEnum
from weathergrabber.adapter.client.weather_api import WeatherApi
from weathergrabber.service.read_weather_service import ReadWeatherService

class WeatherGrabberApplication:

    def _beans(self):
        self.weather_api = WeatherApi()
        self.read_weather_service = ReadWeatherService(self.weather_api)
        pass
        
    def _define_uc(self, output_format: OutputEnum):
        if output_format == OutputEnum.CONSOLE:
            from weathergrabber.usecase.console_uc import ConsoleUC
            self.use_case = ConsoleUC(
                self.read_weather_service
            )

        elif output_format == OutputEnum.JSON:
            from weathergrabber.usecase.json_uc import JsonUC
            self.use_case = JsonUC()

        elif output_format == OutputEnum.WAYBAR:
            from weathergrabber.usecase.waybar_uc import WaybarUC
            self.use_case = WaybarUC()

        else:
            self.logger.error(f"Unsupported output format: {output_format}")
            raise ValueError(f"Unsupported output format: {output_format}")
        
    def __init__(self, params: Params):
        self.logger = logging.getLogger(__name__)
        self._beans()
        self._define_uc(params.output_format)
        self.use_case.execute(params)