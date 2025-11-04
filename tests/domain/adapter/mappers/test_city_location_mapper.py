from weathergrabber.domain.entities.city_location import CityLocation
from weathergrabber.domain.adapter.mappers.city_location_mapper import city_location_to_dict

def test_city_location_to_dict():
    loc = CityLocation("Paris", "Île-de-France", "France")
    d = city_location_to_dict(loc)
    assert d["city"] == "Paris"
    assert d["state_province"] == "Île-de-France"
    assert d["country"] == "France"
    assert isinstance(d, dict)
