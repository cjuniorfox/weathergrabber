from weathergrabber.domain.entities.hourly_predictions import HourlyPredictions


def hourly_predictions_to_dict(hp: HourlyPredictions) -> dict:
    from weathergrabber.domain.adapter.mappers.weather_icon_enum_mapper import weather_icon_enum_to_dict
    from weathergrabber.domain.adapter.mappers.precipitation_mapper import precipitation_to_dict
    from weathergrabber.domain.adapter.mappers.wind_mapper import wind_to_dict
    from weathergrabber.domain.adapter.mappers.uv_index_mapper import uv_index_to_dict
    return {
        "title": hp.title,
        "temperature": hp.temperature,
        "icon": weather_icon_enum_to_dict(hp.icon) if hp.icon else None,
        "summary": hp.summary,
        "precipitation": precipitation_to_dict(hp.precipitation) if hp.precipitation else None,
        "wind": wind_to_dict(hp.wind) if hp.wind else None,
        "feels_like": hp.feels_like,
        "humidity": hp.humidity,
        "uv_index": uv_index_to_dict(hp.uv_index) if hp.uv_index else None,
        "cloud_cover": hp.cloud_cover,
    }

def dict_to_hourly_predictions(data: dict) -> HourlyPredictions:
    from weathergrabber.domain.adapter.mappers.weather_icon_enum_mapper import dict_to_weather_icon_enum
    from weathergrabber.domain.adapter.mappers.precipitation_mapper import dict_to_precipitation
    from weathergrabber.domain.adapter.mappers.wind_mapper import dict_to_wind
    from weathergrabber.domain.adapter.mappers.uv_index_mapper import dict_to_uv_index
    return HourlyPredictions(
        title=data["title"],
        temperature=data["temperature"],
        icon=dict_to_weather_icon_enum(data["icon"]) if data.get("icon") else None,
        summary=data["summary"],
        precipitation=dict_to_precipitation(data["precipitation"]) if data.get("precipitation") else None,
        wind=dict_to_wind(data["wind"]) if data.get("wind") else None,
        feels_like=data["feels_like"],
        humidity=data["humidity"],
        uv_index=dict_to_uv_index(data["uv_index"]) if data.get("uv_index") else None,
        cloud_cover=data["cloud_cover"],
    )
