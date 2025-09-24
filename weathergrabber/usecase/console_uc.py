from weathergrabber.domain.adapter.params import Params
from weathergrabber.service.read_weather_service import ReadWeatherService
from weathergrabber.service.extract_location_service import ExtractLocationService
from weathergrabber.service.extract_temperature_service import ExtractTemperatureService
from weathergrabber.service.extract_feelslike_temperature_service import ExtractFeelslikeTemperatureService
from weathergrabber.service.extract_icon_service import ExtractIconService
from weathergrabber.service.extract_today_details_service import ExtractTodayDetailsService 

class ConsoleUC:
    def __init__(
        self,
        wheater_data_service: ReadWeatherService,
        extract_location_service: ExtractLocationService,
        extract_temperature_icon_service: ExtractTemperatureService,
        extract_feelslike_temperature_service: ExtractFeelslikeTemperatureService,
        extract_icon_service: ExtractIconService,
        extract_today_details_service: ExtractTodayDetailsService
    ):
        self.read_weather_service = wheater_data_service
        self.extract_location_service = extract_location_service
        self.extract_temperature_service = extract_temperature_icon_service
        self.extract_feelslike_temperature_service = extract_feelslike_temperature_service
        self.extract_icon_service = extract_icon_service
        self.extract_today_details_service = extract_today_details_service

    def execute(self, params: Params) -> None:

        weather_data = self.read_weather_service.execute(params.language, params.location)
        
        location = self.extract_location_service.execute(weather_data)
        temperature = self.extract_temperature_service.execute(weather_data)
        feelslike_temperature = self.extract_feelslike_temperature_service.execute(weather_data)
        icon = self.extract_icon_service.execute(weather_data)
        today_details = self.extract_today_details_service.execute(weather_data)
        
        print(f"Executing console use case with output format Console")