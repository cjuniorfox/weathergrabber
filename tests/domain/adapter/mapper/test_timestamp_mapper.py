import pytest
from weathergrabber.domain.timestamp import Timestamp
from weathergrabber.domain.adapter.mapper.timestamp_mapper import timestamp_to_dict

def test_timestamp_to_dict():
    ts = Timestamp(time="16:37", gmt="GMT-03:00", text="As of 16:37 GMT-03:00")
    result = timestamp_to_dict(ts)
    assert result == {"time": "16:37", "gmt": "GMT-03:00", "text": "As of 16:37 GMT-03:00"}
    assert isinstance(result, dict)

def test_timestamp_to_dict_none_text():
    ts = Timestamp(time="20:44", gmt="EDT", text=None)
    result = timestamp_to_dict(ts)
    assert result == {"time": "20:44", "gmt": "EDT", "text": None}
    assert isinstance(result, dict)
