import pytest
import logging
from pyquery import PyQuery
from weathergrabber.application.services.extract_temperature_service import ExtractTemperatureService


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.DEBUG)


def test_execute_returns_temperature_on_valid_html():
    """Should return temperature string when valid temperature data is provided."""
    html = """
    <div class="CurrentConditions--tempIconContainer">
        <span data-testid="TemperatureValue">72°F</span>
    </div>
    """
    doc = PyQuery(html)
    
    service = ExtractTemperatureService()
    result = service.execute(doc)
    
    assert result == "72°F"


def test_execute_returns_empty_string_on_missing_temperature():
    """Should return empty string when temperature element is not found."""
    html = "<div>No temperature data here</div>"
    doc = PyQuery(html)
    
    service = ExtractTemperatureService()
    result = service.execute(doc)
    
    assert result == ""


def test_execute_handles_different_temperature_formats():
    """Should handle various temperature formats and units."""
    test_cases = [
        ("68°C", "68°C"),
        ("32°F", "32°F"),
        ("20.5°C", "20.5°C"),
    ]
    
    for temp_value, expected in test_cases:
        html = f"""
        <div class="CurrentConditions--tempIconContainer">
            <span data-testid="TemperatureValue">{temp_value}</span>
        </div>
        """
        doc = PyQuery(html)
        
        service = ExtractTemperatureService()
        result = service.execute(doc)
        
        assert result == expected


def test_execute_raises_value_error_on_exception(monkeypatch):
    """Should raise ValueError when an exception occurs during extraction."""
    doc = PyQuery("<div>Test</div>")
    
    service = ExtractTemperatureService()
    
    # Mock the text() method to raise an exception
    def mock_text(*args, **kwargs):
        raise RuntimeError("Unexpected error")
    
    monkeypatch.setattr(PyQuery, "text", mock_text)
    
    with pytest.raises(ValueError, match="Could not extract temperature"):
        service.execute(doc)


def test_execute_logs_extracted_temperature(caplog):
    """Should log the extracted temperature at DEBUG level."""
    html = """
    <div class="CurrentConditions--tempIconContainer">
        <span data-testid="TemperatureValue">75°F</span>
    </div>
    """
    doc = PyQuery(html)
    
    service = ExtractTemperatureService()
    
    with caplog.at_level(logging.DEBUG):
        result = service.execute(doc)
    
    assert "Extracted temperature: 75°F" in caplog.text


def test_execute_logs_error_on_failure(caplog):
    """Should log error message when extraction fails."""
    doc = PyQuery("<div>Test</div>")
    
    service = ExtractTemperatureService()
    
    # Mock the text() method to raise an exception
    import pyquery
    original_text = PyQuery.text
    
    def mock_text(self):
        raise RuntimeError("Test error")
    
    PyQuery.text = mock_text
    
    try:
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                service.execute(doc)
        
        assert "Error temperature" in caplog.text
    finally:
        PyQuery.text = original_text
