import pytest
from unittest.mock import MagicMock
from weathergrabber.application.services.read_weather_service import ReadWeatherService

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
