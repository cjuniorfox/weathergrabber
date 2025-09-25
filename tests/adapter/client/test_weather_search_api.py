import pytest
from unittest.mock import patch, MagicMock
from weathergrabber.adapter.client.weather_search_api import WeatherSearchApi

def test_search_cache_hit():
    api = WeatherSearchApi()
    key = ("London", "en-US")
    api.cache[key] = {"cached": True}
    result = api.search("London", "en-US")
    assert result == {"cached": True}

def test_search_cache_miss_success():
    api = WeatherSearchApi()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "ok"}
    with patch("requests.post", return_value=mock_response) as mock_post:
        result = api.search("Paris", "fr-FR")
        assert result == {"result": "ok"}
        assert api.cache[("Paris", "fr-FR")] == {"result": "ok"}
        mock_post.assert_called_once()

def test_search_http_error():
    api = WeatherSearchApi()
    mock_response = MagicMock()
    mock_response.status_code = 404
    with patch("requests.post", return_value=mock_response):
        with pytest.raises(ValueError, match="HTTP error 404 when searching for location."):
            api.search("Berlin", "de-DE")

def test_search_invalid_location_name():
    api = WeatherSearchApi()
    with pytest.raises(ValueError, match="Location name must be provided and cannot be empty."):
        api.search("", "en-US")
    with pytest.raises(ValueError, match="Location name is too long."):
        api.search("x"*101, "en-US")
