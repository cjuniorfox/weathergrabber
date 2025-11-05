import sqlite3
import json
import os
import tempfile
from datetime import datetime
from typing import Optional
import logging
from weathergrabber.domain.entities.forecast import Forecast

class ForecastRepository:
    def __init__(self, db_path: str = None):
        # Use /tmp directory for ephemeral storage by default
        if db_path is None:
            db_path = os.path.join(tempfile.gettempdir(), "weather_forecasts.db")
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing ForecastRepository with DB path: {db_path}")
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        self.logger.debug("Initializing database and creating tables if they do not exist.")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS forecasts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location_id TEXT NOT NULL,
                        search_name TEXT NOT NULL,
                        forecast_data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                # Create indexes for fast retrieval
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_location_id ON forecasts (location_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_name ON forecasts (search_name)")
                conn.commit()
                self.logger.debug(f"Database initialized successfully at {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Error initializing database: {e}")
            raise

    def save_forecast(self, location_id: str, search_name: str, forecast_data: Forecast) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO forecasts (location_id, search_name, forecast_data, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                location_id,
                search_name,
                json.dumps(forecast_data),
                datetime.now(),
                datetime.now()
            ))
            conn.commit()

    def get_by_location_id(self, location_id: str) -> Optional[Forecast]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT forecast_data FROM forecasts
                WHERE location_id = ? ORDER BY created_at DESC
                LIMIT 1
            ''', (location_id,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None

    def get_by_search_name(self, search_name: str) -> Optional[Forecast]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT forecast_data FROM forecasts
                WHERE search_name = ?
                ORDER BY created_at DESC
                LIMIT 1
            ''', (search_name,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None

    def clear_cache(self) -> None:
        """Clear all cached forecasts from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM forecasts")
                conn.commit()
                self.logger.info("Cache cleared successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Error clearing cache: {e}")

    def get_cache_stats(self) -> dict:
        """Get statistics about the cached forecasts."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM forecasts")
                total_count = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(DISTINCT location_id) as unique_locations,
                           COUNT(DISTINCT search_name) as unique_searches
                    FROM forecasts
                """)
                stats = cursor.fetchone()
                
                return {
                    'total_forecasts': total_count,
                    'unique_locations': stats[0],
                    'unique_searches': stats[1],
                    'database_path': self.db_path
                }
        except sqlite3.Error as e:
            self.logger.error(f"Error getting cache stats: {e}")
            return {'error': str(e)}

    def cleanup_old_forecasts(self, hours_old: int = 24) -> None:
        """Remove forecasts older than specified hours."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM forecasts 
                    WHERE created_at < datetime('now', '-{} hours')
                """.format(hours_old))
                deleted_count = cursor.rowcount
                conn.commit()
                self.logger.info(f"Cleaned up {deleted_count} old forecasts")
        except sqlite3.Error as e:
            self.logger.error(f"Error cleaning up old forecasts: {e}")
