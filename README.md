# Write a Weather forecast widget for Waybar

## Write Python Script class

First, let's define a WeatherForecast class to handle the forecast data

```python
class WeatherForecast:
    class HourlyPrediction:
        def __init__(self, moment: str, temperature: float, status: str, chance_of_rain: float):
            self.moment = moment
            self.temperature = temperature
            self.status = status
            self.chance_of_rain = chance_of_rain
    
    class Temperature:
        def __init__(self, current, feel, min, max):
            self.current = current
            self.feel = feel
            self.min = min
            self.max = max

    def __init__(
        self,
        weather_id: str,
        lang: str,
        location: str,
        status: str,
        status_code: int,
        wind_speed: float,
        humidity: float,
        visibility: float,
        air_quality: str,
        temperature : Dict = None,
        hourly_predictions: List[Dict] = None,
    ):
        self.weather_id = weather_id
        self.lang = lang
        self.location = location
        self.status = status
        self.status_code = status_code
        self.wind_speed = wind_speed
        self.humidity = humidity
        self.visibility = visibility
        self.air_quality = air_quality
        self.temperature = WeatherForecast.Temperature(**temperature),
        self.hourly_predictions = [
            WeatherForecast.HourlyPrediction(**prediction) for prediction in (hourly_predictions or [])
        ]
```

Create a function to grab the forecast data from weather.com. The routine will do as follows

1. Check if the weather id was provided and is correctly formatted (hex format 64 characters long)
2. Check for the computer's language.

If no `weather_id` was provided, it defaults to current location defined by weather.com itself.

If no language was defined, it defaults to`en_IL`.

```python
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
    grab_weather_data(lang, weather_id)
```

Having the weather information, let's extract the intended data. To this, we will create a bunch of functions that receives the HTML data and extract those DOM objects with the wanted data.

