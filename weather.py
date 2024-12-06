from typing import List, Dict
import json, os
from pyquery import PyQuery as pq
from urllib.error import HTTPError

weather_icons_fa = {
    'sunnyDay': '\uf185',        # FA Sun
    'clearNight': '\uf186',      # FA Moon
    'cloudyFoggyDay': '\uf6c4',  # FA Cloud-Sun
    'cloudyFoggyNight': '\uf6c3',# FA Cloud-Moon
    'rainyDay': '\uf73d',        # FA Cloud-Sun-Rain
    'rainyNight': '\uf73c',      # FA Cloud-Moon-Rain
    'snowyIcyDay': '\uf2dc',     # FA Snowflake
    'snowyIcyNight': '\uf2dc',   # FA Snowflake (reuse)
    'severe': '\uf76c',          # FA Cloud-Showers-Heavy
    'default': '\uf0c2'          # FA Cloud
}

# Define weather emojis
weather_icons_emoji = {
    'sunnyDay': ' ',
    'clearNight': '🌙',
    'cloudyFoggyDay': '⛅',
    'cloudyFoggyNight': '🌥️',
    'rainyDay': '🌧️',
    'rainyNight': '🌧️',
    'snowyIcyDay': ' ',
    'snowyIcyNight': ' ',
    'severe': '🌩️',
    'default': ' '
}

class WeatherForecast:
    class Prediction:
        def __init__(
                self, 
                moment: str, 
                status: str,
                skycode : str,
                chance_of_rain: str, 
                temperature: str = None, 
                min: str = None, 
                max: str = None
        ):
            self.moment = moment
            self.status = status
            self.skycode = skycode
            self.chance_of_rain = chance_of_rain
            self.temperature = temperature
            self.min = min
            self.max = max
    
    class Temperature:
        def __init__(
                self, 
                current: str, 
                feel: str, 
                max: str, 
                min: str):
            self.current = current
            self.feel = feel
            self.max = max
            self.min = min

    def __init__(
        self,
        weather_id: str,
        lang: str,
        location: str,
        status: str,
        status_code: str,
        icon: str,
        wind_speed: str,
        humidity: str,
        visibility: str,
        air_quality: str,
        temperature : Dict = None,
        hourly_predictions: List[Dict] = None,
        daily_predictions: List[Dict] = None
    ):
        self.weather_id = weather_id
        self.lang = lang
        self.location = location
        self.status = status
        self.status_code = status_code
        self.icon = icon
        self.wind_speed = wind_speed
        self.humidity = humidity
        self.visibility = visibility
        self.air_quality = air_quality
        self.temperature = WeatherForecast.Temperature(**temperature),
        self.hourly_predictions = [
            WeatherForecast.Prediction(**hourly_prediction) for hourly_prediction in (hourly_predictions or [])
        ]
        self.daily_predictions = [
            WeatherForecast.Prediction(**daily_predicion) for daily_predicion in (daily_predictions or [])
        ]

class WeatherForecastExtractor:
    class TemperatureExtractor:
        def __init__(self, html_data):
            self.html_data = html_data
        
        def current(self):
            return self.html_data("span[data-testid='TemperatureValue']").eq(0).text()
        
        def feel(self):
            return self.html_data(
                "div[data-testid='FeelsLikeSection'] > span > span[data-testid='TemperatureValue']"
                ).text()
        def max(self):
            return self.html_data(
                "div[data-testid='wxData'] > span[data-testid='TemperatureValue']"
                ).eq(0).text()
        def min(self):
            return self.html_data(
                "div[data-testid='wxData'] > span[data-testid='TemperatureValue']"
                ).eq(1).text()
        
    def __init__(self, html_data):
        self.html_data = html_data
        self.temperature = WeatherForecastExtractor.TemperatureExtractor(self.html_data)

    def location(self):
        return self.html_data("h1").text()

    def status(self):
        status = self.html_data("div[data-testid='wxPhrase']").text()
        status = f"{status[:16]}.." if len(status) > 17 else status
        return status
    
    def status_code(self):
        return self.html_data("#regionHeader").attr("class").split(" ")[2].split("-")[2]
    
    def icon(self):
        status_code = self.status_code()
        return (
            weather_icons_emoji[status_code] if status_code in weather_icons_emoji else weather_icons_emoji["default"]
        )

    def wind_speed(self):
        return self.html_data("span[data-testid='Wind']").text().split("\n")[1]
    
    def humidity(self):
        return self.html_data("span[data-testid='PercentageValue']").text()
    
    def visibility(self):
        return self.html_data("span[data-testid='VisibilityValue']").text()

    def air_quality(self):
        return self.html_data("text[data-testid='DonutChartValue']").text()
    
    def hourly_predictions(self):
        predictions = [
            {
                'moment': pq(span)("h3 > span").text(),
                'temperature': pq(span)("span[data-testid='TemperatureValue']").text(),
                'status' : pq(span)("svg[data-testid='Icon'] title").contents()[0],
                'skycode' :  pq(span)("svg[data-testid='Icon']").attr('skycode'),
                'chance_of_rain' : pq(span)("div[data-testid='SegmentPrecipPercentage'] > span").contents()[-1],
            }
                for span in self.html_data("section[data-testid='HourlyWeatherModule'] ul[data-testid='WeatherTable'] li")
            ]
        return predictions
    
    def daily_predictions(self):
        predictions = [
            {
                'moment': pq(span)("h3 > span").text(),
                'max': pq(span)("div[data-testid='SegmentHighTemp'] span[data-testid='TemperatureValue']").eq(0).text(),
                'min': pq(span)("div[data-testid='SegmentHighTemp'] span[data-testid='TemperatureValue']").eq(1).text(),
                'status' : pq(span)("svg[data-testid='Icon'] title").contents()[0],
                'skycode' :  pq(span)("svg[data-testid='Icon']").attr('skycode'),
                'chance_of_rain' : pq(span)("div[data-testid='SegmentPrecipPercentage'] span").contents()[-1],
            }
                for span in self.html_data("section[data-testid='DailyWeatherModule'] ul[data-testid='WeatherTable'] li")
            ]
        return predictions
    
    def to_weather_forecast(self, weather_id: str, lang: str) -> WeatherForecast:
        return WeatherForecast(
            weather_id=weather_id,
            lang=lang,
            location=self.location(),
            status=self.status(),
            status_code=self.status_code(),
            icon=self.icon(),
            wind_speed=self.wind_speed(),
            humidity=self.humidity(),
            visibility=self.visibility(),
            air_quality=self.air_quality(),
            temperature={
                "current": self.temperature.current(),
                "feel": self.temperature.feel(),
                "max": self.temperature.max(),
                "min": self.temperature.min(),
            },
            hourly_predictions=self.hourly_predictions(),
            daily_predictions=self.daily_predictions()  
        )


def serializer(obj):
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def grab_weather_data(lang, weather_id = None) -> str :
    url = f"https://weather.com/{lang}/weather/today/l/{weather_id}"
    if not weather_id:
        url = f"https://weather.com/{lang}/weather/today"
    elif len(weather_id) < 64 :
        raise ValueError("Invalid weather_id")
    if not lang:
        raise ValueError("lang must be specified")
    try:
        return pq(url=url)
    except HTTPError as e:
        if(e.code == 404):
            raise ValueError(f"HTTP error {e.code} when fetching weather data. Check for the location_id or lang data.")
    

def get_weather_forecast(lang, weather_id = None) -> WeatherForecast:
    html_data = grab_weather_data(lang, weather_id)
    forecast = WeatherForecastExtractor(html_data) 
    return forecast.to_weather_forecast(weather_id,lang)

## Get current locale, or use the default one
lang = os.getenv("LANG","en_IL.UTF-8").split(".")[0].replace("_","-")


print(json.dumps(get_weather_forecast(lang=lang,weather_id='2bf40a7aa6288f1090ab35632ce451a0014b11f0b4c370b8cd4d9a018d880a3a'),default=serializer, indent=2))