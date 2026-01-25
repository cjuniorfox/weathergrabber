class DummyWind:
    direction = "NW"
    speed = "10 km/h"

from weathergrabber.domain.adapter.mappers.wind_mapper import wind_to_dict, dict_to_wind
from weathergrabber.domain.entities.wind import Wind

def test_wind_to_dict():
    wind = DummyWind()
    d = wind_to_dict(wind)
    assert d["direction"] == "NW"
    assert d["speed"] == "10 km/h"
    assert isinstance(d, dict)

def test_wind_to_dict_none():
    d = wind_to_dict(None)
    assert d is None


def test_dict_to_wind():
    data = {
        "direction": "N",
        "speed": "10 km/h"
    }
    wind = dict_to_wind(data)
    assert isinstance(wind, Wind)
    assert wind.direction == "N"
    assert wind.speed == "10 km/h"


def test_dict_to_wind_none():
    wind = dict_to_wind(None)
    assert wind is None


def test_dict_to_wind_various_directions():
    test_cases = [
        ({"direction": "N", "speed": "5 km/h"}, "N"),
        ({"direction": "S", "speed": "8 km/h"}, "S"),
        ({"direction": "E", "speed": "15 km/h"}, "E"),
        ({"direction": "W", "speed": "12 km/h"}, "W"),
        ({"direction": "NE", "speed": "20 km/h"}, "NE"),
    ]
    for data, expected_direction in test_cases:
        wind = dict_to_wind(data)
        assert wind.direction == expected_direction


def test_dict_to_wind_various_speeds():
    test_cases = [
        ({"direction": "N", "speed": "0 km/h"}, "0 km/h"),
        ({"direction": "S", "speed": "25 km/h"}, "25 km/h"),
        ({"direction": "E", "speed": "50 km/h"}, "50 km/h"),
    ]
    for data, expected_speed in test_cases:
        wind = dict_to_wind(data)
        assert wind.speed == expected_speed


def test_dict_to_wind_roundtrip():
    original = Wind(direction="NW", speed="15 km/h")
    data = wind_to_dict(original)
    reconstructed = dict_to_wind(data)
    assert reconstructed.direction == original.direction
    assert reconstructed.speed == original.speed
