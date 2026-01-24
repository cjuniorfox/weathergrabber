import pytest
from unittest.mock import Mock
from weathergrabber.application.services.save_forecast_to_cache_service import SaveForecastToCacheService
from weathergrabber.domain.entities.forecast import Forecast
from weathergrabber.domain.entities.search import Search


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def service(mock_repo):
    return SaveForecastToCacheService(mock_repo)


@pytest.fixture
def forecast():
    return Forecast(
        search=Search(id="loc-123", search_name="City"),
        current_conditions=None,
        today_details=None,
        air_quality_index=None,
        health_activities=None,
        hourly_predictions=[],
        daily_predictions=[],
    )


def test_execute_saves_forecast(service, mock_repo, forecast, caplog):
    caplog.set_level("INFO")

    service.execute(forecast)

    mock_repo.save_forecast.assert_called_once_with(
        location_id="loc-123",
        search_name="City",
        forecast_data=forecast,
    )
    assert "Saving forecast to cache" in caplog.text


def test_execute_logs_success(service, mock_repo, forecast, caplog):
    caplog.set_level("DEBUG")

    service.execute(forecast)

    assert "Forecast saved to cache successfully" in caplog.text
