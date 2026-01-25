import pytest
from weathergrabber.domain.entities.timestamp import Timestamp
from weathergrabber.domain.adapter.mappers.timestamp_mapper import timestamp_to_dict, dict_to_timestamp

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


def test_dict_to_timestamp():
    data = {
        "time": "14:30",
        "gmt": "GMT-03:00",
        "text": "As of 14:30 GMT-03:00"
    }
    ts = dict_to_timestamp(data)
    assert isinstance(ts, Timestamp)
    assert ts.time == "14:30"
    assert ts.gmt == "GMT-03:00"
    assert ts.text == "As of 14:30 GMT-03:00"


def test_dict_to_timestamp_none_values():
    data = {
        "time": None,
        "gmt": None,
        "text": None
    }
    ts = dict_to_timestamp(data)
    assert ts.time is None
    assert ts.gmt is None
    assert ts.text is None


def test_dict_to_timestamp_missing_keys():
    data = {}
    ts = dict_to_timestamp(data)
    assert ts.time is None
    assert ts.gmt is None
    assert ts.text is None


def test_dict_to_timestamp_with_different_timezones():
    data = {
        "time": "09:00",
        "gmt": "UTC",
        "text": "09:00 UTC"
    }
    ts = dict_to_timestamp(data)
    assert ts.time == "09:00"
    assert ts.gmt == "UTC"


def test_dict_to_timestamp_roundtrip():
    original = Timestamp(time="10:15", gmt="GMT+00:00", text="10:15 UTC")
    data = timestamp_to_dict(original)
    reconstructed = dict_to_timestamp(data)
    assert reconstructed.time == original.time
    assert reconstructed.gmt == original.gmt
    assert reconstructed.text == original.text
