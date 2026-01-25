from weathergrabber.domain.entities.weather_icon_enum import WeatherIconEnum

def weather_icon_enum_to_dict(icon: WeatherIconEnum) -> dict:
    return {
        "name": icon.name,
        "fa_icon": icon.fa_icon,
        "emoji_icon": icon.emoji_icon,
    }

def dict_to_weather_icon_enum(data: dict) -> WeatherIconEnum:
    return WeatherIconEnum.from_name(data.get("name"))