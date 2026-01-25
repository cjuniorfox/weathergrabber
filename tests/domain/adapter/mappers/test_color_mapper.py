from weathergrabber.domain.entities.color import Color
from weathergrabber.domain.adapter.mappers.color_mapper import color_to_dict, dict_to_color

def test_color_to_dict():
    color = Color(255, 0, 170)
    d = color_to_dict(color)
    assert d["red"] == 255
    assert d["green"] == 0
    assert d["blue"] == 170
    assert d["hex"] == "FF00AA"
    assert d["rgb"] == "rgb(255, 0, 170)"


def test_dict_to_color():
    data = {
        "red": 255,
        "green": 0,
        "blue": 170,
        "hex": "FF00AA",
        "rgb": "rgb(255, 0, 170)"
    }
    color = dict_to_color(data)
    assert isinstance(color, Color)
    assert color.red == 255
    assert color.green == 0
    assert color.blue == 170
    assert color.hex == "FF00AA"
    assert color.rgb == "rgb(255, 0, 170)"


def test_dict_to_color_with_minimum_data():
    data = {
        "red": 128,
        "green": 64,
        "blue": 32
    }
    color = dict_to_color(data)
    assert color.red == 128
    assert color.green == 64
    assert color.blue == 32
    assert color.hex == "804020"


def test_dict_to_color_black():
    data = {
        "red": 0,
        "green": 0,
        "blue": 0,
        "hex": "000000",
        "rgb": "rgb(0, 0, 0)"
    }
    color = dict_to_color(data)
    assert color.red == 0
    assert color.green == 0
    assert color.blue == 0
    assert color.hex == "000000"


def test_dict_to_color_white():
    data = {
        "red": 255,
        "green": 255,
        "blue": 255,
        "hex": "FFFFFF",
        "rgb": "rgb(255, 255, 255)"
    }
    color = dict_to_color(data)
    assert color.red == 255
    assert color.green == 255
    assert color.blue == 255
    assert color.hex == "FFFFFF"


def test_dict_to_color_roundtrip():
    original_color = Color(100, 150, 200)
    data = color_to_dict(original_color)
    reconstructed_color = dict_to_color(data)
    assert reconstructed_color.red == original_color.red
    assert reconstructed_color.green == original_color.green
    assert reconstructed_color.blue == original_color.blue
    assert reconstructed_color.hex == original_color.hex
