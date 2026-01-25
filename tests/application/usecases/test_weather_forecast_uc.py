import pytest
from unittest.mock import MagicMock
from requests.exceptions import ConnectionError
from weathergrabber.domain.entities.forecast import Forecast
from weathergrabber.domain.entities.search import Search
from weathergrabber.domain.adapter.params import Params
from weathergrabber.application.usecases.weather_forecast_uc import WeatherForecastUC


@pytest.fixture
def mock_services():
    """Fixture with all services mocked."""
    return {
        "search_location_service": MagicMock(),
        "read_weather_service": MagicMock(),
        "extract_current_conditions_service": MagicMock(),
        "extract_today_details_service": MagicMock(),
        "extract_aqi_service": MagicMock(),
        "extract_health_activities_service": MagicMock(),
        "extract_hourly_forecast_service": MagicMock(),
        "extract_hourly_forecast_oldstyle_service": MagicMock(),
        "extract_daily_forecast_service": MagicMock(),
        "extract_daily_forecast_oldstyle_service": MagicMock(),
        "retrieve_forecast_from_cache_service": MagicMock(),
        "save_forecast_to_cache_service": MagicMock()
    }


@pytest.fixture
def usecase(mock_services):
    """Create a fresh use case instance for each test."""
    return WeatherForecastUC(**mock_services)


@pytest.fixture
def params():
    loc = Params.Location(id=None, search_name="TestSearch")
    return Params(location=loc, language="en")


def test_execute_happy_path(usecase, mock_services, params):
    # Arrange
    mock_services["search_location_service"].execute.return_value = "12345"
    mock_services["read_weather_service"].execute.return_value = "<html>weather</html>"
    mock_services["extract_current_conditions_service"].execute.return_value = "CurrentConditions"
    mock_services["extract_today_details_service"].execute.return_value = "details"
    mock_services["extract_aqi_service"].execute.return_value = "good"
    mock_services["extract_health_activities_service"].execute.return_value = "running"
    mock_services["extract_hourly_forecast_oldstyle_service"].execute.return_value = ["hour1", "hour2"]
    mock_services["extract_daily_forecast_oldstyle_service"].execute.return_value = ["day1", "day2"]
    mock_services["retrieve_forecast_from_cache_service"].execute.return_value = None
    mock_services["save_forecast_to_cache_service"].execute.return_value = None

    # Act
    forecast = usecase.execute(params)

    # Assert
    assert isinstance(forecast, Forecast)
    assert forecast.current_conditions == "CurrentConditions"
    assert forecast.today_details == "details"
    assert forecast.air_quality_index == "good"
    assert forecast.health_activities == "running"
    assert forecast.search.id == "12345"
    assert forecast.hourly_predictions == ["hour1", "hour2"]
    assert forecast.daily_predictions == ["day1", "day2"]


def test_execute_fallback_hourly(usecase, mock_services, params):
    # Hourly forecast raises -> fallback to forecast service
    mock_services["search_location_service"].execute.return_value = "12345"
    mock_services["read_weather_service"].execute.return_value = "<html>weather</html>"
    mock_services["extract_current_conditions_service"].execute.return_value = "CurrentConditions"
    mock_services["extract_today_details_service"].execute.return_value = "details"
    mock_services["extract_aqi_service"].execute.return_value = "good"
    mock_services["extract_health_activities_service"].execute.return_value = "running"
    mock_services["extract_hourly_forecast_oldstyle_service"].execute.side_effect = ValueError("fail hourly")
    mock_services["extract_hourly_forecast_service"].execute.return_value = ["hour_old"]
    mock_services["extract_daily_forecast_service"].execute.return_value = ["day1"]
    mock_services["retrieve_forecast_from_cache_service"].execute.return_value = None
    mock_services["save_forecast_to_cache_service"].execute.return_value = None

    forecast = usecase.execute(params)

    assert forecast.hourly_predictions == ["hour_old"]


def test_execute_fallback_daily(usecase, mock_services, params):
    # Daily forecast raises -> fallback to forecast service
    mock_services["search_location_service"].execute.return_value = "12345"
    mock_services["read_weather_service"].execute.return_value = "<html>weather</html>"
    mock_services["extract_current_conditions_service"].execute.return_value = "CurrentConditions"
    mock_services["extract_today_details_service"].execute.return_value = "details"
    mock_services["extract_aqi_service"].execute.return_value = "good"
    mock_services["extract_health_activities_service"].execute.return_value = "running"
    mock_services["extract_hourly_forecast_service"].execute.return_value = ["hour1"]
    mock_services["extract_daily_forecast_oldstyle_service"].execute.side_effect = ValueError("fail daily")
    mock_services["extract_daily_forecast_service"].execute.return_value = ["day_old"]
    mock_services["retrieve_forecast_from_cache_service"].execute.return_value = None
    mock_services["save_forecast_to_cache_service"].execute.return_value = None

    forecast = usecase.execute(params)

    assert forecast.daily_predictions == ["day_old"]


def test_execute_force_cache(usecase, mock_services, params):
    # Should return cached forecast when force_cache is True
    cached_forecast = Forecast(
        search=Search(id="cached_id", search_name="TestSearch"),
        current_conditions="CachedConditions",
        today_details="CachedDetails",
        air_quality_index="CachedAQI",
        health_activities="CachedHealth",
        hourly_predictions=["h1"],
        daily_predictions=["d1"],
    )
    params_force_cache = Params(location=params.location, language=params.language, force_cache=True)
    mock_services["retrieve_forecast_from_cache_service"].execute.return_value = cached_forecast

    result = usecase.execute(params_force_cache)

    assert result is cached_forecast
    mock_services["retrieve_forecast_from_cache_service"].execute.assert_called_once_with(params_force_cache)
    mock_services["read_weather_service"].execute.assert_not_called()
    mock_services["save_forecast_to_cache_service"].execute.assert_not_called()


def test_execute_connection_error_returns_cache(usecase, mock_services, params):
    # If resolving location raises ConnectionError, should return cache
    cached_forecast = Forecast(
        search=Search(id="cached_id", search_name="TestSearch"),
        current_conditions="CachedConditions",
        today_details="CachedDetails",
        air_quality_index="CachedAQI",
        health_activities="CachedHealth",
        hourly_predictions=["h1"],
        daily_predictions=["d1"],
    )
    mock_services["search_location_service"].execute.side_effect = ConnectionError("network down")
    mock_services["retrieve_forecast_from_cache_service"].execute.return_value = cached_forecast

    result = usecase.execute(params)

    assert result is cached_forecast
    mock_services["retrieve_forecast_from_cache_service"].execute.assert_called_once_with(params)
    mock_services["read_weather_service"].execute.assert_not_called()
    mock_services["save_forecast_to_cache_service"].execute.assert_not_called()
