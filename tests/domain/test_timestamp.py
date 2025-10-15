import pytest
from weathergrabber.domain.timestamp import Timestamp

def test_timestamp_properties():
    ts = Timestamp("16:37", "GMT-03:00", "As of 16:37 GMT-03:00")
    assert ts.time == "16:37"
    assert ts.gmt == "GMT-03:00"
    assert ts.text == "As of 16:37 GMT-03:00"
    assert str(ts) == "As of 16:37 GMT-03:00"
    r = repr(ts)
    assert "Timestamp(" in r
    assert "time='16:37'" in r
    assert "gmt='GMT-03:00'" in r
    assert "text='As of 16:37 GMT-03:00'" in r

def test_timestamp_str_without_text():
    ts = Timestamp("20:44", "EDT")
    assert str(ts) == "As of 20:44 EDT"

def test_from_string_gmt():
    ts = Timestamp.from_string("As of 4:23 pm GMT-03:00")
    assert ts.time == "4:23 pm"
    assert ts.gmt == "GMT-03:00"
    assert ts.text == "As of 4:23 pm GMT-03:00"

def test_from_string_abbreviation():
    ts = Timestamp.from_string("Até 20:44 EDT")
    assert ts.time == "20:44"
    assert ts.gmt == "EDT"
    assert ts.text == "Até 20:44 EDT"
