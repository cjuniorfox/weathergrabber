import logging
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.output_enum import OutputEnum
from weathergrabber.adapter.client.weather_api import WeatherApi
from weathergrabber.adapter.client.weather_search_api import WeatherSearchApi
from weathergrabber.service.search_location_service import SearchLocationService
from weathergrabber.service.read_weather_service import ReadWeatherService
from weathergrabber.service.extract_location_service import ExtractLocationService
from weathergrabber.service.extract_temperature_service import ExtractTemperatureService
from weathergrabber.service.extract_feelslike_temperature_service import ExtractFeelslikeTemperatureService
from weathergrabber.service.extract_icon_service import ExtractIconService
from weathergrabber.service.extract_today_details_service import ExtractTodayDetailsService
from weathergrabber.service.extract_aqi_service import ExtractAQIService
from weathergrabber.service.extract_health_activities_service import ExtractHealthActivitiesService
from weathergrabber.service.extract_hourly_forecast_service import ExtractHourlyForecastService
#from weathergrabber.service.extract_daily_forecast_service import ExtractDailyForecastService


from weathergrabber.usecase.use_case import UseCase


class WeatherGrabberApplication:

    def _beans(self):
        self.weather_search_api = WeatherSearchApi()
        self.weather_api = WeatherApi()
        self.search_location_service = SearchLocationService(self.weather_search_api)
        self.read_weather_service = ReadWeatherService(self.weather_api)
        self.extract_city_location_service = ExtractLocationService()
        self.extract_temperatura_service = ExtractTemperatureService()
        self.extract_feelslike_temperature_service = ExtractFeelslikeTemperatureService()
        self.extract_icon_service = ExtractIconService()
        self.extract_today_details_service = ExtractTodayDetailsService()
        self.extract_aqi_service = ExtractAQIService()
        self.extract_health_activities_service = ExtractHealthActivitiesService()
        self.extract_hourly_forecast_service = ExtractHourlyForecastService()
        #self.extract_daily_forecast_service = ExtractDailyForecastService()
        self.use_case = UseCase(
                self.search_location_service,
                self.read_weather_service,
                self.extract_city_location_service,
                self.extract_temperatura_service,
                self.extract_feelslike_temperature_service,
                self.extract_icon_service,
                self.extract_today_details_service,
                self.extract_aqi_service,
                self.extract_health_activities_service,
                self.extract_hourly_forecast_service,
                #self.extract_daily_forecast_service
            )
        pass
        
    def _define_controller(self, output_format: OutputEnum):
        if output_format == OutputEnum.CONSOLE:
            from weathergrabber.adapter.tty.console_tty import ConsoleTTY
            self.controller = ConsoleTTY(self.use_case)

        elif output_format == OutputEnum.JSON:
            from weathergrabber.adapter.tty.json_tty import JsonTTY
            self.controller = JsonTTY(self.use_case)

        elif output_format == OutputEnum.WAYBAR:
            from weathergrabber.adapter.tty.waybar_tty import WaybarTTY
            self.controller = WaybarTTY(self.use_case)

        else:
            self.logger.error(f"Unsupported output format: {output_format}")
            raise ValueError(f"Unsupported output format: {output_format}")
        
    def __init__(self, params: Params):
        self.logger = logging.getLogger(__name__)
        self._beans()
        self._define_controller(params.output_format)
        self.controller.execute(params)