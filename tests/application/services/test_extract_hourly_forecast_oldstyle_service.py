import pytest
import logging
from pyquery import PyQuery
from weathergrabber.application.services.extract_hourly_forecast_oldstyle_service import ExtractHourlyForecastOldstyleService
from weathergrabber.domain.entities.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.entities.precipitation import Precipitation

logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def service():
    return ExtractHourlyForecastOldstyleService()

def test_execute_success(service):
    html = """
    <html>
      <body>
        <div class="TodayWeatherCard">
          <ul>
            <li>
              <h3><span>10 AM</span></h3>
              <span data-testid="TemperatureValue">22°</span>
              <svg name="sunny"></svg>
              <span class="Column--iconPhrase">Clear skies</span>
              <div data-testid="SegmentPrecipPercentage">
                <span class="Column--precip">💧</span>
                <span class="Column--precip">15%</span>
              </div>
            </li>
          </ul>
        </div>
      </body>
    </html>
    """
    pq = PyQuery(html)
    results = service.execute(pq)

    assert len(results) == 1
    forecast = results[0]
    assert forecast.title == "10 AM"
    assert forecast.temperature == "22°"
    assert forecast.icon == WeatherIconEnum.from_name("sunny")
    assert forecast.summary == "Clear skies"
    assert isinstance(forecast.precipitation, Precipitation)
    assert forecast.precipitation.percentage == "15%"

def test_execute_empty(service):
    html = "<html><body><div class='Malformed'><ul></ul></div></body></html>"
    pq = PyQuery(html)

    with pytest.raises(ValueError, match="Could not extract hourly forecast."):
        service.execute(pq)