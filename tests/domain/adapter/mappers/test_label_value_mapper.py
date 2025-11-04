import pytest
from weathergrabber.domain.entities.label_value import LabelValue
from weathergrabber.domain.adapter.mappers.label_value_mapper import label_value_to_dict

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
