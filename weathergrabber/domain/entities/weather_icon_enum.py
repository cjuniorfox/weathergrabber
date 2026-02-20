from enum import Enum

class WeatherIconEnum(Enum):
    # Weather condition icons
    SUNNY = ("sunny", "\uf185", "☀️")
    CLEAR = ("clear", "\uf185", "☀️")
    MOSTLY_SUNNY = ("mostly-sunny", "\uf185", "🌤️")
    PARTLY_CLOUDY_DAY = ("partly-cloudy-day", "\uf6c4", "⛅")
    MOSTLY_CLOUDY_DAY = ("mostly-cloudy-day", "\uf0c2", "🌥️")
    CLOUDY = ("cloudy", "\uf0c2", "☁️")
    CLEAR_NIGHT = ("clear-night", "\uf186", "🌙")
    PARTLY_CLOUDY_NIGHT = ("partly-cloudy-night", "\uf186", "🌃")
    MOSTLY_CLOUDY_NIGHT = ("mostly-cloudy-night", "\uf186", "☁️")
    RAIN = ("rain", "\uf740", "🌧️")
    DRIZZLE = ("drizzle", "\uf73d", "🌦️")
    SHOWERS_RAIN = ("showers-rain", "\uf740", "🌧️")
    T_STORMS = ("t-storms", "\uf76c", "⛈️")
    HEAVY_T_STORMS = ("heavy-t-storms", "\uf76c", "⛈️")
    SNOW = ("snow", "\uf2dc", "❄️")
    HEAVY_SNOW = ("heavy-snow", "\uf2dc", "🌨️")
    SLEET = ("sleet", "\uf7ad", "🌨️")
    WINTRY_MIX = ("wintry-mix", "\uf7ad", "🌨️")
    BLIZZARD = ("blizzard", "\u001b[34m\uf2dc\u001b[0m", "🌨️")
    HEAVY_SNOW_BLIZZARD = ("heavy-snow-blizzard", "\u007f", "🌨️")
    FOG = ("fog", "\uf75f", "🌫️")
    WINDY = ("windy", "\uf72e", "💨")
    HAZY_SUNSHINE = ("hazy-sunshine", "\uf185", "🌤️")
    HAZY_MOONLIGHT = ("hazy-moonlight", "\uf186", "🌙")
    # UI label icons
    SUNRISE = ("sunrise", "\ue34d", "🌅")
    SUNSET = ("sunset", "\ue34e", "🌇")
    DAY = ("day", "\uf185", "🌡️")
    NIGHT = ("night", "\uf186", "🌡️")
    FEEL = ("feel", "\uf2c9", "🌡️")
    HUMIDITY = ("humidity", "\uf773", "💧")
    VISIBILITY = ("visibility", "\uf06e", "👁️")
    WIND = ("wind", "\uf72e", "💨")

    def __init__(self, name: str, fa_icon: str, emoji_icon: str):
        self._name = name
        self._fa_icon = fa_icon
        self._emoji_icon = emoji_icon

    @property
    def name(self):
        return self._name

    @property
    def fa_icon(self):
        return self._fa_icon

    @property
    def emoji_icon(self):
        return self._emoji_icon

    @staticmethod
    def from_name(name: str):
        for item in WeatherIconEnum:
            if item._name == name:
                return item
        raise ValueError(f'WeatherIconEnum: No icon found for name "{name}"')
