from weathergrabber.domain.entities.city_location import CityLocation

def city_location_to_dict(loc: CityLocation) -> dict:
    return {
        "city": loc.city,
        "state_province": loc.state_province,
        "country": loc.country,
    }

def dict_to_city_location(data: dict) -> CityLocation:
    return CityLocation(
        city=data.get("city"),
        state_province=data.get("state_province"),
        country=data.get("country"),
    )
