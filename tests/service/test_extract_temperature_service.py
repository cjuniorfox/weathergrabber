import pytest
from unittest.mock import MagicMock
from weathergrabber.service.extract_temperature_service import ExtractTemperatureService

def test_execute_success():
    mock_pyquery = MagicMock()
    expected_temp = "22°C"
    mock_pyquery.return_value.text.return_value = expected_temp
    service = ExtractTemperatureService()
    result = service.execute(mock_pyquery)
    mock_pyquery.assert_called_with("div[class*='CurrentConditions--tempIconContainer'] span[data-testid='TemperatureValue']")
    assert result == expected_temp

def test_execute_failure():
    mock_pyquery = MagicMock()
    mock_pyquery.return_value.text.side_effect = Exception("No temperature found")
    service = ExtractTemperatureService()
    with pytest.raises(ValueError, match="Could not extract temperature."):
        service.execute(mock_pyquery)
