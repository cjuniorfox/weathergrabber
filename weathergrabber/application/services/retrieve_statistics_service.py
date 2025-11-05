from weathergrabber.adapter.repository.forecast_repository import ForecastRepository

class RetrieveStatisticsService:
    def __init__(self, weather_repository: ForecastRepository):
        self.weather_repository = weather_repository
    
    def execute(self):
        return self.weather_repository.get_cache_stats()