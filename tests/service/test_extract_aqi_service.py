import pytest
import logging
from pyquery import PyQuery
from weathergrabber.service.extract_aqi_service import ExtractAQIService
from weathergrabber.domain.air_quality_index import AirQualityIndex
from weathergrabber.domain.color import Color


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.DEBUG)


def test_execute_returns_air_quality_index(monkeypatch):
    """Should return an AirQualityIndex object when valid AQI and color data are provided."""

    html = """
    <section data-testid="AirQualityModule">
        Air Quality Index
        27
        Good
        Air quality is considered satisfactory, and air pollution poses little or no risk.
        <svg data-testid="DonutChart">
            <circle></circle>
            <circle style="stroke-width:5;stroke-dasharray:10.02 172.78;stroke:#00E838"></circle>
        </svg>
    </section>
    """
    doc = PyQuery(html)

    expected_aqi = AirQualityIndex(title="Air Quality Index", value=27, category="Good", acronym="AQI", color=Color("00","E8","38"))

    def fake_aqi_color_from_string(aqi_data, color_data):
        assert "Air Quality Index" in aqi_data
        assert "#00E838" in color_data
        return expected_aqi

    monkeypatch.setattr(AirQualityIndex, "aqi_color_from_string", staticmethod(fake_aqi_color_from_string))

    service = ExtractAQIService()
    result = service.execute(doc)

    assert result == expected_aqi


def test_execute_raises_value_error_on_missing_section():
    """Should raise ValueError if AQI section is not found in the HTML."""
    doc = PyQuery("<div>No AQI data here</div>")
    service = ExtractAQIService()

    with pytest.raises(ValueError, match="Could not extract AQI data"):
        service.execute(doc)


def test_execute_raises_value_error_on_invalid_style(monkeypatch):
    """Should raise ValueError if color_data is invalid or missing."""
    html = """
    <section data-testid="AirQualityModule">
        Air Quality Index
        50
        Moderate
        <svg data-testid="DonutChart">
            <circle></circle>
            <circle></circle> <!-- missing style -->
        </svg>
    </section>
    """
    doc = PyQuery(html)

    def fake_aqi_color_from_string(aqi_data, color_data):
        raise ValueError("Invalid color string")

    monkeypatch.setattr(AirQualityIndex, "aqi_color_from_string", staticmethod(fake_aqi_color_from_string))

    service = ExtractAQIService()
    with pytest.raises(ValueError, match="Could not extract AQI data"):
        service.execute(doc)