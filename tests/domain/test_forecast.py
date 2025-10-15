import pytest
from weathergrabber.domain.forecast import Forecast

class DummySearch: pass
class DummyCurrentConditions: pass
class DummyTodayDetails: pass
class DummyAirQualityIndex: pass
class DummyHealthActivities: pass
class DummyHourlyPrediction: pass
class DummyDailyPrediction: pass

def test_forecast_properties():
    search = DummySearch()
    current_conditions = DummyCurrentConditions()
    today_details = DummyTodayDetails()
    air_quality_index = DummyAirQualityIndex()
    health_activities = DummyHealthActivities()
    hourly_predictions = [DummyHourlyPrediction() for _ in range(3)]
    daily_predictions = [DummyDailyPrediction() for _ in range(2)]
    forecast = Forecast(
        search,
        current_conditions,
        today_details,
        air_quality_index,
        health_activities,
        hourly_predictions,
        daily_predictions
    )
    assert forecast.search is search
    assert forecast.current_conditions is current_conditions
    assert forecast.today_details is today_details
    assert forecast.air_quality_index is air_quality_index
    assert forecast.health_activities is health_activities
    assert forecast.hourly_predictions == hourly_predictions
    assert forecast.daily_predictions == daily_predictions
    r = repr(forecast)
    assert "Forecast(" in r
    assert "search=" in r
    assert "current_conditions=" in r
    assert "today_details=" in r
    assert "air_quality_index=" in r
    assert "health_activities=" in r
    assert "hourly_predictions=3 items" in r
    assert "daily_predictions=2 items" in r
