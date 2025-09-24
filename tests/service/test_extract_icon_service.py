import pytest
from unittest.mock import MagicMock, patch
from weathergrabber.service.extract_icon_service import ExtractIconService
from weathergrabber.domain.weather_icon_enum import WeatherIconEnum

def test_execute_success():
    mock_pyquery = MagicMock()
    icon_name = "sunny"
    mock_pyquery.return_value.attr.return_value = icon_name
    expected_icon = WeatherIconEnum.SUNNY
    with patch.object(WeatherIconEnum, "from_name", return_value=expected_icon) as mock_from_name:
        service = ExtractIconService()
        result = service.execute(mock_pyquery)
        mock_pyquery.assert_called_with("div[class*='CurrentConditions--tempIconContainer'] svg[class*='CurrentConditions--wxIcon']")
        mock_from_name.assert_called_with(icon_name)
        assert result == expected_icon

def test_execute_unknown_icon():
    mock_pyquery = MagicMock()
    icon_name = "unknown_icon"
    mock_pyquery.return_value.attr.return_value = icon_name
    with patch.object(WeatherIconEnum, "from_name", return_value=None):
        service = ExtractIconService()
        with pytest.raises(ValueError, match="Could not extract icon."):
            service.execute(mock_pyquery)

def test_execute_exception():
    mock_pyquery = MagicMock()
    mock_pyquery.return_value.attr.side_effect = Exception("fail")
    with patch.object(WeatherIconEnum, "from_name", return_value=None):
        service = ExtractIconService()
        with pytest.raises(ValueError, match="Could not extract icon."):
            service.execute(mock_pyquery)
