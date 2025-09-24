import pytest
from unittest.mock import MagicMock, patch
from weathergrabber.service.extract_location_service import ExtractLocationService

class DummyCityLocation:
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        return isinstance(other, DummyCityLocation) and self.name == other.name
    def __repr__(self):
        return f"DummyCityLocation({self.name!r})"

@patch('weathergrabber.domain.city_location.CityLocation.from_string')
def test_execute_extracts_location(mock_from_string):
    # Arrange
    html_text = "Test City, State, Country"
    mock_pyquery = MagicMock()
    mock_pyquery.return_value.text.return_value = html_text
    expected_location = DummyCityLocation("Test City, State, Country")
    mock_from_string.return_value = expected_location
    service = ExtractLocationService()

    # Act
    result = service.execute(mock_pyquery)

    # Assert
    mock_pyquery.assert_called_with("h1[class*='CurrentConditions--location']")
    mock_from_string.assert_called_with(html_text)
    assert result == expected_location
