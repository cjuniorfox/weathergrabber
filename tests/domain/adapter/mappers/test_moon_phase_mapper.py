from weathergrabber.domain.entities.moon_phase import MoonPhase
from weathergrabber.domain.entities.moon_phase_enum import MoonPhaseEnum
from weathergrabber.domain.adapter.mappers.moon_phase_mapper import moon_phase_to_dict, dict_to_moon_phase

def test_moon_phase_to_dict():
    mp = MoonPhase(MoonPhaseEnum.PHASE_15, "Full Moon", "Moon Phase")
    d = moon_phase_to_dict(mp)
    assert d["icon"] == MoonPhaseEnum.PHASE_15.name
    assert d["phase"] == "Full Moon"
    assert d["label"] == "Moon Phase"
    assert isinstance(d, dict)


def test_dict_to_moon_phase():
    data = {
        "icon": "phase-15",
        "phase": "Full Moon",
        "label": "Moon Phase"
    }
    mp = dict_to_moon_phase(data)
    assert isinstance(mp, MoonPhase)
    assert mp.icon == MoonPhaseEnum.PHASE_15
    assert mp.phase == "Full Moon"
    assert mp.label == "Moon Phase"


def test_dict_to_moon_phase_none_icon():
    data = {
        "icon": None,
        "phase": "Waning Crescent",
        "label": "Moon Phase"
    }
    mp = dict_to_moon_phase(data)
    assert mp.icon is None
    assert mp.phase == "Waning Crescent"
    assert mp.label == "Moon Phase"


def test_dict_to_moon_phase_missing_keys():
    data = {
        "icon": "phase-8",
        "phase": "First Quarter"
    }
    mp = dict_to_moon_phase(data)
    assert mp.icon == MoonPhaseEnum.PHASE_8
    assert mp.phase == "First Quarter"
    assert mp.label is None


def test_dict_to_moon_phase_roundtrip():
    original = MoonPhase(MoonPhaseEnum.PHASE_0, "New Moon", "New")
    data = moon_phase_to_dict(original)
    reconstructed = dict_to_moon_phase(data)
    assert reconstructed.icon == original.icon
    assert reconstructed.phase == original.phase
    assert reconstructed.label == original.label
