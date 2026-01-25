def wind_to_dict(wind):
    if wind is None:
        return None
    return {
        "direction": wind.direction,
        "speed": wind.speed
    }

def dict_to_wind(data: dict):
    if data is None:
        return None
    from weathergrabber.domain.entities.wind import Wind
    return Wind(
        direction=data["direction"],
        speed=data["speed"]
    )
