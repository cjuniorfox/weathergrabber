import pytest
from unittest.mock import MagicMock
from weathergrabber.service.extract_feelslike_temperature_service import ExtractFeelslikeTemperatureService

def test_execute_success():
    mock_pyquery = MagicMock()
    expected_temp = "25°C"
    mock_pyquery.return_value.text.return_value = expected_temp
    service = ExtractFeelslikeTemperatureService()
    result = service.execute(mock_pyquery)
    mock_pyquery.assert_called_with("span[class*='TodayDetailsCard--feelsLikeTempValue']")
    assert result == expected_temp

def test_execute_failure():
    mock_pyquery = MagicMock()
    mock_pyquery.return_value.text.side_effect = Exception("fail")
    service = ExtractFeelslikeTemperatureService()
    with pytest.raises(ValueError, match="Could not extract feels like temperature."):
        service.execute(mock_pyquery)
