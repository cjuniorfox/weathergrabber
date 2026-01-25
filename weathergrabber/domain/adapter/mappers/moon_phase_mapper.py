from weathergrabber.domain.entities.moon_phase import MoonPhase
from weathergrabber.domain.entities.moon_phase_enum import MoonPhaseEnum

def moon_phase_to_dict(mp: MoonPhase) -> dict:
    return {
        "icon": mp.icon.name if mp.icon else None,
        "phase": mp.phase,
        "label": mp.label,
    }

def dict_to_moon_phase(data: dict) -> MoonPhase:
    return MoonPhase(
        icon=MoonPhaseEnum.from_name(data["icon"]) if data.get("icon") else None,
        phase=data.get("phase"),
        label=data.get("label"),
    )
