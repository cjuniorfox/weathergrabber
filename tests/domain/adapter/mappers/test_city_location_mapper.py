from weathergrabber.domain.entities.city_location import CityLocation
from weathergrabber.domain.adapter.mappers.city_location_mapper import city_location_to_dict, dict_to_city_location

def test_city_location_to_dict():
    loc = CityLocation("Paris", "Île-de-France", "France")
    d = city_location_to_dict(loc)
    assert d["city"] == "Paris"
    assert d["state_province"] == "Île-de-France"
    assert d["country"] == "France"
    assert isinstance(d, dict)


def test_dict_to_city_location():
    data = {
        "city": "Paris",
        "state_province": "Île-de-France",
        "country": "France"
    }
    loc = dict_to_city_location(data)
    assert isinstance(loc, CityLocation)
    assert loc.city == "Paris"
    assert loc.state_province == "Île-de-France"
    assert loc.country == "France"


def test_dict_to_city_location_with_none_values():
    data = {
        "city": None,
        "state_province": None,
        "country": None
    }
    loc = dict_to_city_location(data)
    assert loc.city is None
    assert loc.state_province is None
    assert loc.country is None


def test_dict_to_city_location_missing_keys():
    data = {}
    loc = dict_to_city_location(data)
    assert loc.city is None
    assert loc.state_province is None
    assert loc.country is None


def test_dict_to_city_location_partial_data():
    data = {
        "city": "New York",
        "country": "United States"
    }
    loc = dict_to_city_location(data)
    assert loc.city == "New York"
    assert loc.state_province is None
    assert loc.country == "United States"


def test_dict_to_city_location_roundtrip():
    original_loc = CityLocation("Tokyo", "Tokyo", "Japan")
    data = city_location_to_dict(original_loc)
    reconstructed_loc = dict_to_city_location(data)
    assert reconstructed_loc.city == original_loc.city
    assert reconstructed_loc.state_province == original_loc.state_province
    assert reconstructed_loc.country == original_loc.country
