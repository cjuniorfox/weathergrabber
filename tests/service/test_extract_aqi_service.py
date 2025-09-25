import pytest
from unittest.mock import MagicMock, patch
from weathergrabber.service.extract_aqi_service import ExtractAQIService
from weathergrabber.domain.air_quality_index import AirQualityIndex

def test_execute_success():
    mock_weather_data = MagicMock()
    aqi_text = "26\nGood\nAir quality is considered satisfactory, and air pollution poses little or no risk."
    mock_weather_data.return_value.text.return_value = aqi_text
    expected_aqi = MagicMock()
    with patch.object(AirQualityIndex, "from_string", return_value=expected_aqi) as mock_from_string:
        service = ExtractAQIService()
        result = service.execute(mock_weather_data)
        mock_weather_data.assert_called_with("div[data-testid='AirQualityCard']")
        mock_from_string.assert_called_with(aqi_text)
        assert result == expected_aqi

def test_execute_none():
    mock_weather_data = MagicMock()
    mock_weather_data.return_value.text.return_value = ""
    with patch.object(AirQualityIndex, "from_string", return_value=None):
        service = ExtractAQIService()
        result = service.execute(mock_weather_data)
        assert result is None

def test_execute_exception():
    mock_weather_data = MagicMock()
    mock_weather_data.return_value.text.side_effect = Exception("fail")
    with patch.object(AirQualityIndex, "from_string", return_value=None):
        service = ExtractAQIService()
        with pytest.raises(ValueError, match="Could not extract AQI data"):
            service.execute(mock_weather_data)
