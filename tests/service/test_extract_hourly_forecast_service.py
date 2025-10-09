import pytest
from pyquery import PyQuery
## No need for MagicMock, use PyQuery and real HTML
from weathergrabber.service.extract_hourly_forecast_service import ExtractHourlyForecastService
from weathergrabber.domain.hourly_predictions import HourlyPredictions

def test_execute_success():
    html = '''
    <html>
      <body>
        <section data-testid="HourlyForecast">
          <div class="Card">
            <details>
              <h2>10:00 AM</h2>
              <div data-testid="detailsTemperature">22°C</div>
              <svg class="DetailsSummary" name="clear"/>
              <span class="DetailsSummary--wxPhrase">Sunny</span>
              <div data-testid="Precip"><span data-testid="PercentageValue">10%</span></div>
              <span data-testid="WindTitle"></span><div><span>NW 10km/h</span></div>
              <span data-testid="FeelsLikeTitle"></span><span>21°C</span>
              <span data-testid="HumidityTitle"></span><span>50%</span>
              <span data-testid="UVIndexValue">3</span>
              <span data-testid="CloudCoverTitle"></span><span>10%</span>
              <span data-testid="AccumulationTitle"></span><span>0 mm</span>
            </details>
          </div>
          <div class="Card">
            <details>
              <h2>11:00 AM</h2>
              <div data-testid="detailsTemperature">22°C</div>
              <svg class="DetailsSummary" name="clear"/>
              <span class="DetailsSummary--wxPhrase">Sunny</span>
              <div data-testid="Precip"><span data-testid="PercentageValue">10%</span></div>
              <span data-testid="WindTitle"></span><div><span>NW 10km/h</span></div>
              <span data-testid="FeelsLikeTitle"></span><span>21°C</span>
              <span data-testid="HumidityTitle"></span><span>50%</span>
              <span data-testid="UVIndexValue">3</span>
              <span data-testid="CloudCoverTitle"></span><span>10%</span>
              <span data-testid="AccumulationTitle"></span><span>0 mm</span>
            </details>
            </details>
          </div>
        </section>
      </body>
    </html>
    '''
    pq = PyQuery(html)
    service = ExtractHourlyForecastService()
    result = service.execute(pq)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].title == "10:00 AM"
    assert result[1].title == "11:00 AM"

def test_execute_empty():
  html = "<section data-testid='HourlyForecast'></section>"  # No Card divs
  pq = PyQuery(html)
  service = ExtractHourlyForecastService()
  with pytest.raises(ValueError, match="Could not extract hourly forecast."):
    service.execute(pq)

def test_execute_exception_on_wind_error():
  html = '''
  <html>
    <body>
      <section data-testid="HourlyForecast">
        <div class="Card">
          <details>
            <h2>10:00 AM</h2>
            <div data-testid="detailsTemperature">22°C</div>
            <svg class="DetailsSummary" name="clear"/>
            <span class="DetailsSummary--wxPhrase">Sunny</span>
            <div data-testid="Precip"><span data-testid="PercentageValue">10%</span></div>
            <span data-testid="WindTitle"></span><div><span>INVALID WIND DATA</span></div>
            <span data-testid="FeelsLikeTitle"></span><span>21°C</span>
            <span data-testid="HumidityTitle"></span><span>50%</span>
            <span data-testid="UVIndexValue">3</span>
            <span data-testid="CloudCoverTitle"></span><span>10%</span>
            <span data-testid="AccumulationTitle"></span><span>0 mm</span>
          </details>
        </div>
      </section>
    </body>
  </html>
  '''
  pq = PyQuery(html)
  service = ExtractHourlyForecastService()
  with pytest.raises(ValueError, match="Could not extract hourly forecast."):
    service.execute(pq)
    

def test_execute_exception():
  class BrokenPyQuery(PyQuery):
    def find(self, *args, **kwargs):
      raise Exception("fail")
  pq = BrokenPyQuery("<section></section>")
  service = ExtractHourlyForecastService()
  with pytest.raises(ValueError, match="Could not extract hourly forecast."):
    service.execute(pq)
