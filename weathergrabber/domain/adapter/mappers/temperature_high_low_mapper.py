from weathergrabber.domain.entities.temperature_hight_low import TemperatureHighLow

def temperature_high_low_to_dict(thl: TemperatureHighLow) -> dict:
    return {
        "high": thl.high,
        "low": thl.low,
        "label": thl.label,
    }

def dict_to_temperature_high_low(data: dict) -> TemperatureHighLow:
    return TemperatureHighLow(
        high=data.get("high"),
        low=data.get("low"),
        label=data.get("label"),
    )
