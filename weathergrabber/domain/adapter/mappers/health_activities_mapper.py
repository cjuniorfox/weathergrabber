from weathergrabber.domain.entities.health_activities import HealthActivities

def health_activities_to_dict(ha: HealthActivities) -> dict:
    return {
        "category_name": ha.category_name,
        "title": ha.title,
        "description": ha.description,
    }

def dict_to_health_activities(data: dict) -> HealthActivities:
    return HealthActivities(
        category_name=data["category_name"],
        title=data["title"],
        description=data["description"],
    )
