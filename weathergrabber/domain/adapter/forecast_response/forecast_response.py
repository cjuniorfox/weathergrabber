from .humidity_response import HumidityResponse
from .feels_like_response import FeelsLikeResponse
from .sunrise_sunset_response import SunriseSunsetResponse
from .moon_response import MoonResponse
from .day_night_response import DayNightResponse
from .wind_response import WindResponse
from .visibility_response import VisibilityResponse
from .aqi_response import AQIResponse

class ForecastResponse:

    def __init__(
            self, 
            rain_icon: str, 
            city_location: str,
            icon: str,
            temperature: str,
            humidity: HumidityResponse,
            day_night_temp: DayNightResponse,
            moon: MoonResponse,
            summary: str,
            feelslike: FeelsLikeResponse,
            sunrise_sunset: SunriseSunsetResponse,
            wind: WindResponse,
            pressure: str,
            uv_index: str,
            visibility: VisibilityResponse,
            aqi: AQIResponse
        ):
        self.rain_icon = rain_icon
        self.city_location = city_location
        self.icon = icon
        self.temperature = temperature
        self.humidity = humidity
        self.day_night_temp = day_night_temp
        self.moon = moon
        self.summary = summary
        self.feelslike = feelslike
        self.sunrise_sunset = sunrise_sunset
        self.wind = wind
        self.pressure = pressure
        self.uv_index = uv_index
        self.visibility = visibility
        self.aqi = aqi
        
    

