from weathergrabber.domain.entities.daily_predictions import DailyPredictions


def daily_predictions_to_dict(dp: DailyPredictions) -> dict:
    from weathergrabber.domain.adapter.mappers.temperature_high_low_mapper import temperature_high_low_to_dict
    from weathergrabber.domain.adapter.mappers.weather_icon_enum_mapper import weather_icon_enum_to_dict
    from weathergrabber.domain.adapter.mappers.precipitation_mapper import precipitation_to_dict
    from weathergrabber.domain.adapter.mappers.moon_phase_mapper import moon_phase_to_dict
    return {
        "title": dp.title,
        "high_low": temperature_high_low_to_dict(dp.high_low) if dp.high_low else None,
        "icon": weather_icon_enum_to_dict(dp.icon) if dp.icon else None,
        "summary": dp.summary,
        "precipitation": precipitation_to_dict(dp.precipitation) if dp.precipitation else None,
        "moon_phase": moon_phase_to_dict(dp.moon_phase) if dp.moon_phase else None,
    }

def dict_to_daily_predictions(data: dict) -> DailyPredictions:
    from weathergrabber.domain.adapter.mappers.temperature_high_low_mapper import dict_to_temperature_high_low
    from weathergrabber.domain.adapter.mappers.weather_icon_enum_mapper import dict_to_weather_icon_enum
    from weathergrabber.domain.adapter.mappers.precipitation_mapper import dict_to_precipitation
    from weathergrabber.domain.adapter.mappers.moon_phase_mapper import dict_to_moon_phase
    return DailyPredictions(
        title=data.get("title"),
        high_low=dict_to_temperature_high_low(data["high_low"]) if data.get("high_low") else None,
        icon=dict_to_weather_icon_enum(data["icon"]) if data.get("icon") else None,
        summary=data.get("summary"),
        precipitation=dict_to_precipitation(data["precipitation"]) if data.get("precipitation") else None,
        moon_phase=dict_to_moon_phase(data["moon_phase"]) if data.get("moon_phase") else None,
    )
