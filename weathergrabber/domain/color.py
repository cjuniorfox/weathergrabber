import re

class Color:
    
    def __init__(self, red: str, green: str, blue: str):
        self._red = red
        self._green = green
        self._blue = blue

    @property
    def red(self):
        return self._red
    
    @property
    def green(self):
        return self._green
    
    @property
    def blue(self):
        return self._blue
    
    @classmethod
    def from_string(cls,string_value: str) -> "Color":

        color_pattern = r"#([0-9A-Fa-f]{6})"        
        
        match = re.search(color_pattern, string_value)
        color = f"#{match.group(1)}"
        hex_color = color.lstrip('#')
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
        
        return cls(r, g, b)
    
    def __str__(self):
        return f"#{self.red}{self.green}{self.blue}"
    
    def __repr__(self):
        return f"Color(red='{self.red}', green='{self.green}', blue='{self.blue}')"