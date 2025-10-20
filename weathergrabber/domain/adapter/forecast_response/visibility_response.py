class VisibilityResponse:
    def __init__(self, icon: str, value: str):
        self.icon = icon
        self.value = value

    def __str__(self):
        return f"{self.icon} {self.value}"