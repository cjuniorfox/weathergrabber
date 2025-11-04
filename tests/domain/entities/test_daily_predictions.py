import pytest
from weathergrabber.domain.entities.daily_predictions import DailyPredictions

class DummyHighLow:
    pass
class DummyIcon:
    pass
class DummyPrecipitation:
    pass
class DummyMoonPhase:
    pass

def test_daily_predictions_properties():
    title = "Today"
    high_low = DummyHighLow()
    icon = DummyIcon()
    summary = "Sunny"
    precipitation = DummyPrecipitation()
    moon_phase = DummyMoonPhase()
    dp = DailyPredictions(title, high_low, icon, summary, precipitation, moon_phase)
    assert dp.title == "Today"
    assert dp.high_low is high_low
    assert dp.icon is icon
    assert dp.summary == "Sunny"
    assert dp.precipitation is precipitation
    assert dp.moon_phase is moon_phase
    # Check repr output
    r = repr(dp)
    assert "DailyPredictions(" in r
    assert "title=" in r
    assert "high_low=" in r
    assert "icon=" in r
    assert "summary=" in r
    assert "precipitation=" in r
    assert "moon_phase=" in r
