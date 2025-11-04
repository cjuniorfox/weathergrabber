import pytest
from weathergrabber.domain.entities.health_activities import HealthActivities
from weathergrabber.domain.adapter.mappers.health_activities_mapper import health_activities_to_dict

def test_health_activities_to_dict():
    ha = HealthActivities(category_name="Fitness", title="Running", description="Good for heart health")
    result = health_activities_to_dict(ha)
    assert result == {
        "category_name": "Fitness",
        "title": "Running",
        "description": "Good for heart health"
    }
    assert isinstance(result, dict)

def test_health_activities_to_dict_empty():
    ha = HealthActivities(category_name="", title="", description="")
    result = health_activities_to_dict(ha)
    assert result == {
        "category_name": "",
        "title": "",
        "description": ""
    }
    assert isinstance(result, dict)
