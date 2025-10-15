import pytest
from unittest.mock import patch, MagicMock
from weathergrabber.adapter.client.weather_api import WeatherApi
from urllib.error import HTTPError

@patch('weathergrabber.adapter.client.weather_api.PyQuery')
def test_get_weather_valid(mock_pyquery):
    mock_pyquery.return_value = "dummy"
    api = WeatherApi()
    result = api.get_weather("pt-BR", "a"*64)
    mock_pyquery.assert_called_with(url="https://weather.com/pt-BR/weather/today/l/{}".format("a"*64))
    assert result == "dummy"

def test_get_weather_invalid_location():
    api = WeatherApi()
    with pytest.raises(ValueError, match="Invalid location"):
        api.get_weather("pt-BR", "short")

def test_get_weather_no_language():
    api = WeatherApi()
    with pytest.raises(ValueError, match="language must be specified"):
        api.get_weather(None, "a"*64)

def test_get_weather_no_location():
    api = WeatherApi()
    with patch('weathergrabber.adapter.client.weather_api.PyQuery') as mock_pyquery:
        mock_pyquery.return_value = "dummy_no_location"
        result = api.get_weather("pt-BR", None)
        mock_pyquery.assert_called_with(url="https://weather.com/pt-BR/weather/today")
        assert result == "dummy_no_location"

@patch('weathergrabber.adapter.client.weather_api.PyQuery')
def test_get_weather_http_error(mock_pyquery):
    api = WeatherApi()
    mock_pyquery.side_effect = HTTPError("url", 404, "Not Found", None, None)
    with pytest.raises(ValueError, match="HTTP error 404 when fetching weather data."):
        api.get_weather("pt-BR", "a"*64)
