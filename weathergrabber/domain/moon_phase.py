from weathergrabber.domain.moon_phase_enum import MoonPhaseEnum

class MoonPhase:
    def __init__(self, icon: MoonPhaseEnum, phase: str):
        self._icon = icon
        self._phase = phase

    @property
    def icon(self) -> MoonPhaseEnum:
        return self._icon
    
    @property
    def phase(self) -> str:
        return self._phase
    
    def __repr__(self) -> str:
        return f"MoonPhase(icon={self.icon}, phase={self.phase!r})"