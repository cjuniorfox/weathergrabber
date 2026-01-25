from weathergrabber.domain.entities.day_night import DayNight

def day_night_to_dict(dn: DayNight) -> dict:
    def temp_to_dict(temp):
        return {
            "label": temp.label,
            "value": temp.value,
        } if temp else None
    return {
        "day": temp_to_dict(dn.day) if dn.day else None,
        "night": temp_to_dict(dn.night) if dn.night else None,
    }

def dict_to_day_night(data: dict) -> DayNight:
    def dict_to_temp(data):
        return DayNight.Temperature(
            label=data.get("label"),
            value=data.get("value"),
        ) if data else None
    return DayNight(
        day=dict_to_temp(data["day"]) if data.get("day") else None,
        night=dict_to_temp(data["night"]) if data.get("night") else None,
    )
