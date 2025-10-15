from weathergrabber.domain.color import Color
from weathergrabber.domain.adapter.mapper.color_mapper import color_to_dict

def test_color_to_dict():
    color = Color(255, 0, 170)
    d = color_to_dict(color)
    assert d["red"] == 255
    assert d["green"] == 0
    assert d["blue"] == 170
    assert d["hex"] == "FF00AA"
    assert d["rgb"] == "rgb(255, 0, 170)"
