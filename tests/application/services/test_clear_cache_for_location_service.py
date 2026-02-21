import pytest
from weathergrabber.application.services.clear_cache_for_location_service import ClearCacheForLocationService
from unittest.mock import Mock


@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def service(mock_repo):
    return ClearCacheForLocationService(mock_repo)
    
def test_clear_cache_for_location_service(service, mock_repo):
    location_id = "loc-123"
    
    service.execute(location_id)
    
    mock_repo.clear_cache_for_location.assert_called_once_with(location_id)
    
def test_clear_cache_for_location_service_no_location_id(service, mock_repo, caplog):
    caplog.set_level("WARNING")
    
    service.execute("")
    
    mock_repo.clear_cache_for_location.assert_not_called()
    assert "No location_id provided, skipping cache clear" in caplog.text