from weathergrabber.domain.entities.current_conditions import CurrentConditions



def current_conditions_to_dict(cc: CurrentConditions) -> dict:
    from weathergrabber.domain.adapter.mappers.city_location_mapper import city_location_to_dict
    from weathergrabber.domain.adapter.mappers.timestamp_mapper import timestamp_to_dict
    from weathergrabber.domain.adapter.mappers.weather_icon_enum_mapper import weather_icon_enum_to_dict
    from weathergrabber.domain.adapter.mappers.day_night_mapper import day_night_to_dict
    return {
        "location": city_location_to_dict(cc.location) if cc.location else None,
        "timestamp": timestamp_to_dict(cc.timestamp) if cc.timestamp else None,
        "temperature": cc.temperature,
        "icon": weather_icon_enum_to_dict(cc.icon) if cc.icon else None,
        "summary": cc.summary,
        "day_night": day_night_to_dict(cc.day_night) if cc.day_night else None,
    }

def dict_to_current_conditions(data: dict) -> CurrentConditions:
    from weathergrabber.domain.adapter.mappers.city_location_mapper import dict_to_city_location
    from weathergrabber.domain.adapter.mappers.timestamp_mapper import dict_to_timestamp
    from weathergrabber.domain.adapter.mappers.weather_icon_enum_mapper import dict_to_weather_icon_enum
    from weathergrabber.domain.adapter.mappers.day_night_mapper import dict_to_day_night

    return CurrentConditions(
        location=dict_to_city_location(data["location"]) if data.get("location") else None,
        timestamp=dict_to_timestamp(data["timestamp"]) if data.get("timestamp") else None,
        temperature=data.get("temperature"),
        icon=dict_to_weather_icon_enum(data["icon"]) if data.get("icon") else None,
        summary=data.get("summary"),
        day_night=dict_to_day_night(data["day_night"]) if data.get("day_night") else None,
    )
