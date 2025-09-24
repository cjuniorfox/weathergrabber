from weathergrabber.domain.output_enum import OutputEnum

class Params:
    def __init__(
            self,
            location: str,
            language: str = "en-US",
            output_format: OutputEnum = OutputEnum.CONSOLE,
            persist: bool = False,
            icons: str = "emoji"
        ):
        self._location = location
        self._language = language
        self._output_format = output_format
        self._persist = persist
        self._icons = icons

    @property
    def location(self) -> str:
        return self._location
    
    @property
    def language(self) -> str:
        return self._language
    
    @property
    def output_format(self) -> OutputEnum:
        return self._output_format
    
    @property
    def persist(self) -> bool:
        return self._persist
    
    @property
    def icons(self) -> str:
        return self._icons
    
    def __str__(self):
        return f"Params(location={self.location}, language={self.language}, output_format={self.output_format}, persist={self.persist}, icons={self.icons})"
    