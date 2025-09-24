from weathergrabber.domain.temperature_hight_low import TemperatureHighLow
from typing import Optional
from weathergrabber.domain.uv_index import UVIndex
from weathergrabber.domain.moon_phase import MoonPhase

class TodayDetails:

    def __init__(
            self,
            high_low: Optional[TemperatureHighLow],
            wind: str,
            humidity: str,
            dew_point: str,
            pressure: str,
            uv_index: Optional[UVIndex],
            visibility: str,
            moon_phase: Optional[MoonPhase]
        ):
        self._high_low = high_low
        self._wind = wind
        self._humidity = humidity
        self._dew_point = dew_point
        self._pressure = pressure
        self._uv_index = uv_index
        self._visibility = visibility
        self._moon_phase = moon_phase

    @property
    def high_low(self) -> Optional[TemperatureHighLow]:
        return self._high_low
    
    @property
    def wind(self) -> str:
        return self._wind
    
    @property
    def humidity(self) -> str:
        return self._humidity
    
    @property
    def dew_point(self) -> str:
        return self._dew_point
    
    @property
    def pressure(self) -> str:
        return self._pressure
    
    @property
    def uv_index(self) -> Optional[UVIndex]:
        return self._uv_index
    
    @property
    def visibility(self) -> str:
        return self._visibility
    
    @property
    def moon_phase(self) -> Optional[MoonPhase]:
        return self._moon_phase

    def __repr__(self) -> str:
        return (f"TodayDetails(high_low={self.high_low}, wind={self.wind!r}, "
                f"humidity={self.humidity!r}, dew_point={self.dew_point!r}, "
                f"pressure={self.pressure!r}, uv_index={self.uv_index}, "
                f"visibility={self.visibility!r}, moon_phase={self.moon_phase})")    