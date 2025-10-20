class DayNightResponse:
    def __init__(
            self, 
            day: "DayNightResponse.Temperature", 
            night: "DayNightResponse.Temperature"
        ):
        self.day = day
        self.night = night
        
    def __str__(self):
        return f"{self.day}/ {self.night}"
        
    class Temperature:
        def __init__(self, label: str, value: str):
            self.label = label
            self.value = value

        def __str__(self):
            return f"{self.label} {self.value}"