class DummySearch:
    id = "dummy_id"
    search_name = "dummy_name"

class DummyCurrentConditions:
    location = None
    timestamp = None
    temperature = "22°C"
    icon = None
    summary = "Sunny"
    day_night = None

class DummyTodayDetails:
    feelslike = None
    sunrise_sunset = None
    high_low = None
    wind = None
    humidity = None
    dew_point = None
    pressure = None
    uv_index = None
    visibility = None
    moon_phase = None

class DummyAirQualityIndex:
    title = "AQI"
    value = 42
    category = "Good"
    description = "Air quality is good."
    acronym = "AQI"
    color = None

class DummyHealthActivities:
    category_name = "Fitness"
    title = "Running"
    description = "Good for heart health"

class DummyHourlyPrediction:
    title = "10:00 AM"
    temperature = "22°C"
    icon = None
    summary = "Sunny"
    precipitation = None
    wind = None
    feels_like = "21°C"
    humidity = "50%"
    uv_index = None
    cloud_cover = "10%"

class DummyDailyPrediction:
    title = "Today"
    high_low = None
    icon = None
    summary = "Sunny"
    precipitation = None
    moon_phase = None

def dummy_to_dict(obj):
    return {"dummy": True}

from weathergrabber.domain.forecast import Forecast
from weathergrabber.domain.adapter.mapper.forecast_mapper import forecast_to_dict
from weathergrabber.domain.adapter.mapper import search_mapper, current_conditions_mapper, today_details_mapper, air_quality_index_mapper, health_activities_mapper, hourly_predictions_mapper, daily_predictions_mapper


def test_forecast_to_dict():
    forecast = Forecast(
        DummySearch(),
        DummyCurrentConditions(),
        DummyTodayDetails(),
        DummyAirQualityIndex(),
        DummyHealthActivities(),
        [DummyHourlyPrediction(), DummyHourlyPrediction()],
        [DummyDailyPrediction()]
    )
    d = forecast_to_dict(forecast)
    assert d["search"] == {"id": "dummy_id", "search_name": "dummy_name"}
    assert d["current_conditions"] == {
        "location": None,
        "timestamp": None,
        "temperature": "22°C",
        "icon": None,
        "summary": "Sunny",
        "day_night": None,
    }
    assert d["today_details"] == {
        "feelslike": None,
        "sunrise_sunset": None,
        "high_low": None,
        "wind": None,
        "humidity": None,
        "dew_point": None,
        "pressure": None,
        "uv_index": None,
        "visibility": None,
        "moon_phase": None,
    }
    assert d["air_quality_index"] == {
        "title": "AQI",
        "value": 42,
        "category": "Good",
        "description": "Air quality is good.",
        "acronym": "AQI",
        "color": None,
    }
    assert d["health_activities"] == {
        "category_name": "Fitness",
        "title": "Running",
        "description": "Good for heart health",
    }
    assert d["hourly_predictions"] == [
        {
            "title": "10:00 AM",
            "temperature": "22°C",
            "icon": None,
            "summary": "Sunny",
            "precipitation": None,
            "wind": None,
            "feels_like": "21°C",
            "humidity": "50%",
            "uv_index": None,
            "cloud_cover": "10%",
        },
        {
            "title": "10:00 AM",
            "temperature": "22°C",
            "icon": None,
            "summary": "Sunny",
            "precipitation": None,
            "wind": None,
            "feels_like": "21°C",
            "humidity": "50%",
            "uv_index": None,
            "cloud_cover": "10%",
        },
    ]
    assert d["daily_predictions"] == [
        {
            "title": "Today",
            "high_low": None,
            "icon": None,
            "summary": "Sunny",
            "precipitation": None,
            "moon_phase": None,
        }
    ]
    assert isinstance(d, dict)
