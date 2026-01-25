import pytest
import logging
from unittest.mock import MagicMock
from weathergrabber.application.usecases.statistics_uc import StatisticsUC
from weathergrabber.domain.entities.statistics import Statistics
from weathergrabber.domain.adapter.params import Params


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.INFO)


@pytest.fixture
def mock_retrieve_statistics_service():
    """Fixture with mocked RetrieveStatisticsService."""
    service = MagicMock()
    return service


@pytest.fixture
def usecase(mock_retrieve_statistics_service):
    """Create a fresh StatisticsUC instance for each test."""
    return StatisticsUC(mock_retrieve_statistics_service)


@pytest.fixture
def params():
    """Create basic params for testing."""
    loc = Params.Location(id=None, search_name="TestSearch")
    return Params(location=loc, language="en")


def test_execute_returns_statistics(usecase, mock_retrieve_statistics_service, params):
    """Should return Statistics object from the service."""
    # Arrange
    expected_statistics = Statistics(
        total_forecasts=10,
        unique_locations=5,
        unique_search_names=3,
        database_path="/tmp/weather.db"
    )
    mock_retrieve_statistics_service.execute.return_value = expected_statistics
    
    # Act
    result = usecase.execute(params)
    
    # Assert
    assert result == expected_statistics
    assert result.total_forecasts == 10
    assert result.unique_locations == 5
    mock_retrieve_statistics_service.execute.assert_called_once()


def test_execute_calls_retrieve_statistics_service(usecase, mock_retrieve_statistics_service, params):
    """Should call the retrieve statistics service."""
    # Arrange
    expected_statistics = Statistics(
        total_forecasts=0,
        unique_locations=0,
        unique_search_names=0,
        database_path=""
    )
    mock_retrieve_statistics_service.execute.return_value = expected_statistics
    
    # Act
    usecase.execute(params)
    
    # Assert
    mock_retrieve_statistics_service.execute.assert_called_once()


def test_execute_logs_start_message(usecase, mock_retrieve_statistics_service, params, caplog):
    """Should log info message when execution starts."""
    # Arrange
    expected_statistics = Statistics(
        total_forecasts=0,
        unique_locations=0,
        unique_search_names=0,
        database_path=""
    )
    mock_retrieve_statistics_service.execute.return_value = expected_statistics
    
    # Act
    with caplog.at_level(logging.INFO):
        usecase.execute(params)
    
    # Assert
    assert "Executing StatisticsUC" in caplog.text
    assert "retrieve weather statistics" in caplog.text


def test_execute_logs_success_message(usecase, mock_retrieve_statistics_service, params, caplog):
    """Should log info message on successful execution."""
    # Arrange
    expected_statistics = Statistics(
        total_forecasts=5,
        unique_locations=2,
        unique_search_names=1,
        database_path="/tmp/weather.db"
    )
    mock_retrieve_statistics_service.execute.return_value = expected_statistics
    
    # Act
    with caplog.at_level(logging.INFO):
        usecase.execute(params)
    
    # Assert
    assert "Weather statistics retrieved successfully" in caplog.text


def test_execute_with_error_in_statistics(usecase, mock_retrieve_statistics_service, params):
    """Should return statistics even if it contains an error."""
    # Arrange
    error_statistics = Statistics(
        total_forecasts=0,
        unique_locations=0,
        unique_search_names=0,
        database_path="",
        error="Database error occurred"
    )
    mock_retrieve_statistics_service.execute.return_value = error_statistics
    
    # Act
    result = usecase.execute(params)
    
    # Assert
    assert result.error == "Database error occurred"


def test_execute_returns_statistics_with_zero_values(usecase, mock_retrieve_statistics_service, params):
    """Should handle and return statistics with zero values."""
    # Arrange
    zero_statistics = Statistics(
        total_forecasts=0,
        unique_locations=0,
        unique_search_names=0,
        database_path=""
    )
    mock_retrieve_statistics_service.execute.return_value = zero_statistics
    
    # Act
    result = usecase.execute(params)
    
    # Assert
    assert result.total_forecasts == 0
    assert result.unique_locations == 0
    assert result.unique_search_names == 0


def test_execute_returns_statistics_with_large_values(usecase, mock_retrieve_statistics_service, params):
    """Should handle and return statistics with large values."""
    # Arrange
    large_statistics = Statistics(
        total_forecasts=999999,
        unique_locations=50000,
        unique_search_names=100000,
        database_path="/tmp/large_db.db"
    )
    mock_retrieve_statistics_service.execute.return_value = large_statistics
    
    # Act
    result = usecase.execute(params)
    
    # Assert
    assert result.total_forecasts == 999999
    assert result.unique_locations == 50000
    assert result.unique_search_names == 100000


def test_execute_preserves_database_path(usecase, mock_retrieve_statistics_service, params):
    """Should preserve the database path from statistics."""
    # Arrange
    db_path = "/custom/path/to/weather.db"
    statistics = Statistics(
        total_forecasts=5,
        unique_locations=2,
        unique_search_names=1,
        database_path=db_path
    )
    mock_retrieve_statistics_service.execute.return_value = statistics
    
    # Act
    result = usecase.execute(params)
    
    # Assert
    assert result.database_path == db_path
