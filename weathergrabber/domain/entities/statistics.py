from typing import Optional


class Statistics:
    def __init__(
        self,
        total_forecasts: int,
        unique_locations: int,
        unique_search_names: int,
        database_path: str,
        error: Optional[str] = None
    ):
        self._total_forecasts = total_forecasts
        self._unique_locations = unique_locations
        self._unique_search_names = unique_search_names
        self._database_path = database_path
        self._error = error
        
    @property
    def total_forecasts(self) -> int:
        return self._total_forecasts
    
    @property
    def unique_locations(self) -> int:
        return self._unique_locations
    
    @property
    def unique_search_names(self) -> int:
        return self._unique_search_names
    
    @property
    def database_path(self) -> str:
        return self._database_path

    @property
    def error(self) -> Optional[str]:
        return self._error
    
    def __repr__(self):
        return (
            f"Statistics(total_forecasts={self.total_forecasts!r}, "
            f"unique_locations={self.unique_locations!r}, "
            f"unique_search_names={self.unique_search_names!r}, "
            f"database_path={self.database_path!r}, "
            f"error={self.error!r})"
        )
