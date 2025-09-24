from weathergrabber.domain.adapter.params import Params
from weathergrabber.service.read_weather_service import ReadWeatherService

class ConsoleUC:
    def __init__(
        self,
        wheater_data_service: ReadWeatherService
    ):
        self.read_weather_service = wheater_data_service
        pass

    def execute(self, params: Params) -> None:

        weather_data = self.read_weather_service.execute(params.language, params.location)

        print(f"Executing console use case with output format Console")