
from weathergrabber.domain.entities.air_quality_index import AirQualityIndex


def air_quality_index_to_dict(aqi: AirQualityIndex) -> dict:
    from weathergrabber.domain.adapter.mappers.color_mapper import color_to_dict
    return {
        "title": aqi.title,
        "value": aqi.value,
        "category": aqi.category,
        "description": aqi.description,
        "acronym": aqi.acronym,
        "color": color_to_dict(aqi.color) if aqi.color else None,
    }

def dict_to_air_quality_index(data: dict) -> AirQualityIndex:
    from weathergrabber.domain.adapter.mappers.color_mapper import dict_to_color
    return AirQualityIndex(
        title=data["title"],
        value=data["value"],
        category=data["category"],
        description=data["description"],
        acronym=data["acronym"],
        color=dict_to_color(data["color"]) if data.get("color") else None,
    )
