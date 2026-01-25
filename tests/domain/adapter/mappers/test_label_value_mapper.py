import pytest
from weathergrabber.domain.entities.label_value import LabelValue
from weathergrabber.domain.adapter.mappers.label_value_mapper import label_value_to_dict, dict_to_label_value

def test_label_value_to_dict():
    lv = LabelValue(label="Humidity", value="60%")
    result = label_value_to_dict(lv)
    assert result == {"label": "Humidity", "value": "60%"}
    assert isinstance(result, dict)

def test_label_value_to_dict_empty():
    lv = LabelValue(label="", value="")
    result = label_value_to_dict(lv)
    assert result == {"label": "", "value": ""}
    assert isinstance(result, dict)


def test_dict_to_label_value():
    data = {"label": "Humidity", "value": "60%"}
    lv = dict_to_label_value(data)
    assert isinstance(lv, LabelValue)
    assert lv.label == "Humidity"
    assert lv.value == "60%"


def test_dict_to_label_value_empty():
    data = {"label": "", "value": ""}
    lv = dict_to_label_value(data)
    assert lv.label == ""
    assert lv.value == ""


def test_dict_to_label_value_with_special_chars():
    data = {"label": "Sensação térmica", "value": "23°C"}
    lv = dict_to_label_value(data)
    assert lv.label == "Sensação térmica"
    assert lv.value == "23°C"


def test_dict_to_label_value_roundtrip():
    original = LabelValue(label="Wind Speed", value="25 km/h")
    data = label_value_to_dict(original)
    reconstructed = dict_to_label_value(data)
    assert reconstructed.label == original.label
    assert reconstructed.value == original.value
