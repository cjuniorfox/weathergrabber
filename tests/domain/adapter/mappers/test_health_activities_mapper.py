import pytest
from weathergrabber.domain.entities.health_activities import HealthActivities
from weathergrabber.domain.adapter.mappers.health_activities_mapper import health_activities_to_dict, dict_to_health_activities

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


def test_dict_to_health_activities():
    data = {
        "category_name": "Fitness",
        "title": "Running",
        "description": "Good for heart health"
    }
    ha = dict_to_health_activities(data)
    assert isinstance(ha, HealthActivities)
    assert ha.category_name == "Fitness"
    assert ha.title == "Running"
    assert ha.description == "Good for heart health"


def test_dict_to_health_activities_empty():
    data = {
        "category_name": "",
        "title": "",
        "description": ""
    }
    ha = dict_to_health_activities(data)
    assert ha.category_name == ""
    assert ha.title == ""
    assert ha.description == ""


def test_dict_to_health_activities_with_special_chars():
    data = {
        "category_name": "Saúde",
        "title": "Corrida",
        "description": "Ótimo para a saúde do coração"
    }
    ha = dict_to_health_activities(data)
    assert ha.category_name == "Saúde"
    assert ha.title == "Corrida"
    assert ha.description == "Ótimo para a saúde do coração"


def test_dict_to_health_activities_roundtrip():
    original = HealthActivities(
        category_name="Sports",
        title="Swimming",
        description="Excellent full-body exercise"
    )
    data = health_activities_to_dict(original)
    reconstructed = dict_to_health_activities(data)
    assert reconstructed.category_name == original.category_name
    assert reconstructed.title == original.title
    assert reconstructed.description == original.description
