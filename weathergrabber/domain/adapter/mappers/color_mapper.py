from weathergrabber.domain.entities.color import Color

def color_to_dict(color: Color) -> dict:
    return {
        "red": color.red,
        "green": color.green,
        "blue": color.blue,
        "hex": color.hex,
        "rgb": color.rgb,
    }

def dict_to_color(data: dict) -> Color:
    return Color(
        red=data["red"],
        green=data["green"],
        blue=data["blue"],
    )
