class AirQualityIndex:
    def __init__(self, aqi: int, category: str = None, description: str = None):
        self._aqi = aqi
        self._category = category
        self._description = description

    @property
    def aqi(self) -> int:
        return self._aqi
    
    @property
    def category(self) -> str | None:
        return self._category
    
    @property
    def description(self) -> str | None:
        return self._description
    
    def __str__(self) -> str:
        return f"AQI: {self._aqi}, Category: {self._category}, Description: {self._description}"
    
    def __repr__(self) -> str:
        return f"AirQualityIndex(aqi={self._aqi}, category={self._category}, description={self._description})"
    
    # '26\nGood\nAir quality is considered satisfactory, and air pollution poses little or no risk.'
    @staticmethod
    def from_string(data: str) -> 'AirQualityIndex':
        try:
            parts = data.split('\n')
            aqi = int(parts[0])
            category = parts[1] if len(parts) > 1 else None
            description = parts[2] if len(parts) > 2 else None
            return AirQualityIndex(aqi, category, description)
        except (ValueError, IndexError) as e:
            raise ValueError("Invalid AQI data format") from e