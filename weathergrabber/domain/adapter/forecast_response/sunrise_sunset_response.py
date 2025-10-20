class SunriseSunsetResponse:
    def __init__(
            self, 
            sunrise: "SunriseSunsetResponse.Sun",
            sunset: "SunriseSunsetResponse.Sun"
        ):
        self.sunrise = sunrise
        self.sunset = sunset

    def __str__(self):
        return f"{self.sunrise} • {self.sunset}"

    class Sun:
        def __init__(self, icon: str, value: str):
            self.icon = icon
            self.value = value