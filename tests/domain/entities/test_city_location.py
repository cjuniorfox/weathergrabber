import pytest
from weathergrabber.domain.entities.city_location import CityLocation

def test_from_string_full():
    data = "Nova Friburgo, Rio de Janeiro, Brazil"
    loc = CityLocation.from_string(data)
    assert loc.city == "Nova Friburgo"
    assert loc.state_province == "Rio de Janeiro"
    assert loc.country == "Brazil"
    assert loc.location is None
    assert str(loc) == "Nova Friburgo, Rio de Janeiro, Brazil"

def test_from_string_with_location():
    data = "Macuco, Santos, São Paulo, Brésil"
    loc = CityLocation.from_string(data)
    assert loc.city == "Santos"
    assert loc.state_province == "São Paulo"
    assert loc.country == "Brésil"
    assert loc.location == "Macuco"
    assert str(loc) == "Macuco, Santos, São Paulo, Brésil"

def test_from_string_us():
    data = "New York, NY, USA"
    loc = CityLocation.from_string(data)
    assert loc.city == "New York"
    assert loc.state_province == "NY"
    assert loc.country == "USA"
    assert loc.location is None
    assert str(loc) == "New York, NY, USA"

def test_from_string_japan():
    data = "Tokyo, Tokyo Prefecture, Japan"
    loc = CityLocation.from_string(data)
    assert loc.city == "Tokyo"
    assert loc.state_province == "Tokyo Prefecture"
    assert loc.country == "Japan"
    assert loc.location is None
    assert str(loc) == "Tokyo, Tokyo Prefecture, Japan"

def test_from_string_two_parts():
    data = "London, England"
    loc = CityLocation.from_string(data)
    assert loc.city == "London"
    assert loc.state_province == "England"
    assert loc.country is None
    assert loc.location is None
    assert str(loc) == "London, England"

def test_from_string_one_part():
    data = "Paris"
    loc = CityLocation.from_string(data)
    assert loc.city == "Paris"
    assert loc.state_province is None
    assert loc.country is None
    assert loc.location is None
    assert str(loc) == "Paris"

def test_empty_city_location_string():
    with pytest.raises(ValueError, match="City location string cannot be empty"):
        CityLocation.from_string("")
