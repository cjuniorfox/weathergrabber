import pytest
from unittest.mock import MagicMock
from weathergrabber.adapter.tty.waybar_tty import WaybarTTY
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.icon_enum import IconEnum
from weathergrabber.domain.city_location import CityLocation

class DummyHighLow:
    high = '30°'
    low = '20°'

class DummyForecast:
    class current_conditions:
        location = CityLocation(city='TestCity', state_province='TestState', country='TestCountry', location='TestLocation')

        icon = type('icon', (), {'fa_icon': '🌤', 'emoji_icon': '☀️', 'name': 'PARTLY_CLOUDY'})()
        temperature = '25°'
        day_night = type('dn', (), {
            'day': type('temp', (), {'value': '30°'})(),
            'night': type('temp', (), {'value': '20°'})()
        })()
        summary = 'Sunny'
        timestamp = '2025-09-30 12:00'
    class today_details:
        feelslike = type('feels', (), {'value': '27°'})()
        sunrise_sunset = type('ss', (), {
            'sunrise': type('sun', (), {'icon': type('icon', (), {'fa_icon': '🌅', 'emoji_icon': '🌄'}), 'value': '06:00'})(),
            'sunset': type('sun', (), {'icon': type('icon', (), {'fa_icon': '🌇', 'emoji_icon': '🌆'}), 'value': '18:00'})()
        })()
        moon_phase = type('moon', (), {'icon': type('icon', (), {'fa_icon': '🌙', 'emoji_icon': '🌚'}), 'phase': 'Full'})()
        wind = type('wind', (), {'value': '10km/h'})()
        humidity = type('hum', (), {'value': '50%'})()
        pressure = '1013hPa'
        uv_index = '5'
        visibility = type('vis', (), {'value': '10km'})()
    class air_quality_index:
        color = type('color', (), {'hex': '#64c896'})()
        category = 'Good'
        acronym = 'AQI'
        value = '42'
    hourly_predictions = [
        type('hour', (), {
            'title': '13:00', 'temperature': '25°', 'icon': type('icon', (), {'fa_icon': '🌤', 'emoji_icon': '☀️'}),
            'precipitation': type('prec', (), {'percentage': '0%'})()
        })
    ]
    daily_predictions = [
        type('day', (), {
            'title': 'Tue', 'high_low': DummyHighLow(), 'icon': type('icon', (), {'fa_icon': '🌤', 'emoji_icon': '☀️'}),
            'precipitation': type('prec', (), {'percentage': '10%'})()
        })
    ]

@pytest.fixture
def dummy_use_case():
    mock = MagicMock()
    mock.execute.return_value = DummyForecast()
    return mock

def test_waybar_tty_prints_json(monkeypatch, capsys, dummy_use_case):
    import json
    params = Params(icons=IconEnum.FA)
    tty = WaybarTTY(dummy_use_case)
    tty.execute(params)
    output = capsys.readouterr().out
    # Check valid JSON
    try:
        data = json.loads(output)
    except Exception as e:
        pytest.fail(f"Output is not valid JSON: {e}\nOutput: {output}")
    result = data.get('tooltip')
    # Check for expected values in JSON
    assert 'TestCity' in result
    assert '25°' in result  # degrees
    assert 'Sunny' in result
    assert '2025-09-30 12:00' in result
    assert '🌤' in result  # weather icon
    assert 'AQI' in result
    assert 'Tue' in result
    assert '30°' in result and '20°' in result
    assert 'text' in data and 'tooltip' in data
