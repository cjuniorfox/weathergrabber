from weathergrabber.domain.entities.temperature_hight_low import TemperatureHighLow
from weathergrabber.domain.adapter.mappers.temperature_high_low_mapper import temperature_high_low_to_dict, dict_to_temperature_high_low

def test_temperature_high_low_to_dict():
    thl = TemperatureHighLow("30°", "20°", "Today")
    d = temperature_high_low_to_dict(thl)
    assert d["high"] == "30°"
    assert d["low"] == "20°"
    assert d["label"] == "Today"
    assert isinstance(d, dict)


def test_dict_to_temperature_high_low():
    data = {
        "high": "30°C",
        "low": "20°C",
        "label": "High/Low"
    }
    thl = dict_to_temperature_high_low(data)
    assert isinstance(thl, TemperatureHighLow)
    assert thl.high == "30°C"
    assert thl.low == "20°C"
    assert thl.label == "High/Low"


def test_dict_to_temperature_high_low_none_values():
    data = {
        "high": None,
        "low": None,
        "label": None
    }
    thl = dict_to_temperature_high_low(data)
    assert thl.high is None
    assert thl.low is None
    assert thl.label is None


def test_dict_to_temperature_high_low_missing_keys():
    data = {}
    thl = dict_to_temperature_high_low(data)
    assert thl.high is None
    assert thl.low is None
    assert thl.label is None


def test_dict_to_temperature_high_low_fahrenheit():
    data = {
        "high": "86°F",
        "low": "68°F",
        "label": "Temperature"
    }
    thl = dict_to_temperature_high_low(data)
    assert thl.high == "86°F"
    assert thl.low == "68°F"


def test_dict_to_temperature_high_low_roundtrip():
    original = TemperatureHighLow(high="25°C", low="15°C", label="Daily")
    data = temperature_high_low_to_dict(original)
    reconstructed = dict_to_temperature_high_low(data)
    assert reconstructed.high == original.high
    assert reconstructed.low == original.low
    assert reconstructed.label == original.label
