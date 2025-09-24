import pytest
from unittest.mock import MagicMock
from weathergrabber.service.read_weather_service import ReadWeatherService

class DummyPyQuery:
    pass

def test_execute_with_explicit_language_and_location(monkeypatch):
    mock_api = MagicMock()
    expected_result = DummyPyQuery()
    mock_api.get_weather.return_value = expected_result
    service = ReadWeatherService(mock_api)

    result = service.execute("pt-BR", "abcdef123456")

    mock_api.get_weather.assert_called_with("pt-BR", "abcdef123456")
    assert result == expected_result

def test_execute_with_env_defaults(monkeypatch):
    mock_api = MagicMock()
    expected_result = DummyPyQuery()
    mock_api.get_weather.return_value = expected_result
    service = ReadWeatherService(mock_api)
    monkeypatch.setenv("LANG", "fr_FR.UTF-8")
    monkeypatch.setenv("WEATHER_LOCATION_ID", "locationid123")

    result = service.execute(None, None)

    mock_api.get_weather.assert_called_with("fr-FR", "locationid123")
    assert result == expected_result
