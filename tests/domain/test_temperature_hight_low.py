import pytest
from weathergrabber.domain.temperature_hight_low import TemperatureHighLow

def test_temperature_high_low_properties():
    thl = TemperatureHighLow("30°", "20°", "Today")
    assert thl.high == "30°"
    assert thl.low == "20°"
    assert thl.label == "Today"
    assert str(thl) == "30°/20°"
    r = repr(thl)
    assert "TemperatureHighLow(" in r
    assert "high='30°'" in r
    assert "low='20°'" in r
    assert "label='Today'" in r

def test_from_string_valid():
    thl = TemperatureHighLow.from_string("28°/18°", "Tomorrow")
    assert thl.high == "28°"
    assert thl.low == "18°"
    assert thl.label == "Tomorrow"
    assert str(thl) == "28°/18°"

def test_from_string_invalid():
    with pytest.raises(ValueError):
        TemperatureHighLow.from_string("invalid", "BadLabel")
