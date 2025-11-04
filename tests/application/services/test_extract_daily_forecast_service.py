import pytest
from pyquery import PyQuery
from weathergrabber.domain.entities.daily_predictions import DailyPredictions
from weathergrabber.application.services.extract_daily_forecast_service import ExtractDailyForecastService


HTML_SINGLE = """
<html>
<body>
<section data-testid="DailyForecast">
  <div class="Card">
    <details>
      <h2 data-testid="daypartName">Monday</h2>
      <div data-testid="detailsTemperature">20°/10°</div>
      <svg class="DetailsSummary" name="sunny"></svg>
      <span class="DetailsSummary--wxPhrase">Clear skies</span>
      <div data-testid="Precip"><span data-testid="PercentageValue">10</span></div>
      <li data-testid="MoonphaseSection">
        <svg class="DetailsTable" name="phase-3"></svg>
        <span data-testid="moonPhase">Waxing Crescent</span>
      </li>
    </details>
  </div>
</section>
</body>
</html>
"""

HTML_MULTIPLE = """
<html>
<body>
<section data-testid="DailyForecast">
  <div class="Card">
    <details>
      <h2 data-testid="daypartName">Monday</h2>
      <div data-testid="detailsTemperature">20°/10°</div>
      <svg class="DetailsSummary" name="sunny"></svg>
      <span class="DetailsSummary--wxPhrase">Clear skies</span>
      <div data-testid="Precip"><span data-testid="PercentageValue">10</span></div>
      <li data-testid="MoonphaseSection">
        <svg class="DetailsTable" name="phase-2"></svg>
        <span data-testid="moonPhase">Waxing Crescent</span>
      </li>
    </details>
    <details>
      <h2 data-testid="daypartName">Tuesday</h2>
      <div data-testid="detailsTemperature">22°/12°</div>
      <svg class="DetailsSummary" name="rain"></svg>
      <span class="DetailsSummary--wxPhrase">Light rain</span>
      <div data-testid="Precip"><span data-testid="PercentageValue">60</span></div>
      <li data-testid="MoonphaseSection">
        <svg class="DetailsTable" name="phase-3"></svg>
        <span data-testid="moonPhase">Waxing Crescent%</span>
      </li>
    </details>
  </div>
</section>
</body>
</html>
"""


def test_execute_returns_daily_predictions():
    service = ExtractDailyForecastService()
    pq = PyQuery(HTML_SINGLE)

    results = service.execute(pq)

    assert isinstance(results, list)
    assert len(results) == 1
    dp = results[0]
    assert isinstance(dp, DailyPredictions)
    assert dp.title == "Monday"
    assert dp.summary == "Clear skies"
    assert dp.precipitation.percentage == "10"  # string from HTML
    assert dp.moon_phase.phase == "Waxing Crescent"
    assert "DailyPredictions" in repr(dp)


def test_execute_multiple_forecasts():
    service = ExtractDailyForecastService()
    pq = PyQuery(HTML_MULTIPLE)

    results = service.execute(pq)

    assert len(results) == 2
    titles = [dp.title for dp in results]
    assert "Monday" in titles
    assert "Tuesday" in titles
    assert results[1].summary == "Light rain"


def test_execute_raises_on_missing_section():
    service = ExtractDailyForecastService()
    pq = PyQuery("<html></html>")  # no DailyForecast section

    with pytest.raises(ValueError):
        service.execute(pq)
