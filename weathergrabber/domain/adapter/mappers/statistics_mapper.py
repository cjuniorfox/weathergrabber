from weathergrabber.domain.entities.statistics import Statistics


def statistics_to_dict(statistics: Statistics) -> dict:
    """Convert a Statistics entity to a dictionary."""
    data = {
        "total_forecasts": statistics.total_forecasts,
        "unique_locations": statistics.unique_locations,
        "unique_search_names": statistics.unique_search_names,
        "database_path": statistics.database_path,
    }
    if statistics.error:
        data["error"] = statistics.error
    return data


def dict_to_statistics(data: dict) -> Statistics:
    """Convert a dictionary to a Statistics entity."""
    return Statistics(
        total_forecasts=data.get("total_forecasts", 0),
        unique_locations=data.get("unique_locations", 0),
        unique_search_names=data.get("unique_search_names", 0),
        database_path=data.get("database_path", ""),
        error=data.get("error")
    )
