
from weathergrabber.domain.entities.today_details import TodayDetails

def today_details_to_dict(td: TodayDetails) -> dict:
    from weathergrabber.domain.adapter.mappers.label_value_mapper import label_value_to_dict
    from weathergrabber.domain.adapter.mappers.sunrise_sunset_mapper import sunrise_sunset_to_dict
    from weathergrabber.domain.adapter.mappers.temperature_high_low_mapper import temperature_high_low_to_dict
    from weathergrabber.domain.adapter.mappers.uv_index_mapper import uv_index_to_dict
    from weathergrabber.domain.adapter.mappers.moon_phase_mapper import moon_phase_to_dict

    return {
        "feelslike": label_value_to_dict(td.feelslike) if td.feelslike else None,
        "sunrise_sunset": sunrise_sunset_to_dict(td.sunrise_sunset) if td.sunrise_sunset else None,
        "high_low": temperature_high_low_to_dict(td.high_low) if td.high_low else None,
        "wind": label_value_to_dict(td.wind) if td.wind else None,
        "humidity": label_value_to_dict(td.humidity) if td.humidity else None,
        "dew_point": label_value_to_dict(td.dew_point) if td.dew_point else None,
        "pressure": label_value_to_dict(td.pressure) if td.pressure else None,
        "uv_index": uv_index_to_dict(td.uv_index) if td.uv_index else None,
        "visibility": label_value_to_dict(td.visibility) if td.visibility else None,
        "moon_phase": moon_phase_to_dict(td.moon_phase) if td.moon_phase else None,
    }

def dict_to_today_details(data: dict) -> TodayDetails:
    from weathergrabber.domain.adapter.mappers.label_value_mapper import dict_to_label_value
    from weathergrabber.domain.adapter.mappers.sunrise_sunset_mapper import dict_to_sunrise_sunset
    from weathergrabber.domain.adapter.mappers.temperature_high_low_mapper import dict_to_temperature_high_low
    from weathergrabber.domain.adapter.mappers.uv_index_mapper import dict_to_uv_index
    from weathergrabber.domain.adapter.mappers.moon_phase_mapper import dict_to_moon_phase

    return TodayDetails(
        feelslike=dict_to_label_value(data["feelslike"]) if data.get("feelslike") else None,
        sunrise_sunset=dict_to_sunrise_sunset(data["sunrise_sunset"]) if data.get("sunrise_sunset") else None,
        high_low=dict_to_temperature_high_low(data["high_low"]) if data.get("high_low") else None,
        wind=dict_to_label_value(data["wind"]) if data.get("wind") else None,
        humidity=dict_to_label_value(data["humidity"]) if data.get("humidity") else None,
        dew_point=dict_to_label_value(data["dew_point"]) if data.get("dew_point") else None,
        pressure=dict_to_label_value(data["pressure"]) if data.get("pressure") else None,
        uv_index=dict_to_uv_index(data["uv_index"]) if data.get("uv_index") else None,
        visibility=dict_to_label_value(data["visibility"]) if data.get("visibility") else None,
        moon_phase=dict_to_moon_phase(data["moon_phase"]) if data.get("moon_phase") else None,
    )
