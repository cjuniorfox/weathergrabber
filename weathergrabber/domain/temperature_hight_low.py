class TemperatureHighLow:
    def __init__(self, high: str, low: str):
        self._high = high
        self._low = low

    @classmethod
    def from_string(cls, data: str) -> 'TemperatureHighLow':
        parts = data.split('/')
        if len(parts) == 2:
            high, low = parts
            return cls(high=high.strip(), low=low.strip())
        else:
            raise ValueError("Invalid temperature high/low string format")

    @property
    def high(self) -> str:
        return self._high
    
    @property
    def low(self) -> str:
        return self._low
    
    def __repr__(self):
        return f"TemperatureHighLow(high={self.high!r}, low={self.low!r})"