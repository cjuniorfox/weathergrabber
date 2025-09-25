import pytest
from unittest.mock import MagicMock, patch
from weathergrabber.service.extract_hourly_forecast_service import ExtractHourlyForecastService
from weathergrabber.domain.hourly_predictions import HourlyPredictions

@patch('weathergrabber.domain.hourly_predictions.HourlyPredictions')
@patch('weathergrabber.domain.weather_icon_enum.WeatherIconEnum.from_name', return_value='icon')
@patch('weathergrabber.domain.precipitation.Precipitation', return_value='precip')
@patch('weathergrabber.domain.wind.Wind.from_string', return_value='wind')
@patch('weathergrabber.domain.uv_index.UVIndex.from_string', return_value='uv')
@patch('weathergrabber.service.extract_hourly_forecast_service.PyQuery')
def test_execute_success(mock_uv, mock_wind, mock_precip, mock_icon, mock_hourly, mock_pyquery_cls):

    mock_pq_instance = MagicMock()

    mock_find = MagicMock()
    mock_find.text.return_value = "Now"
    mock_find.attr.return_value = "cloudy"
    mock_find.next.eq.text.return_value = "S"
    mock_find.next.text.return_value = "some-text"


    mock_pyquery_cls.find.side_effect = mock_find
    mock_pyquery_cls.return_value = mock_pq_instance

    mock_pyquery = MagicMock()
    mock_data = [MagicMock(), MagicMock()]
    mock_pyquery.find.return_value = mock_data
    
    service = ExtractHourlyForecastService()
    result = service.execute(mock_pyquery)
    assert mock_hourly.call_count == 2
    assert isinstance(result, list)

def test_execute_empty():
    mock_pyquery = MagicMock()
    mock_pyquery.find.return_value = []
    service = ExtractHourlyForecastService()
    with pytest.raises(ValueError, match="Could not extract hourly forecast."):
        service.execute(mock_pyquery)

def test_execute_exception():
    mock_pyquery = MagicMock()
    mock_pyquery.find.side_effect = Exception("fail")
    service = ExtractHourlyForecastService()
    with pytest.raises(ValueError, match="Could not extract hourly forecast."):
        service.execute(mock_pyquery)
