import pytest
from unittest.mock import MagicMock
import json

from weathergrabber.domain.city_location import CityLocation
from weathergrabber.domain.hourly_predictions import HourlyPredictions
from weathergrabber.domain.daily_predictions import DailyPredictions

from weathergrabber.domain.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.precipitation import Precipitation 
from weathergrabber.domain.wind import Wind
from weathergrabber.domain.uv_index import UVIndex
from weathergrabber.domain.temperature_hight_low import TemperatureHighLow
from weathergrabber.domain.moon_phase import MoonPhase
from weathergrabber.domain.moon_phase_enum import MoonPhaseEnum
from weathergrabber.domain.day_night import DayNight
from weathergrabber.domain.day_night import DayNight
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.label_value import LabelValue
from weathergrabber.domain.sunrise_sunset import SunriseSunset
from weathergrabber.domain.search import Search
from weathergrabber.domain.timestamp import Timestamp
from weathergrabber.domain.air_quality_index import AirQualityIndex
from weathergrabber.domain.health_activities import HealthActivities

from weathergrabber.adapter.tty.json_tty import JsonTTY

class DummyForecast:
    class current_conditions:
        location = CityLocation(city='TestCity', state_province='TestState', country='TestCountry', location='TestLocation')
        icon = WeatherIconEnum.SUNNY
        temperature = '25°'
        day_night = DayNight(day=DayNight.Temperature("Day","30°"), night=DayNight.Temperature("Night","20°"))
        summary = 'Sunny'
        timestamp = Timestamp.from_string('2025-09-30 12:00')

    class today_details:
        feelslike = LabelValue(label='Feels Like', value='27°')
        sunrise_sunset = SunriseSunset("06:00", "18:00")
        moon_phase = MoonPhase(MoonPhaseEnum.PHASE_15, "Full Moon")
        wind = LabelValue(label='Wind', value='10km/h')
        humidity = LabelValue(label='Humidity', value='50%')
        pressure = LabelValue(label='Pressure', value='1013hPa')
        uv_index = UVIndex.from_string("5 of 12","UV Index")
        visibility = LabelValue(label='Visibility', value='10km')
        high_low = TemperatureHighLow("30°", "20°")
        dew_point = LabelValue(label='Dew Point', value='15°')
    
    air_quality_index = AirQualityIndex.aqi_color_from_string("Air Quality Index\n26\nGood\nAir quality is considered satisfactory, and air pollution poses little or no risk.","#00E838")
    health_activities = HealthActivities.from_text("Health & Activities\nGrass\nSeasonal Allergies and Pollen Count Forecast\nGrass pollen is low in your area")
    hourly_predictions = [
        HourlyPredictions("13:00", "25°", WeatherIconEnum.SUNNY, "Sunny", Precipitation("0%"), Wind.from_string("5 km/h"), "27°", "50%", UVIndex.from_string("5 of 12","UV Index"), "10%"),
        HourlyPredictions("14:00", "26°", WeatherIconEnum.CLOUDY, "Partly Cloudy", Precipitation("10%"), Wind.from_string("10 km/h"), "28°", "55%", UVIndex.from_string("6 of 12","UV Index"), "20%")
    ]
    daily_predictions = [
        DailyPredictions("Today", TemperatureHighLow("30°", "20°"), WeatherIconEnum.SUNNY, "Sun", Precipitation("0%"), MoonPhase(MoonPhaseEnum.PHASE_15, "Full Moon")),
        DailyPredictions("Tomorrow", TemperatureHighLow("28°", "18°"), WeatherIconEnum.CLOUDY, "Cloud", Precipitation("10%"), MoonPhase(MoonPhaseEnum.PHASE_16, "Wan ing Gibbous")),
    ]
    search = Search("12345","TestCity")

@pytest.fixture
def dummy_use_case():
    mock = MagicMock()
    mock.execute.return_value = DummyForecast()
    return mock

def test_console_tty_prints_forecast(monkeypatch, capsys, dummy_use_case):
    params = MagicMock(spec=Params)
    tty = JsonTTY(dummy_use_case)
    tty.execute(params)

    # Check that print was called with the expected JSON string
    output = capsys.readouterr().out
    json_obj = json.loads(output)
    assert isinstance(json_obj, dict)

    assert output.startswith('{')
    assert '"city": "TestCity"' in output
    assert '"temperature": "25\\u00b0"' in output
    assert '"summary": "Sunny"' in output
    assert '{"label": "Wind", "value": "10km/h"}' in output
    assert 'AQI' in output
    assert 'Today' in output
    assert '{"day": {"label": "Day", "value": "30\\u00b0"}' in output
