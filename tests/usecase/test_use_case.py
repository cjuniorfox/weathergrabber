import pytest
from unittest.mock import MagicMock
from weathergrabber.domain.forecast import Forecast
from weathergrabber.domain.search import Search
from weathergrabber.domain.adapter.params import Params
from weathergrabber.usecase.use_case import UseCase


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
    }


@pytest.fixture
def usecase(mock_services):
    return UseCase(**mock_services)


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
    mock_services["extract_hourly_forecast_service"].execute.return_value = ["hour1", "hour2"]
    mock_services["extract_daily_forecast_service"].execute.return_value = ["day1", "day2"]

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
    # Hourly forecast raises -> fallback to oldstyle
    mock_services["search_location_service"].execute.return_value = "12345"
    mock_services["read_weather_service"].execute.return_value = "<html>weather</html>"
    mock_services["extract_current_conditions_service"].execute.return_value = "CurrentConditions"
    mock_services["extract_today_details_service"].execute.return_value = "details"
    mock_services["extract_aqi_service"].execute.return_value = "good"
    mock_services["extract_health_activities_service"].execute.return_value = "running"

    mock_services["extract_hourly_forecast_service"].execute.side_effect = ValueError("fail hourly")
    mock_services["extract_hourly_forecast_oldstyle_service"].execute.return_value = ["hour_old"]
    mock_services["extract_daily_forecast_service"].execute.return_value = ["day1"]

    forecast = usecase.execute(params)

    assert forecast.hourly_predictions == ["hour_old"]


def test_execute_fallback_daily(usecase, mock_services, params):
    # Daily forecast raises -> fallback to oldstyle
    mock_services["search_location_service"].execute.return_value = "12345"
    mock_services["read_weather_service"].execute.return_value = "<html>weather</html>"
    mock_services["extract_current_conditions_service"].execute.return_value = "CurrentConditions"
    mock_services["extract_today_details_service"].execute.return_value = "details"
    mock_services["extract_aqi_service"].execute.return_value = "good"
    mock_services["extract_health_activities_service"].execute.return_value = "running"

    mock_services["extract_hourly_forecast_service"].execute.return_value = ["hour1"]
    mock_services["extract_daily_forecast_service"].execute.side_effect = ValueError("fail daily")
    mock_services["extract_daily_forecast_oldstyle_service"].execute.return_value = ["day_old"]

    forecast = usecase.execute(params)

    assert forecast.daily_predictions == ["day_old"]
