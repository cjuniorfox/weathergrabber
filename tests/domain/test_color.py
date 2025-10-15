import pytest
from weathergrabber.domain.color import Color

def test_color_from_string_valid():
    color = Color.from_string("#FF00AA")
    assert color.red == 255
    assert color.green == 0
    assert color.blue == 170
    assert color.hex == "FF00AA"
    assert color.rgb == "rgb(255, 0, 170)"
    assert str(color) == "FF00AA"
    assert repr(color) == "Color(red='255', green='0', blue='170')"

def test_color_from_string_lowercase():
    color = Color.from_string("#ff00aa")
    assert color.red == 255
    assert color.green == 0
    assert color.blue == 170
    assert color.hex == "FF00AA"

def test_color_from_string_invalid():
    with pytest.raises(ValueError):
        Color.from_string("not-a-color")

def test_color_init_with_ints():
    color = Color(10, 20, 30)
    assert color.red == 10
    assert color.green == 20
    assert color.blue == 30
    assert color.hex == "0A141E"

def test_color_init_with_hex_strings():
    color = Color("0A", "14", "1E")
    assert color.red == 10
    assert color.green == 20
    assert color.blue == 30
    assert color.hex == "0A141E"
