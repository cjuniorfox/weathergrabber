from weathergrabber.domain.entities.sunrise_sunset import SunriseSunset

def sunrise_sunset_to_dict(ss: SunriseSunset) -> dict:
    from weathergrabber.domain.adapter.mappers.weather_icon_enum_mapper import weather_icon_enum_to_dict
    def icon_value_to_dict(iv: SunriseSunset.IconValue):
        return {
            "icon": weather_icon_enum_to_dict(iv.icon) if iv.icon else None,
            "value": iv.value,
        } if iv else None
    return {
        "sunrise": icon_value_to_dict(ss.sunrise) if ss.sunrise else None,
        "sunset": icon_value_to_dict(ss.sunset) if ss.sunset else None,
    }

def dict_to_sunrise_sunset(data: dict) -> SunriseSunset:

    if data is None:
        return None

    return SunriseSunset(
        sunrise=data.get("sunrise").get("value") if data.get("sunrise") and data.get("sunrise").get("value") else None,
        sunset=data.get("sunset").get("value") if data.get("sunset") and data.get("sunset").get("value") else None
    )
