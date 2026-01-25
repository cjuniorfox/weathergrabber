from weathergrabber.domain.entities.forecast import Forecast

def forecast_to_dict(forecast: Forecast) -> dict:
    from weathergrabber.domain.adapter.mappers.search_mapper import search_to_dict
    from weathergrabber.domain.adapter.mappers.current_conditions_mapper import current_conditions_to_dict
    from weathergrabber.domain.adapter.mappers.today_details_mapper import today_details_to_dict
    from weathergrabber.domain.adapter.mappers.air_quality_index_mapper import air_quality_index_to_dict
    from weathergrabber.domain.adapter.mappers.health_activities_mapper import health_activities_to_dict
    from weathergrabber.domain.adapter.mappers.hourly_predictions_mapper import hourly_predictions_to_dict
    from weathergrabber.domain.adapter.mappers.daily_predictions_mapper import daily_predictions_to_dict

    return {
        "search": search_to_dict(forecast.search) if forecast.search else None,
        "current_conditions": current_conditions_to_dict(forecast.current_conditions) if forecast.current_conditions else None,
        "today_details": today_details_to_dict(forecast.today_details) if forecast.today_details else None,
        "air_quality_index": air_quality_index_to_dict(forecast.air_quality_index) if forecast.air_quality_index else None,
        "health_activities": health_activities_to_dict(forecast.health_activities) if forecast.health_activities else None,
        "hourly_predictions": [hourly_predictions_to_dict(h) for h in forecast.hourly_predictions],
        "daily_predictions": [daily_predictions_to_dict(d) for d in forecast.daily_predictions],
    }
def dict_to_forecast(data: dict) -> Forecast:
    from weathergrabber.domain.adapter.mappers.search_mapper import dict_to_search
    from weathergrabber.domain.adapter.mappers.current_conditions_mapper import dict_to_current_conditions
    from weathergrabber.domain.adapter.mappers.today_details_mapper import dict_to_today_details
    from weathergrabber.domain.adapter.mappers.air_quality_index_mapper import dict_to_air_quality_index
    from weathergrabber.domain.adapter.mappers.health_activities_mapper import dict_to_health_activities
    from weathergrabber.domain.adapter.mappers.hourly_predictions_mapper import dict_to_hourly_predictions
    from weathergrabber.domain.adapter.mappers.daily_predictions_mapper import dict_to_daily_predictions

    return Forecast(
        search=dict_to_search(data["search"]) if data.get("search") else None,
        current_conditions=dict_to_current_conditions(data["current_conditions"]) if data.get("current_conditions") else None,
        today_details=dict_to_today_details(data["today_details"]) if data.get("today_details") else None,
        air_quality_index=dict_to_air_quality_index(data["air_quality_index"]) if data.get("air_quality_index") else None,
        health_activities=dict_to_health_activities(data["health_activities"]) if data.get("health_activities") else None,
        hourly_predictions=[dict_to_hourly_predictions(h) for h in data.get("hourly_predictions", [])],
        daily_predictions=[dict_to_daily_predictions(d) for d in data.get("daily_predictions", [])],
    )
