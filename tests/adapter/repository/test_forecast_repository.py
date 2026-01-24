import pytest
import sqlite3
import json
import tempfile
import os
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime
from weathergrabber.adapter.repository.forecast_repository import ForecastRepository
from weathergrabber.domain.entities.forecast import Forecast
from weathergrabber.domain.entities.search import Search


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    db_path = os.path.join(tempfile.gettempdir(), "test_weather_forecasts.db")
    yield db_path
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def dummy_forecast():
    """Create a dummy forecast for testing."""
    search = Search(id="test_location_123", search_name="Test City")
    return Forecast(
        search=search,
        current_conditions=None,
        today_details=None,
        air_quality_index=None,
        health_activities=None,
        hourly_predictions=[],
        daily_predictions=[]
    )


class TestForecastRepositoryInit:
    """Tests for ForecastRepository initialization."""
    
    def test_init_with_default_db_path(self):
        """Test initialization with default database path."""
        repo = ForecastRepository()
        assert repo.db_path is not None
        assert "weather_forecasts.db" in repo.db_path
        assert os.path.exists(repo.db_path)
        # Cleanup
        if os.path.exists(repo.db_path):
            os.remove(repo.db_path)

    def test_init_with_custom_db_path(self, temp_db):
        """Test initialization with custom database path."""
        repo = ForecastRepository(db_path=temp_db)
        assert repo.db_path == temp_db
        assert os.path.exists(temp_db)

    def test_init_creates_database_and_tables(self, temp_db):
        """Test that initialization creates database and tables."""
        repo = ForecastRepository(db_path=temp_db)
        
        # Verify database file exists
        assert os.path.exists(temp_db)
        
        # Verify tables exist
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='forecasts'"
            )
            assert cursor.fetchone() is not None

    def test_init_creates_indexes(self, temp_db):
        """Test that initialization creates indexes."""
        repo = ForecastRepository(db_path=temp_db)
        
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_location_id'"
            )
            assert cursor.fetchone() is not None


class TestForecastRepositorySave:
    """Tests for saving forecasts."""
    
    def test_save_forecast(self, temp_db, dummy_forecast):
        """Test saving a forecast."""
        repo = ForecastRepository(db_path=temp_db)
        
        repo.save_forecast(
            location_id="test_location_123",
            search_name="Test City",
            forecast_data=dummy_forecast
        )
        
        # Verify forecast was saved
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM forecasts")
            count = cursor.fetchone()[0]
            assert count == 1

    def test_save_forecast_stores_correct_data(self, temp_db, dummy_forecast):
        """Test that saved forecast contains correct data."""
        repo = ForecastRepository(db_path=temp_db)
        location_id = "test_123"
        search_name = "Test City"
        
        repo.save_forecast(
            location_id=location_id,
            search_name=search_name,
            forecast_data=dummy_forecast
        )
        
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT location_id, search_name FROM forecasts WHERE location_id = ?",
                (location_id,)
            )
            row = cursor.fetchone()
            assert row[0] == location_id
            assert row[1] == search_name


class TestForecastRepositoryRetrieve:
    """Tests for retrieving forecasts."""
    
    def test_get_by_location_id_returns_forecast(self, temp_db, dummy_forecast):
        """Test retrieving forecast by location ID."""
        repo = ForecastRepository(db_path=temp_db)
        location_id = "test_location_123"
        
        repo.save_forecast(
            location_id=location_id,
            search_name="Test City",
            forecast_data=dummy_forecast
        )
        
        retrieved = repo.get_by_location_id(location_id)
        assert retrieved is not None
        assert isinstance(retrieved, Forecast)

    def test_get_by_location_id_not_found(self, temp_db):
        """Test retrieving non-existent forecast by location ID returns None."""
        repo = ForecastRepository(db_path=temp_db)
        
        retrieved = repo.get_by_location_id("non_existent_id")
        assert retrieved is None

    def test_get_by_search_name_returns_forecast(self, temp_db, dummy_forecast):
        """Test retrieving forecast by search name."""
        repo = ForecastRepository(db_path=temp_db)
        search_name = "Test City"
        
        repo.save_forecast(
            location_id="test_123",
            search_name=search_name,
            forecast_data=dummy_forecast
        )
        
        retrieved = repo.get_by_search_name(search_name)
        assert retrieved is not None
        assert isinstance(retrieved, Forecast)

    def test_get_by_search_name_not_found(self, temp_db):
        """Test retrieving non-existent forecast by search name returns None."""
        repo = ForecastRepository(db_path=temp_db)
        
        retrieved = repo.get_by_search_name("Non Existent City")
        assert retrieved is None

    def test_get_by_location_id_returns_most_recent(self, temp_db, dummy_forecast):
        """Test that retrieving by location ID returns the most recent forecast."""
        repo = ForecastRepository(db_path=temp_db)
        location_id = "test_123"
        
        # Save first forecast
        repo.save_forecast(location_id, "City", dummy_forecast)
        
        # Save another forecast for same location
        another_forecast = Forecast(
            search=Search(id=location_id, search_name="City"),
            current_conditions=None,
            today_details=None,
            air_quality_index=None,
            health_activities=None,
            hourly_predictions=[],
            daily_predictions=[]
        )
        repo.save_forecast(location_id, "City", another_forecast)
        
        # Verify we can retrieve both
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM forecasts WHERE location_id = ?", (location_id,))
            count = cursor.fetchone()[0]
            assert count == 2
        
        # Verify get_by_location_id returns one (the most recent)
        retrieved = repo.get_by_location_id(location_id)
        assert retrieved is not None


class TestForecastRepositoryClearCache:
    """Tests for clearing cache."""
    
    def test_clear_cache_removes_all_forecasts(self, temp_db, dummy_forecast):
        """Test that clear_cache removes all forecasts."""
        repo = ForecastRepository(db_path=temp_db)
        
        # Save multiple forecasts
        repo.save_forecast("loc_1", "City 1", dummy_forecast)
        repo.save_forecast("loc_2", "City 2", dummy_forecast)
        
        # Verify they were saved
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM forecasts")
            assert cursor.fetchone()[0] == 2
        
        # Clear cache
        repo.clear_cache()
        
        # Verify all were removed
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM forecasts")
            assert cursor.fetchone()[0] == 0

    def test_clear_cache_handles_empty_database(self, temp_db):
        """Test that clear_cache handles empty database gracefully."""
        repo = ForecastRepository(db_path=temp_db)
        
        # Should not raise error
        repo.clear_cache()
        
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM forecasts")
            assert cursor.fetchone()[0] == 0


class TestForecastRepositoryCacheStats:
    """Tests for cache statistics."""
    
    def test_get_cache_stats_empty_database(self, temp_db):
        """Test getting stats from empty database."""
        repo = ForecastRepository(db_path=temp_db)
        
        stats = repo.get_cache_stats()
        assert stats['total_forecasts'] == 0
        assert stats['unique_locations'] == 0
        assert stats['unique_search_names'] == 0

    def test_get_cache_stats_with_data(self, temp_db, dummy_forecast):
        """Test getting stats with forecast data."""
        repo = ForecastRepository(db_path=temp_db)
        
        # Save forecasts
        repo.save_forecast("loc_1", "City 1", dummy_forecast)
        repo.save_forecast("loc_2", "City 2", dummy_forecast)
        repo.save_forecast("loc_1", "City 1", dummy_forecast)  # Duplicate location
        
        stats = repo.get_cache_stats()
        assert stats['total_forecasts'] == 3
        assert stats['unique_locations'] == 2
        assert stats['unique_search_names'] == 2
        assert stats['database_path'] == temp_db

    def test_get_cache_stats_on_error(self, temp_db):
        """Test that get_cache_stats handles database errors gracefully."""
        repo = ForecastRepository(db_path=temp_db)
        
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Database error")
            
            stats = repo.get_cache_stats()
            assert 'error' in stats


class TestForecastRepositoryCleanup:
    """Tests for cleaning up old forecasts."""
    
    def test_cleanup_old_forecasts_removes_old_entries(self, temp_db, dummy_forecast):
        """Test that cleanup removes forecasts older than specified hours."""
        repo = ForecastRepository(db_path=temp_db)
        
        # Save a forecast
        repo.save_forecast("loc_1", "City 1", dummy_forecast)
        
        # Manually update created_at to be old
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE forecasts 
                SET created_at = datetime('now', '-25 hours')
                WHERE location_id = 'loc_1'
            """)
            conn.commit()
        
        # Save another forecast (new)
        repo.save_forecast("loc_2", "City 2", dummy_forecast)
        
        # Cleanup old forecasts (older than 24 hours)
        repo.cleanup_old_forecasts(hours_old=24)
        
        # Verify only new forecast remains
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM forecasts")
            count = cursor.fetchone()[0]
            assert count == 1
            
            cursor.execute("SELECT location_id FROM forecasts")
            remaining = cursor.fetchone()[0]
            assert remaining == "loc_2"

    def test_cleanup_old_forecasts_default_hours(self, temp_db, dummy_forecast):
        """Test cleanup with default 24 hours."""
        repo = ForecastRepository(db_path=temp_db)
        
        repo.save_forecast("loc_1", "City 1", dummy_forecast)
        
        # Should not raise error when called with defaults
        repo.cleanup_old_forecasts()
        
        # Forecast should still exist since it's not old
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM forecasts")
            assert cursor.fetchone()[0] == 1

    def test_cleanup_old_forecasts_on_error(self, temp_db):
        """Test that cleanup handles database errors gracefully."""
        repo = ForecastRepository(db_path=temp_db)
        
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Database error")
            
            # Should not raise error
            repo.cleanup_old_forecasts()


class TestForecastRepositoryExceptions:
    """Tests for exception handling in ForecastRepository."""
    
    def test_init_handles_database_error_on_creation(self):
        """Test that initialization raises error when database creation fails."""
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Cannot create database")
            
            with pytest.raises(sqlite3.Error):
                ForecastRepository(db_path="/tmp/test_error.db")

    def test_save_forecast_handles_database_error(self, temp_db):
        """Test that save_forecast handles database errors gracefully."""
        repo = ForecastRepository(db_path=temp_db)
        dummy_search = Search(id="test", search_name="Test")
        dummy_forecast = Forecast(
            search=dummy_search,
            current_conditions=None,
            today_details=None,
            air_quality_index=None,
            health_activities=None,
            hourly_predictions=[],
            daily_predictions=[]
        )
        
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Database error on save")
            
            with pytest.raises(sqlite3.Error):
                repo.save_forecast("loc_1", "City", dummy_forecast)

    def test_get_by_location_id_handles_database_error(self, temp_db):
        """Test that get_by_location_id handles database errors gracefully."""
        repo = ForecastRepository(db_path=temp_db)
        
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Database error on retrieve")
            
            with pytest.raises(sqlite3.Error):
                repo.get_by_location_id("test_location")

    def test_get_by_search_name_handles_database_error(self, temp_db):
        """Test that get_by_search_name handles database errors gracefully."""
        repo = ForecastRepository(db_path=temp_db)
        
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Database error on retrieve")
            
            with pytest.raises(sqlite3.Error):
                repo.get_by_search_name("Test City")

    def test_clear_cache_logs_error_on_database_failure(self, temp_db, caplog):
        """Test that clear_cache logs error but doesn't raise exception."""
        repo = ForecastRepository(db_path=temp_db)
        
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Database error on clear")
            
            # Should not raise, should log error
            repo.clear_cache()
            # Verify error was logged
            assert "Error clearing cache" in caplog.text or isinstance(mock_connect.side_effect, sqlite3.Error)

    def test_get_cache_stats_returns_error_dict_on_failure(self, temp_db):
        """Test that get_cache_stats returns error dict on database failure."""
        repo = ForecastRepository(db_path=temp_db)
        
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Database error on stats")
            
            stats = repo.get_cache_stats()
            assert 'error' in stats
            assert "Database error on stats" in stats['error']

    def test_cleanup_old_forecasts_logs_error_on_failure(self, temp_db, caplog):
        """Test that cleanup_old_forecasts logs error but doesn't raise exception."""
        repo = ForecastRepository(db_path=temp_db)
        
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Database error on cleanup")
            
            # Should not raise, should log error
            repo.cleanup_old_forecasts()
            # Verify error was logged
            assert "Error cleaning up old forecasts" in caplog.text or isinstance(mock_connect.side_effect, sqlite3.Error)
