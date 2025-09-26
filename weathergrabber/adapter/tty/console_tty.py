from weathergrabber.usecase.use_case import UseCase
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.icon_enum import IconEnum
from weathergrabber.domain.weather_icon_enum import WeatherIconEnum
import logging

class ConsoleTTY:

    def __init__(self, use_case: UseCase):
        self.logger = logging.getLogger(__name__)
        self.use_case = use_case
        pass

    def execute(self, params: Params) -> None:
        self.logger.info("Executing Console output")

        is_fa = params.icons == IconEnum.FA

        forecast = self.use_case.execute(params)
        print(
            f"{forecast.location.city_location.city}, {forecast.location.city_location.state_province}\n"
            "\n"
            f"{forecast.icon.fa_icon if is_fa else forecast.icon.emoji_icon}      {forecast.temperature}\n"
            "\n"
            f"{forecast.today_details.high_low}   {WeatherIconEnum.FEEL.fa_icon if is_fa else WeatherIconEnum.FEEL.emoji_icon} {forecast.feelslike}"
        )
        

        self.logger.info("Console output executed")