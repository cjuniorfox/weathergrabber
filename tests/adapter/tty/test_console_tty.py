import pytest
from unittest.mock import MagicMock

from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.icon_enum import IconEnum


from weathergrabber.adapter.tty.console_tty import ConsoleTTY


def make_mock_forecast():
    mock_forecast = MagicMock()
    mock_current = MagicMock()
    mock_current.location = MagicMock()
    mock_current.location.__str__.return_value = 'TestLocation, TestCity, TestState, TestCountry'
    mock_icon = MagicMock()
    mock_icon.fa_icon = 'FA_SUNNY'
    mock_icon.emoji_icon = '☀️'
    mock_current.icon = mock_icon
    mock_current.temperature = '25°'
    mock_current.day_night = MagicMock()
    mock_current.summary = 'Sunny'
    mock_current.timestamp = '2025-09-30 12:00'
    mock_forecast.current_conditions = mock_current

    mock_today = MagicMock()
    mock_today.feelslike = MagicMock()
    mock_today.sunrise_sunset = MagicMock()
    mock_today.moon_phase = MagicMock()
    mock_today.wind = MagicMock()
    mock_today.humidity = MagicMock()
    mock_today.pressure = MagicMock()
    mock_today.uv_index = MagicMock()
    mock_today.visibility = MagicMock()
    mock_forecast.today_details = mock_today

    mock_aqi = MagicMock()
    mock_aqi.color = MagicMock()
    mock_aqi.category = 'Good'
    mock_aqi.acronym = 'AQI'
    mock_aqi.value = '42'
    mock_forecast.air_quality_index = mock_aqi

    mock_hourly = [MagicMock(), MagicMock()]
    mock_forecast.hourly_predictions = mock_hourly

    mock_daily_1 = MagicMock()
    mock_daily_1.day = "Today"
    mock_daily_1.title = "Today"
    mock_daily_1.temperature = MagicMock()
    mock_daily_1.temperature.__str__.return_value = "30°/20°"
    mock_daily_1.high_low = MagicMock()
    mock_daily_1.high_low.__str__.return_value = "30°/20°"
    mock_daily_1.__str__.return_value = "Today 30°/20°"

    mock_daily_2 = MagicMock()
    mock_daily_2.day = "Tomorrow"
    mock_daily_2.title = "Tomorrow"
    mock_daily_2.temperature = MagicMock()
    mock_daily_2.temperature.__str__.return_value = "28°/18°"
    mock_daily_2.high_low = MagicMock()
    mock_daily_2.high_low.__str__.return_value = "28°/18°"
    mock_daily_2.__str__.return_value = "Tomorrow 28°/18°"

    mock_forecast.daily_predictions = [mock_daily_1, mock_daily_2]

    return mock_forecast


@pytest.fixture
def dummy_use_case():
    mock = MagicMock()
    mock.execute.return_value = make_mock_forecast()
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
    assert 'AQI' in output
    assert 'Today' in output
    assert '30°/20°' in output

def test_console_tty_keep_open(monkeypatch, capsys, dummy_use_case):
    params = Params(icons=IconEnum.FA, keep_open=True)
    tty = ConsoleTTY(dummy_use_case)

    # Patch input to simulate user pressing Enter immediately
    monkeypatch.setattr('builtins.input', lambda _: '\n')
    
    tty.execute(params)
    output = capsys.readouterr().out
    assert '\033[' in output
