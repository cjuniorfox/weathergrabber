import pytest
from unittest.mock import MagicMock
from weathergrabber.adapter.tty.console_tty import ConsoleTTY
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.icon_enum import IconEnum
from weathergrabber.domain.city_location import CityLocation

class DummyForecast:
    class current_conditions:
        location = CityLocation(city='TestCity', state_province='TestState', country='TestCountry', location='TestLocation')
        icon = type('icon', (), {'fa_icon': '🌤', 'emoji_icon': '☀️'})()
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
        color = type('color', (), {'red': 100, 'green': 200, 'blue': 150})()
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
            'title': 'Tuesday', 'high_low': '30°/20°', 'icon': type('icon', (), {'fa_icon': '🌤', 'emoji_icon': '☀️'}),
            'precipitation': type('prec', (), {'percentage': '10%'})()
        })
    ]

@pytest.fixture
def dummy_use_case():
    mock = MagicMock()
    mock.execute.return_value = DummyForecast()
    return mock

def test_console_tty_prints_forecast(monkeypatch, capsys, dummy_use_case):
    params = Params(icons=IconEnum.FA, keep_open=False)
    tty = ConsoleTTY(dummy_use_case)
    tty.execute(params)
    output = capsys.readouterr().out
    assert 'TestLocation, TestCity, TestState, TestCountry' in output
    assert '25°' in output
    assert 'Sunny' in output
    assert '2025-09-30 12:00' in output
    assert '🌤' in output
    assert 'AQI' in output
    assert 'Tuesday' in output
    assert '30°/20°' in output
