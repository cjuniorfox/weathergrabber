from weathergrabber.domain.entities.moon_phase import MoonPhase
from weathergrabber.domain.entities.moon_phase_enum import MoonPhaseEnum
from weathergrabber.domain.adapter.mappers.moon_phase_mapper import moon_phase_to_dict

def test_moon_phase_to_dict():
    mp = MoonPhase(MoonPhaseEnum.PHASE_15, "Full Moon", "Moon Phase")
    d = moon_phase_to_dict(mp)
    assert d["icon"] == MoonPhaseEnum.PHASE_15.name
    assert d["phase"] == "Full Moon"
    assert d["label"] == "Moon Phase"
    assert isinstance(d, dict)
