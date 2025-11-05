from weathergrabber.application.services.retrieve_statistics_service import RetrieveStatisticsService

class StatisticsUC:
    def __init__(self, retrieve_statistics_service: RetrieveStatisticsService):
        self.retrieve_statistics_service = retrieve_statistics_service

    def execute(self):
        # Implement statistics calculation logic here
        weather_data = self.retrieve_statistics_service.get_all_weather_data()
        statistics = {
            "total_entries": len(weather_data),
            "average_temperature": sum(entry['temperature'] for entry in weather_data) / len(weather_data) if weather_data else 0,
            # Add more statistics as needed
        }
        return statistics