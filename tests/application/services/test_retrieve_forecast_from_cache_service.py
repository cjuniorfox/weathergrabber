import pytest
from unittest.mock import Mock
from weathergrabber.application.services.retrieve_forecast_from_cache_service import RetrieveForecastFromCacheService
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.entities.forecast import Forecast
from weathergrabber.domain.entities.search import Search


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def service(mock_repo):
    return RetrieveForecastFromCacheService(mock_repo)


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


def test_execute_by_location_id_returns_forecast(service, mock_repo, forecast):
    params = Params(location=Params.Location(id="loc-123", search_name=None))
    mock_repo.get_by_location_id.return_value = forecast

    result = service.execute(params)

    assert result is forecast
    mock_repo.get_by_location_id.assert_called_once_with("loc-123")
    mock_repo.get_by_search_name.assert_not_called()


def test_execute_by_search_name_returns_forecast(service, mock_repo, forecast):
    params = Params(location=Params.Location(id=None, search_name="City"))
    mock_repo.get_by_search_name.return_value = forecast

    result = service.execute(params)

    assert result is forecast
    mock_repo.get_by_search_name.assert_called_once_with("City")
    mock_repo.get_by_location_id.assert_not_called()


def test_execute_missing_location_raises_value_error(service, mock_repo):
    params = Params(location=Params.Location(id=None, search_name=None))

    with pytest.raises(ValueError):
        service.execute(params)

    mock_repo.get_by_location_id.assert_not_called()
    mock_repo.get_by_search_name.assert_not_called()


def test_execute_not_found_raises_value_error(service, mock_repo):
    params = Params(location=Params.Location(id="loc-123", search_name=None))
    mock_repo.get_by_location_id.return_value = None

    with pytest.raises(ValueError):
        service.execute(params)

    mock_repo.get_by_location_id.assert_called_once_with("loc-123")
