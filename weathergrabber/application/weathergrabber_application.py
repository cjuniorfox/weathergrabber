import logging
from time import sleep
from weathergrabber.adapter.repository.forecast_repository import ForecastRepository
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.output_enum import OutputEnum
from weathergrabber.adapter.client.weather_api import WeatherApi
from weathergrabber.adapter.client.weather_search_api import WeatherSearchApi
from .services.search_location_service import SearchLocationService
from .services.read_weather_service import ReadWeatherService
from .services.retrieve_forecast_from_cache_service import RetrieveForecastFromCacheService
from .services.save_forecast_to_cache_service import SaveForecastToCacheService
from .services.extract_current_conditions_service import ExtractCurrentConditionsService
from .services.extract_today_details_service import ExtractTodayDetailsService
from .services.extract_aqi_service import ExtractAQIService
from .services.extract_health_activities_service import ExtractHealthActivitiesService
from .services.extract_hourly_forecast_service import ExtractHourlyForecastService
from .services.extract_hourly_forecast_oldstyle_service import ExtractHourlyForecastOldstyleService
from .services.extract_daily_forecast_service import ExtractDailyForecastService
from .services.extract_daily_forecast_oldstyle_service import ExtractDailyForecastOldstyleService
from .usecases.weather_forecast_uc import WeatherForecastUC


class WeatherGrabberApplication:

    def _beans(self):
        self.weather_search_api = WeatherSearchApi()
        self.weather_api = WeatherApi()
        self.forecast_repository = ForecastRepository()
        self.search_location_service = SearchLocationService(self.weather_search_api)
        self.read_weather_service = ReadWeatherService(self.weather_api)
        self.extract_current_conditions_service = ExtractCurrentConditionsService()
        self.extract_today_details_service = ExtractTodayDetailsService()
        self.extract_aqi_service = ExtractAQIService()
        self.extract_health_activities_service = ExtractHealthActivitiesService()
        self.extract_hourly_forecast_service = ExtractHourlyForecastService()
        self.extract_hourly_forecast_oldstyle_service = ExtractHourlyForecastOldstyleService()
        self.extract_daily_forecast_service = ExtractDailyForecastService()
        self.extract_daily_forecast_oldstyle_service = ExtractDailyForecastOldstyleService()
        self.retrieve_forecast_from_cache_service = RetrieveForecastFromCacheService(self.forecast_repository)
        self.save_forecast_to_cache_service = SaveForecastToCacheService(self.forecast_repository)
        self.weather_forecast_uc = WeatherForecastUC(
                self.search_location_service,
                self.read_weather_service,
                self.extract_current_conditions_service,
                self.extract_today_details_service,
                self.extract_aqi_service,
                self.extract_health_activities_service,
                self.extract_hourly_forecast_service,
                self.extract_hourly_forecast_oldstyle_service,
                self.extract_daily_forecast_service,
                self.extract_daily_forecast_oldstyle_service,
                self.retrieve_forecast_from_cache_service,
                self.save_forecast_to_cache_service
            )
        pass
        
    def _define_controller(self, output_format: OutputEnum):
        if output_format == OutputEnum.CONSOLE:
            from weathergrabber.adapter.tty.console_tty import ConsoleTTY
            self.controller = ConsoleTTY(self.weather_forecast_uc)

        elif output_format == OutputEnum.JSON:
            from weathergrabber.adapter.tty.json_tty import JsonTTY
            self.controller = JsonTTY(self.weather_forecast_uc)

        elif output_format == OutputEnum.WAYBAR:
            from weathergrabber.adapter.tty.waybar_tty import WaybarTTY
            self.controller = WaybarTTY(self.weather_forecast_uc)

        elif output_format == OutputEnum.STATISTICS:
            from weathergrabber.adapter.tty.statistics_tty import StatisticsTTY
            self.controller = StatisticsTTY(self.weather_forecast_uc)

        else:
            self.logger.error(f"Unsupported output format: {output_format}")
            raise ValueError(f"Unsupported output format: {output_format}")
        
    def __init__(self, params: Params):
        self.logger = logging.getLogger(__name__)
        self._beans()
        self._define_controller(params.output_format)
        self.logger.info("Starting WeatherGrabber Application")
        if params.keep_open:
            self.logger.info("Keep open mode enabled, the application will refresh every 5 minutes")
            while True:
                self.controller.execute(params)
                sleep(1)  # Sleep for 5 minutes
        else:
            self.controller.execute(params)
        self.logger.info("WeatherGrabber Application finished")