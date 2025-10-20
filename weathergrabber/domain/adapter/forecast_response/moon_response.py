class MoonResponse:
    def __init__(self, icon: str, phase: str):
            self.icon = icon
            self.phase = phase

    def __str__(self):
        return f"{self.icon} {self.phase}"