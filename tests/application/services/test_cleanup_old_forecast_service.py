import pytest
from weathergrabber.application.services.cleanup_old_forecasts_service import CleanupOldForecastsService
from unittest.mock import Mock

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def service(mock_repo):
    return CleanupOldForecastsService(mock_repo)

def test_cleanup_old_forecasts_service(service, mock_repo):
    hours_threshold = 24
    
    service.execute(hours_threshold)
    
    mock_repo.delete_old_forecasts.assert_called_once_with(hours_threshold=hours_threshold)

def test_cleanup_old_forecasts_service_exception(service, mock_repo, caplog):
    caplog.set_level("ERROR")
    
    mock_repo.delete_old_forecasts.side_effect = Exception("Database error")
    
    service.execute(24)
    
    assert "Error cleaning up old forecasts: Database error" in caplog.text