class UVIndex:
    
    def __init__(self, string_value: str, index: str, of: str, observation:str = None):
        self._string_value = string_value
        self._index = index
        self._of = of
        self._observation = observation

    @property
    def string_value(self) -> str:
        return self._string_value

    @property
    def index(self) -> str:
        return self._index
    
    @property
    def of(self) -> str:
        return self._of
    
    @property
    def observation(self) -> str:
        return self._observation
    
    @classmethod
    def from_string(cls, data: str) -> 'UVIndex':
        parts = data.split(' ')
        if len(parts) == 3:
            index, of, some = parts
            return cls(data, index=index.strip(), of=some.strip())
        elif len(parts) == 1:
            parts
            return cls(data, index=None, of=None, observation=parts.strip())
        else:
            raise ValueError("Invalid UV index string format")
    
    def __repr__(self) -> str:
        return f"UVIndex(string_value={self.string_value!r}, index={self.index!r}, of={self.of!r}, observation={self.observation!r})"