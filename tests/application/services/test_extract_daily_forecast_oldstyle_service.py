import pytest
from pyquery import PyQuery
from weathergrabber.domain.entities.daily_predictions import DailyPredictions
from weathergrabber.application.services.extract_daily_forecast_oldstyle_service import ExtractDailyForecastOldstyleService


HTML_SINGLE = """
<html>
  <body>
    <div class="DailyWeatherCard">
      <ul>
        <li>
          <h3><span>Monday</span></h3>
          <div data-testid="SegmentHighTemp">20°/10°</div>
          <svg name="sunny"></svg>
          <span class="Column--iconPhrase">Clear skies</span>
          <div data-testid="SegmentPrecipPercentage">
            <span class="Column--precip">Precip</span>
            <span class="Column--precip">10%</span>
          </div>
        </li>
      </ul>
    </div>
  </body>
</html>
"""

HTML_MULTIPLE = """
<html>
  <body>
    <div class="DailyWeatherCard">
      <ul>
        <li>
          <h3><span>Monday</span></h3>
          <div data-testid="SegmentHighTemp">20°/10°</div>
          <svg name="sunny"></svg>
          <span class="Column--iconPhrase">Clear skies</span>
          <div data-testid="SegmentPrecipPercentage">
            <span class="Column--precip">Precip</span>
            <span class="Column--precip">10%</span>
          </div>
        </li>
        <li>
          <h3><span>Tuesday</span></h3>
          <div data-testid="SegmentHighTemp">22°/12°</div>
          <svg name="rain"></svg>
          <span class="Column--iconPhrase">Light rain</span>
          <div data-testid="SegmentPrecipPercentage">
            <span class="Column--precip">Precip</span>
            <span class="Column--precip">60%</span>
          </div>
        </li>
      </ul>
    </div>
  </body>
</html>
"""


def test_execute_returns_single_prediction():
    service = ExtractDailyForecastOldstyleService()
    pq = PyQuery(HTML_SINGLE)

    results = service.execute(pq)

    assert isinstance(results, list)
    assert len(results) == 1

    dp = results[0]
    assert isinstance(dp, DailyPredictions)
    assert dp.title == "Monday"
    assert dp.summary == "Clear skies"
    # Precipitation is a domain object, check its percentage
    assert dp.precipitation.percentage == "10%"


def test_execute_returns_multiple_predictions():
    service = ExtractDailyForecastOldstyleService()
    pq = PyQuery(HTML_MULTIPLE)

    results = service.execute(pq)

    assert len(results) == 2
    titles = [dp.title for dp in results]
    assert "Monday" in titles
    assert "Tuesday" in titles
    assert results[1].summary == "Light rain"
    assert results[1].precipitation.percentage == "60%"


def test_execute_raises_on_missing_section():
    service = ExtractDailyForecastOldstyleService()
    pq = PyQuery("<html><body></body></html>")  # no DailyWeatherCard

    with pytest.raises(ValueError):
        service.execute(pq)
