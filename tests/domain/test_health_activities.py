import pytest
from weathergrabber.domain.health_activities import HealthActivities

def test_from_text_valid():
    text = "Health & Activities\nGrass\nSeasonal Allergies and Pollen Count Forecast\nGrass pollen is low in your area"
    ha = HealthActivities.from_text(text)
    assert ha.category_name == "Health & Activities"
    assert ha.title == "Seasonal Allergies and Pollen Count Forecast"
    assert ha.description == "Grass pollen is low in your area"
    assert str(ha).startswith("Health & Activities:")
    assert "category_name=" in repr(ha)

def test_from_text_extra_lines():
    text = "Health & Activities\nGrass\nSeasonal Allergies and Pollen Count Forecast\nGrass pollen is low in your area\nExtra info"
    ha = HealthActivities.from_text(text)
    assert "Extra info" in ha.description

def test_from_text_insufficient_lines():
    text = "Health & Activities\nGrass"
    with pytest.raises(ValueError):
        HealthActivities.from_text(text)

def test_manual_init():
    ha = HealthActivities("Fitness", "Running", "Good for heart health")
    assert ha.category_name == "Fitness"
    assert ha.title == "Running"
    assert ha.description == "Good for heart health"
    assert str(ha) == "Fitness: Running - Good for heart health"
