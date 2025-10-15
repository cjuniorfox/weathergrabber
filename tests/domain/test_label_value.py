import pytest
from weathergrabber.domain.label_value import LabelValue

def test_label_value_properties():
    lv = LabelValue("Humidity", "50%")
    assert lv.label == "Humidity"
    assert lv.value == "50%"
    assert str(lv) == "Humidity 50%"
    r = repr(lv)
    assert "LabelValue(" in r
    assert "label=" in r
    assert "value=" in r
