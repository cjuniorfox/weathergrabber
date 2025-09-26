from typing import Optional, List
from .location import Location
from .weather_icon_enum import WeatherIconEnum
from .today_details import TodayDetails
from .air_quality_index import AirQualityIndex
from .health_activities import HealthActivities
from .hourly_predictions import HourlyPredictions
from .daily_predictions import DailyPredictions


class Forecast:
    def __init__(
        self,
        location: Optional[Location],
        temperature: str,
        feelslike: str,
        icon: Optional[WeatherIconEnum],
        today_details: Optional[TodayDetails],
        air_quality_index: Optional[AirQualityIndex],
        health_activities: Optional[HealthActivities],
        hourly_predictions: List[HourlyPredictions],
        daily_predictions: List[DailyPredictions],
    ):
        self._location = location
        self._temperature = temperature
        self._feelslike = feelslike
        self._icon = icon
        self._today_details = today_details
        self._air_quality_index = air_quality_index
        self._health_activities = health_activities
        self._hourly_predictions = hourly_predictions
        self._daily_predictions = daily_predictions

    @property
    def location(self) -> Optional[Location]:
        return self._location

    @property
    def temperature(self) -> str:
        return self._temperature

    @property
    def feelslike(self) -> str:
        return self._feelslike

    @property
    def icon(self) -> Optional[WeatherIconEnum]:
        return self._icon

    @property
    def today_details(self) -> Optional[TodayDetails]:
        return self._today_details

    @property
    def air_quality_index(self) -> Optional[AirQualityIndex]:
        return self._air_quality_index

    @property
    def health_activities(self) -> Optional[HealthActivities]:
        return self._health_activities

    @property
    def hourly_predictions(self) -> List[HourlyPredictions]:
        return self._hourly_predictions

    @property
    def daily_predictions(self) -> List[DailyPredictions]:
        return self._daily_predictions

    def __repr__(self) -> str:
        return (
            f"Forecast(location={self._location}, "
            f"temperature='{self._temperature}', "
            f"feelslike='{self._feelslike}', "
            f"icon={self._icon}, "
            f"today_details={self._today_details}, "
            f"air_quality_index={self._air_quality_index}, "
            f"health_activities={self._health_activities}, "
            f"hourly_predictions={len(self._hourly_predictions)} items, "
            f"daily_predictions={len(self._daily_predictions)} items)"
        )
