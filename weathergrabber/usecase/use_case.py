from weathergrabber.domain.adapter.params import Params
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
from weathergrabber.service.extract_hourly_forecast_oldstyle_service import ExtractHourlyForecastOldstyleService
from weathergrabber.service.extract_daily_forecast_service import ExtractDailyForecastService
from weathergrabber.service.extract_daily_forecast_oldstyle_service import ExtractDailyForecastOldstyleService


class UseCase:
    def __init__(
        self,
        search_location_service: SearchLocationService,
        read_weather_service: ReadWeatherService,
        extract_location_service: ExtractLocationService,
        extract_temperature_icon_service: ExtractTemperatureService,
        extract_feelslike_temperature_service: ExtractFeelslikeTemperatureService,
        extract_icon_service: ExtractIconService,
        extract_today_details_service: ExtractTodayDetailsService,
        extract_aqi_service: ExtractAQIService,
        extract_health_activities_service: ExtractHealthActivitiesService,
        extract_hourly_forecast_service: ExtractHourlyForecastService,
        extract_hourly_forecast_oldstyle_service: ExtractHourlyForecastOldstyleService,
        extract_daily_forecast_service: ExtractDailyForecastService,
        extract_daily_forecast_oldstyle_service: ExtractDailyForecastOldstyleService,

    ):
        self.read_weather_service = read_weather_service
        self.extract_location_service = extract_location_service
        self.extract_temperature_service = extract_temperature_icon_service
        self.extract_feelslike_temperature_service = extract_feelslike_temperature_service
        self.extract_icon_service = extract_icon_service
        self.extract_today_details_service = extract_today_details_service
        self.search_location_service = search_location_service
        self.extract_aqi_service = extract_aqi_service
        self.extract_health_activities_service = extract_health_activities_service
        self.extract_hourly_forecast_service = extract_hourly_forecast_service
        self.extract_hourly_forecast_oldstyle_service = extract_hourly_forecast_oldstyle_service
        self.extract_daily_forecast_service = extract_daily_forecast_service
        self.extract_daily_forecast_oldstyle_service = extract_daily_forecast_oldstyle_service

    def execute(self, params: Params) -> None:

        location_id = params.location.id
        if not location_id:
            location_id = self.search_location_service.execute(params.location.name, params.language)

        weather_data = self.read_weather_service.execute(params.language, location_id)
        
        location = self.extract_location_service.execute(weather_data)
        temperature = self.extract_temperature_service.execute(weather_data)
        feelslike_temperature = self.extract_feelslike_temperature_service.execute(weather_data)
        icon = self.extract_icon_service.execute(weather_data)
        today_details = self.extract_today_details_service.execute(weather_data)
        air_quality_index = self.extract_aqi_service.execute(weather_data)
        health_activities = self.extract_health_activities_service.execute(weather_data)
        
        try:
            hourly_forecast = self.extract_hourly_forecast_service.execute(weather_data)
        except ValueError:
            hourly_forecast = self.extract_hourly_forecast_oldstyle_service.execute(weather_data)
        
        try:
            daily_forecast = self.extract_daily_forecast_service.execute(weather_data)
        except ValueError:
            daily_forecast = self.extract_daily_forecast_oldstyle_service.execute(weather_data)
        