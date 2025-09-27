import pytest
from pyquery import PyQuery
from weathergrabber.service.extract_current_conditions_service import ExtractCurrentConditionsService
from weathergrabber.domain.current_conditions import CurrentConditions

def test_extract_current_conditions_service_real_html():
    html = """
        <html>
          <body>
            <div data-testid="CurrentConditionsContainer">
              <h1>Nova Friburgo, Rio de Janeiro, Brazil</h1>
              <span class="timestamp">As of 11:25 am GMT-03:00</span>
              <div>
                <span class="tempValue" data-testid="TemperatureValue">16<span class="CurrentConditions--degreeSymbol--tzLy9">°</span></span>
                <span>
                  <svg class="wxIcon" name="mostly-cloudy-day"></svg>
                </span>
              </div>
              <div data-testid="wxPhrase" class="CurrentConditions--phraseValue---VS-k">Mostly Cloudy</div>
              <div class="tempHiLoValue">
                Day&nbsp;17° • Night&nbsp;8°
              </div>
            </div>
          </body>
        </html>
    """
    pq = PyQuery(html)
    service = ExtractCurrentConditionsService()
    result = service.execute(pq)
    assert isinstance(result, CurrentConditions)
    assert result.location is not None
    assert result.temperature == "16°"
    assert result.icon is not None
    assert result.summary == "Mostly Cloudy"
    assert result.day_night is not None
