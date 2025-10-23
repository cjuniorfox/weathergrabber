import pytest
from weathergrabber.domain.moon_phase_enum import MoonPhaseEnum

def test_enum_members():
    assert MoonPhaseEnum.PHASE_0.name == "phase-0"
    assert MoonPhaseEnum.PHASE_15.emoji_icon == "🌕"
    assert MoonPhaseEnum.PHASE_25.fa_icon == "\uf186"

def test_from_name_found():
    phase = MoonPhaseEnum.from_name("phase-15")
    assert phase == MoonPhaseEnum.PHASE_15
    assert phase.emoji_icon == "🌕"

def test_from_name_not_found():
    with pytest.raises(ValueError, match='WeatherIconEnum: No icon found for name "not-a-phase"'):
        MoonPhaseEnum.from_name("not-a-phase")

def test_enum_repr_and_properties():
    phase = MoonPhaseEnum.PHASE_8
    assert phase.name == "phase-8"
    assert phase.fa_icon == "\uf186"
    assert phase.emoji_icon == "🌔"
