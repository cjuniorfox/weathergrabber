import pytest
from unittest.mock import MagicMock, patch
from weathergrabber.service.extract_health_activities_service import ExtractHealthActivitiesService
from weathergrabber.domain.health_activities import HealthActivities

def test_execute_success():
    mock_pyquery = MagicMock()
    health_text = "Health & Activities\nGrass\nSeasonal Allergies and Pollen Count Forecast\nGrass pollen is low in your area"
    mock_pyquery.return_value.text.return_value = health_text
    expected_health = MagicMock()
    with patch.object(HealthActivities, "from_text", return_value=expected_health) as mock_from_text:
        service = ExtractHealthActivitiesService()
        result = service.execute(mock_pyquery)
        mock_pyquery.assert_called_with("section[data-testid='HealthAndActivitiesModule']")
        mock_from_text.assert_called_with(health_text)
        assert result == expected_health

def test_execute_none():
    mock_pyquery = MagicMock()
    mock_pyquery.return_value.text.return_value = ""
    with patch.object(HealthActivities, "from_text", return_value=None):
        service = ExtractHealthActivitiesService()
        result = service.execute(mock_pyquery)
        assert result is None

def test_execute_exception():
    mock_pyquery = MagicMock()
    mock_pyquery.return_value.text.side_effect = Exception("fail")
    with patch.object(HealthActivities, "from_text", return_value=None):
        service = ExtractHealthActivitiesService()
        with pytest.raises(ValueError, match="Could not extract Health & Activities data"):
            service.execute(mock_pyquery)
