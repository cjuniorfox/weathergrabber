import pytest
from weathergrabber.domain.entities.current_conditions import CurrentConditions
from weathergrabber.domain.entities.city_location import CityLocation
from weathergrabber.domain.entities.timestamp import Timestamp
from weathergrabber.domain.entities.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.entities.day_night import DayNight
from weathergrabber.domain.adapter.mappers.current_conditions_mapper import current_conditions_to_dict

def test_current_conditions_to_dict():
    location = CityLocation(city="São Paulo", state_province="SP", country="Brazil")
    timestamp = Timestamp(time="16:37", gmt="GMT-03:00", text="As of 16:37 GMT-03:00")
    temperature = "22°C"
    icon = WeatherIconEnum.SUNNY
    summary = "Sunny"
    day = DayNight.Temperature(label="Day Temp", value="25°C")
    night = DayNight.Temperature(label="Night Temp", value="18°C")
    day_night = DayNight(day=day, night=night)

    cc = CurrentConditions(
        location=location,
        timestamp=timestamp,
        temperature=temperature,
        icon=icon,
        summary=summary,
        day_night=day_night
    )
    result = current_conditions_to_dict(cc)
    assert result["location"] == {"city": "São Paulo", "state_province": "SP", "country": "Brazil"}
    assert result["timestamp"] == {"time": "16:37", "gmt": "GMT-03:00", "text": "As of 16:37 GMT-03:00"}
    assert result["temperature"] == "22°C"
    assert result["icon"]["name"] == "sunny"
    assert result["summary"] == "Sunny"
    assert result["day_night"]["day"] == {"label": "Day Temp", "value": "25°C"}
    assert result["day_night"]["night"] == {"label": "Night Temp", "value": "18°C"}
    assert isinstance(result, dict)

def test_current_conditions_to_dict_none():
    cc = CurrentConditions(
        location=None,
        timestamp=None,
        temperature="22°C",
        icon=None,
        summary="Sunny",
        day_night=None
    )
    result = current_conditions_to_dict(cc)
    assert result["location"] is None
    assert result["timestamp"] is None
    assert result["temperature"] == "22°C"
    assert result["icon"] is None
    assert result["summary"] == "Sunny"
    assert result["day_night"] is None
    assert isinstance(result, dict)
