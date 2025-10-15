from weathergrabber.domain.temperature_hight_low import TemperatureHighLow
from weathergrabber.domain.adapter.mapper.temperature_high_low_mapper import temperature_high_low_to_dict

def test_temperature_high_low_to_dict():
    thl = TemperatureHighLow("30°", "20°", "Today")
    d = temperature_high_low_to_dict(thl)
    assert d["high"] == "30°"
    assert d["low"] == "20°"
    assert d["label"] == "Today"
    assert isinstance(d, dict)
