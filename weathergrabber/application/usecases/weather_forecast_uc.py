from typing import List
import logging

from requests.exceptions import ConnectionError
from weathergrabber.domain.adapter.params import Params
from weathergrabber.application.services.search_location_service import SearchLocationService
from weathergrabber.application.services.read_weather_service import ReadWeatherService
from weathergrabber.application.services.clear_cache_for_location_service import ClearCacheForLocationService
from weathergrabber.application.services.cleanup_old_forecasts_service import CleanupOldForecastsService
from weathergrabber.application.services.extract_current_conditions_service import ExtractCurrentConditionsService
from weathergrabber.application.services.extract_today_details_service import ExtractTodayDetailsService
from weathergrabber.application.services.extract_aqi_service import ExtractAQIService
from weathergrabber.application.services.extract_health_activities_service import ExtractHealthActivitiesService
from weathergrabber.application.services.extract_hourly_forecast_service import ExtractHourlyForecastService
from weathergrabber.application.services.extract_hourly_forecast_oldstyle_service import ExtractHourlyForecastOldstyleService
from weathergrabber.application.services.extract_daily_forecast_service import ExtractDailyForecastService
from weathergrabber.application.services.extract_daily_forecast_oldstyle_service import ExtractDailyForecastOldstyleService
from weathergrabber.application.services.retrieve_forecast_from_cache_service import RetrieveForecastFromCacheService
from weathergrabber.domain.entities.daily_predictions import DailyPredictions
from weathergrabber.domain.entities.hourly_predictions import HourlyPredictions
from weathergrabber.domain.entities.search import Search
from weathergrabber.domain.entities.forecast import Forecast
from weathergrabber.application.services.save_forecast_to_cache_service import SaveForecastToCacheService

class WeatherForecastUC:
    """Use case for retrieving weather forecast data."""
    
    # Constants for warning messages
    HOURLY_FORECAST_FALLBACK_MSG = "Falling back to new style hourly forecast extraction"
    DAILY_FORECAST_FALLBACK_MSG = "Falling back to new style daily forecast extraction"
    
    def __init__(
        self,
        search_location_service: SearchLocationService,
        read_weather_service: ReadWeatherService,
        extract_current_conditions_service: ExtractCurrentConditionsService,
        extract_today_details_service: ExtractTodayDetailsService,
        extract_aqi_service: ExtractAQIService,
        extract_health_activities_service: ExtractHealthActivitiesService,
        extract_hourly_forecast_service: ExtractHourlyForecastService,
        extract_hourly_forecast_oldstyle_service: ExtractHourlyForecastOldstyleService,
        extract_daily_forecast_service: ExtractDailyForecastService,
        extract_daily_forecast_oldstyle_service: ExtractDailyForecastOldstyleService,
        retrieve_forecast_from_cache_service: RetrieveForecastFromCacheService,
        save_forecast_to_cache_service: SaveForecastToCacheService,
        clear_cache_for_location_service: ClearCacheForLocationService,
        cleanup_old_forecasts_service: CleanupOldForecastsService
    ):
        self.logger = logging.getLogger(__name__)
        self.search_location_service = search_location_service
        self.read_weather_service = read_weather_service
        self.extract_current_conditions_service = extract_current_conditions_service
        self.extract_today_details_service = extract_today_details_service
        self.extract_aqi_service = extract_aqi_service
        self.extract_health_activities_service = extract_health_activities_service
        self.extract_hourly_forecast_service = extract_hourly_forecast_service
        self.extract_hourly_forecast_oldstyle_service = extract_hourly_forecast_oldstyle_service
        self.extract_daily_forecast_service = extract_daily_forecast_service
        self.extract_daily_forecast_oldstyle_service = extract_daily_forecast_oldstyle_service
        self.retrieve_forecast_from_cache_service = retrieve_forecast_from_cache_service
        self.save_forecast_to_cache_service = save_forecast_to_cache_service
        self.clear_cache_for_location_service = clear_cache_for_location_service
        self.cleanup_old_forecasts_service = cleanup_old_forecasts_service
    def execute(self, params: Params) -> Forecast:
        """Execute the weather forecast retrieval use case."""
        self.logger.debug("Starting weather forecast use case")

        if params.force_cache:
            return self.retrieve_forecast_from_cache_service.execute(params)
        
        try:
            location_id = self._resolve_location_id(params)
            weather_data = self.read_weather_service.execute(params.language, location_id)
        except ConnectionError as e:
            self.logger.debug("A connection error occurred while fetching weather data. Trying to retrieve from cache.")
            return self.retrieve_forecast_from_cache_service.execute(params)

        current_conditions = self.extract_current_conditions_service.execute(weather_data)
        today_details = self.extract_today_details_service.execute(weather_data)
        air_quality_index = self.extract_aqi_service.execute(weather_data)
        health_activities = self.extract_health_activities_service.execute(weather_data)
        
        hourly_predictions = self._extract_hourly_predictions(weather_data)
        daily_predictions = self._extract_daily_predictions(weather_data)

        forecast = Forecast(
            search=Search(id=location_id, search_name=params.location.search_name),
            current_conditions=current_conditions,
            today_details=today_details,
            air_quality_index=air_quality_index,
            health_activities=health_activities,
            hourly_predictions=hourly_predictions,
            daily_predictions=daily_predictions
        )

        self.clear_cache_for_location_service.execute(location_id)
        self.save_forecast_to_cache_service.execute(forecast)
        self.cleanup_old_forecasts_service.execute()

        self.logger.debug("Forecast data obtained successfully")
        return forecast
    
    def _resolve_location_id(self, params: Params) -> str:
        """Resolve location ID from params, searching if necessary."""
        location_id = params.location.id
        if not location_id:
            location_id = self.search_location_service.execute(
                params.location.search_name, 
                params.language
            )
        return location_id

    def _extract_hourly_predictions(self, weather_data) -> List[HourlyPredictions]:
        """Extract hourly predictions with fallback mechanism."""
        try:
            return self.extract_hourly_forecast_oldstyle_service.execute(weather_data)
        except ValueError:
            self.logger.warning(self.HOURLY_FORECAST_FALLBACK_MSG)
            return self.extract_hourly_forecast_service.execute(weather_data)

    def _extract_daily_predictions(self, weather_data) -> List[DailyPredictions]:
        """Extract daily predictions with fallback mechanism."""
        try:
            return self.extract_daily_forecast_oldstyle_service.execute(weather_data)
        except ValueError:
            self.logger.warning(self.DAILY_FORECAST_FALLBACK_MSG)
            return self.extract_daily_forecast_service.execute(weather_data)
