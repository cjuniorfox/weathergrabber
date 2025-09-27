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

        city = forecast.current_conditions.location.city
        state_province = forecast.current_conditions.location.state_province
        icon = forecast.current_conditions.icon.fa_icon if is_fa else forecast.current_conditions.icon.emoji_icon
        temperature = forecast.current_conditions.temperature
        summary = forecast.current_conditions.summary

        high_low = forecast.today_details.high_low

        feelslike_icon = WeatherIconEnum.FEEL.fa_icon if is_fa else WeatherIconEnum.FEEL.emoji_icon
        feelslike = forecast.feelslike

        wind_icon = WeatherIconEnum.WIND.fa_icon if is_fa else WeatherIconEnum.WIND.emoji_icon
        wind = forecast.today_details.wind

        humidity_icon = WeatherIconEnum.HUMIDITY.fa_icon if is_fa else WeatherIconEnum.HUMIDITY.emoji_icon
        humidity = forecast.today_details.humidity

        visibility_icon = WeatherIconEnum.VISIBILITY.fa_icon if is_fa else WeatherIconEnum.VISIBILITY.emoji_icon
        visibility = forecast.today_details.visibility

        r, g, b = forecast.air_quality_index.color.red, forecast.air_quality_index.color.green, forecast.air_quality_index.color.blue
        aqi_category = f"\033[38;2;{forecast.air_quality_index.category}\033[0m \n"
        aqi_acronym = forecast.air_quality_index.acronym
        aqi_value = forecast.air_quality_index.value

        print(
            f"\n"
            f"{city}, {state_province}\n"
            "\n"
            f"{icon}      {temperature}\n"
            "\n"
            f"{summary}\n"
            f"{high_low}   {feelslike_icon} {feelslike}"
            f"\n"
            f"{wind_icon} {wind}        {humidity_icon} {humidity}\n"
            f"{visibility_icon} {visibility}      {aqi_acronym} {aqi_value} {aqi_category}"
        )
        

        self.logger.info("Console output executed")