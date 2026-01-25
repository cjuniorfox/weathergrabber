import pytest
from weathergrabber.domain.entities.statistics import Statistics
from weathergrabber.domain.adapter.mappers.statistics_mapper import (
    dict_to_statistics,
    statistics_to_dict
)


@pytest.fixture
def sample_dict():
    return {
        "total_forecasts": 42,
        "unique_locations": 10,
        "unique_search_names": 15,
        "database_path": "/tmp/weather.db"
    }


@pytest.fixture
def sample_dict_with_error():
    return {
        "total_forecasts": 0,
        "unique_locations": 0,
        "unique_search_names": 0,
        "database_path": "/tmp/weather.db",
        "error": "Database connection failed"
    }


@pytest.fixture
def statistics(sample_dict):
    return Statistics(
        total_forecasts=sample_dict["total_forecasts"],
        unique_locations=sample_dict["unique_locations"],
        unique_search_names=sample_dict["unique_search_names"],
        database_path=sample_dict["database_path"]
    )


class TestStatisticsEntity:
    """Tests for Statistics entity."""

    def test_statistics_properties(self, statistics):
        assert statistics.total_forecasts == 42
        assert statistics.unique_locations == 10
        assert statistics.unique_search_names == 15
        assert statistics.database_path == "/tmp/weather.db"
        assert statistics.error is None

    def test_statistics_with_error(self):
        stats = Statistics(
            total_forecasts=0,
            unique_locations=0,
            unique_search_names=0,
            database_path="/tmp/weather.db",
            error="Database error"
        )
        assert stats.error == "Database error"

    def test_statistics_repr(self, statistics):
        repr_str = repr(statistics)
        assert "Statistics" in repr_str
        assert "total_forecasts=42" in repr_str
        assert "unique_locations=10" in repr_str


class TestStatisticsMapper:
    """Tests for statistics mapper functions."""

    def test_dict_to_statistics_success(self, sample_dict):
        stats = dict_to_statistics(sample_dict)

        assert isinstance(stats, Statistics)
        assert stats.total_forecasts == 42
        assert stats.unique_locations == 10
        assert stats.unique_search_names == 15
        assert stats.database_path == "/tmp/weather.db"
        assert stats.error is None

    def test_dict_to_statistics_with_error(self, sample_dict_with_error):
        stats = dict_to_statistics(sample_dict_with_error)

        assert stats.error == "Database connection failed"

    def test_dict_to_statistics_missing_fields(self):
        partial_dict = {"total_forecasts": 5}
        stats = dict_to_statistics(partial_dict)

        assert stats.total_forecasts == 5
        assert stats.unique_locations == 0
        assert stats.unique_search_names == 0
        assert stats.database_path == ""
        assert stats.error is None

    def test_statistics_to_dict_success(self, statistics, sample_dict):
        result = statistics_to_dict(statistics)

        assert result == sample_dict

    def test_statistics_to_dict_with_error(self):
        stats = Statistics(
            total_forecasts=0,
            unique_locations=0,
            unique_search_names=0,
            database_path="/tmp/weather.db",
            error="Connection failed"
        )
        result = statistics_to_dict(stats)

        assert result["error"] == "Connection failed"

    def test_dict_to_statistics_round_trip(self, sample_dict):
        stats = dict_to_statistics(sample_dict)
        result_dict = statistics_to_dict(stats)

        assert result_dict == sample_dict
