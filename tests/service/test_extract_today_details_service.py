import pytest
from pyquery import PyQuery
from weathergrabber.service.extract_today_details_service import ExtractTodayDetailsService
from weathergrabber.domain.today_details import TodayDetails

def get_sample_html():
    return '''
    <html><body>
    <div id="todayDetails">
      <div data-testid="FeelsLikeSection">
        <span>Feels Like</span>
        <span>60°</span>
      </div>
      <div data-testid="sunriseSunsetContainer">
        <div>
          <p class="TwcSunChart">6:12 AM</p>
          <p class="TwcSunChart">7:45 PM</p>
        </div>
      </div>

      <svg class="WeatherDetailsListItem--icon" name="sun"></svg>
      <div class="WeatherDetailsListItem--label">High / Low</div>
      <div data-testid="wxData">--/54°</div>

      <svg class="WeatherDetailsListItem--icon" name="wind"></svg>
      <div class="WeatherDetailsListItem--label">Wind</div>
      <div data-testid="wxData">7 mph</div>

      <svg class="WeatherDetailsListItem--icon" name="humidity"></svg>
      <div class="WeatherDetailsListItem--label">Humidity</div>
      <div data-testid="wxData">100%</div>

      <svg class="WeatherDetailsListItem--icon" name="dew-point"></svg>
      <div class="WeatherDetailsListItem--label">Dew Point</div>
      <div data-testid="wxData">60°</div>

      <svg class="WeatherDetailsListItem--icon" name="pressure"></svg>
      <div class="WeatherDetailsListItem--label">Pressure</div>
      <div data-testid="wxData">30.31 in</div>

      <svg class="WeatherDetailsListItem--icon" name="uv-index"></svg>
      <div class="WeatherDetailsListItem--label">UV Index</div>
      <div data-testid="wxData">5 of 10</div>

      <svg class="WeatherDetailsListItem--icon" name="visibility"></svg>
      <div class="WeatherDetailsListItem--label">Visibility</div>
      <div data-testid="wxData">10.0 mi</div>

      <svg class="WeatherDetailsListItem--icon" name="phase-2"></svg>
      <div class="WeatherDetailsListItem--label">Moon Phase</div>
      <div data-testid="wxData">Waxing Crescent</div>
    </div>
    </body></html>
    '''

def test_extract_today_details_service():
    html = get_sample_html()
    pq = PyQuery(html)
    service = ExtractTodayDetailsService()
    result = service.execute(pq)
    assert isinstance(result, TodayDetails)
    assert result.feelslike.value == '60°'
    assert result.sunrise_sunset.sunrise.value == '6:12 AM'
    assert result.sunrise_sunset.sunset.value == '7:45 PM'
    assert f"{result.high_low}" == '--/54°'
    assert result.wind.value == '7 mph'
    assert result.humidity.value == '100%'
    assert result.dew_point.value == '60°'
    assert result.pressure.value == '30.31 in'
    assert f"{result.uv_index}" == 'UV Index: 5 of 10'
    assert result.visibility.value == '10.0 mi'
    assert result.moon_phase.phase == 'Waxing Crescent'
    assert result.moon_phase.label == 'Moon Phase'
    assert result.moon_phase.icon is not None
