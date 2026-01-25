import pytest
import logging
from unittest.mock import MagicMock, patch
from weathergrabber.application.services.retrieve_statistics_service import RetrieveStatisticsService
from weathergrabber.domain.entities.statistics import Statistics


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def mock_repository():
    """Fixture with mocked ForecastRepository."""
    repo = MagicMock()
    return repo


@pytest.fixture
def service(mock_repository):
    """Create a fresh RetrieveStatisticsService instance for each test."""
    return RetrieveStatisticsService(mock_repository)


def test_execute_returns_statistics_object(service, mock_repository):
    """Should return a Statistics object when valid data is retrieved from repository."""
    # Arrange
    mock_repository.get_cache_stats.return_value = {
        "total_forecasts": 10,
        "unique_locations": 5,
        "unique_search_names": 3,
        "database_path": "/tmp/weather.db"
    }
    
    # Act
    result = service.execute()
    
    # Assert
    assert isinstance(result, Statistics)
    assert result.total_forecasts == 10
    assert result.unique_locations == 5
    assert result.unique_search_names == 3
    assert result.database_path == "/tmp/weather.db"
    mock_repository.get_cache_stats.assert_called_once()


def test_execute_returns_statistics_with_error(service, mock_repository):
    """Should return a Statistics object with error when error is present in data."""
    # Arrange
    mock_repository.get_cache_stats.return_value = {
        "total_forecasts": 0,
        "unique_locations": 0,
        "unique_search_names": 0,
        "database_path": "",
        "error": "Database connection failed"
    }
    
    # Act
    result = service.execute()
    
    # Assert
    assert isinstance(result, Statistics)
    assert result.error == "Database connection failed"


def test_execute_handles_missing_optional_fields(service, mock_repository):
    """Should handle missing optional fields gracefully."""
    # Arrange
    mock_repository.get_cache_stats.return_value = {
        "total_forecasts": 5,
        "unique_locations": 2,
        "unique_search_names": 1,
        "database_path": "/tmp/weather.db"
        # error is not provided
    }
    
    # Act
    result = service.execute()
    
    # Assert
    assert result.error is None


def test_execute_calls_repository_get_cache_stats(service, mock_repository):
    """Should call repository's get_cache_stats method."""
    # Arrange
    mock_repository.get_cache_stats.return_value = {
        "total_forecasts": 0,
        "unique_locations": 0,
        "unique_search_names": 0,
        "database_path": ""
    }
    
    # Act
    service.execute()
    
    # Assert
    mock_repository.get_cache_stats.assert_called_once()


def test_execute_logs_retrieval_start(service, mock_repository, caplog):
    """Should log debug message at the start of execution."""
    # Arrange
    mock_repository.get_cache_stats.return_value = {
        "total_forecasts": 0,
        "unique_locations": 0,
        "unique_search_names": 0,
        "database_path": ""
    }
    
    # Act
    with caplog.at_level(logging.DEBUG):
        service.execute()
    
    # Assert
    assert "Retrieving statistics from repository" in caplog.text


def test_execute_logs_success(service, mock_repository, caplog):
    """Should log debug message on successful retrieval."""
    # Arrange
    mock_repository.get_cache_stats.return_value = {
        "total_forecasts": 8,
        "unique_locations": 3,
        "unique_search_names": 2,
        "database_path": "/tmp/weather.db"
    }
    
    # Act
    with caplog.at_level(logging.DEBUG):
        result = service.execute()
    
    # Assert
    assert "Statistics retrieved successfully" in caplog.text


def test_execute_with_zero_values(service, mock_repository):
    """Should handle statistics with zero values."""
    # Arrange
    mock_repository.get_cache_stats.return_value = {
        "total_forecasts": 0,
        "unique_locations": 0,
        "unique_search_names": 0,
        "database_path": "/tmp/empty.db"
    }
    
    # Act
    result = service.execute()
    
    # Assert
    assert result.total_forecasts == 0
    assert result.unique_locations == 0
    assert result.unique_search_names == 0


def test_execute_with_large_values(service, mock_repository):
    """Should handle statistics with large values."""
    # Arrange
    mock_repository.get_cache_stats.return_value = {
        "total_forecasts": 1000000,
        "unique_locations": 50000,
        "unique_search_names": 100000,
        "database_path": "/tmp/large.db"
    }
    
    # Act
    result = service.execute()
    
    # Assert
    assert result.total_forecasts == 1000000
    assert result.unique_locations == 50000
    assert result.unique_search_names == 100000
