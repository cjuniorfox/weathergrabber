import logging
from weathergrabber.domain.adapter.params import Params
from weathergrabber.service.search_location_service import SearchLocationService
from weathergrabber.service.read_weather_service import ReadWeatherService
from weathergrabber.service.extract_current_conditions_service import ExtractCurrentConditionsService
from weathergrabber.service.extract_today_details_service import ExtractTodayDetailsService
from weathergrabber.service.extract_aqi_service import ExtractAQIService
from weathergrabber.service.extract_health_activities_service import ExtractHealthActivitiesService
from weathergrabber.service.extract_hourly_forecast_service import ExtractHourlyForecastService
from weathergrabber.service.extract_hourly_forecast_oldstyle_service import ExtractHourlyForecastOldstyleService
from weathergrabber.service.extract_daily_forecast_service import ExtractDailyForecastService
from weathergrabber.service.extract_daily_forecast_oldstyle_service import ExtractDailyForecastOldstyleService
from weathergrabber.domain.search import Search
from weathergrabber.domain.forecast import Forecast

class UseCase:
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

    def execute(self, params: Params) -> Forecast:
        """Execute the weather forecast retrieval use case."""
        self.logger.debug("Starting weather forecast use case")

        location_id = self._resolve_location_id(params)
        weather_data = self.read_weather_service.execute(params.language, location_id)
        
        basic_weather_data = self._extract_basic_weather_data(weather_data)
        hourly_predictions = self._extract_hourly_predictions(weather_data)
        daily_predictions = self._extract_daily_predictions(weather_data)

        forecast = self._build_forecast(
            location_id=location_id,
            search_name=params.location.search_name,
            basic_data=basic_weather_data,
            hourly_predictions=hourly_predictions,
            daily_predictions=daily_predictions
        )

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

    def _extract_basic_weather_data(self, weather_data) -> dict:
        """Extract basic weather information."""
        return {
            'current_conditions': self.extract_current_conditions_service.execute(weather_data),
            'today_details': self.extract_today_details_service.execute(weather_data),
            'air_quality_index': self.extract_aqi_service.execute(weather_data),
            'health_activities': self.extract_health_activities_service.execute(weather_data),
        }

    def _extract_hourly_predictions(self, weather_data):
        """Extract hourly predictions with fallback mechanism."""
        try:
            return self.extract_hourly_forecast_oldstyle_service.execute(weather_data)
        except ValueError:
            self.logger.warning(self.HOURLY_FORECAST_FALLBACK_MSG)
            return self.extract_hourly_forecast_service.execute(weather_data)

    def _extract_daily_predictions(self, weather_data):
        """Extract daily predictions with fallback mechanism."""
        try:
            return self.extract_daily_forecast_oldstyle_service.execute(weather_data)
        except ValueError:
            self.logger.warning(self.DAILY_FORECAST_FALLBACK_MSG)
            return self.extract_daily_forecast_service.execute(weather_data)

    def _build_forecast(self, location_id: str, search_name: str, basic_data: dict, 
                       hourly_predictions, daily_predictions) -> Forecast:
        """Build the final forecast object."""
        return Forecast(
            search=Search(id=location_id, search_name=search_name),
            current_conditions=basic_data['current_conditions'],
            today_details=basic_data['today_details'],
            air_quality_index=basic_data['air_quality_index'],
            health_activities=basic_data['health_activities'],
            hourly_predictions=hourly_predictions,
            daily_predictions=daily_predictions
        )