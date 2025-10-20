class AQIResponse:
    def __init__(
            self, 
            color: "AQIResponse.Color", 
            acronym: str, 
            category: str, 
            value: str
        ):
        self.color = color
        self.acronym = acronym
        self.category = category
        self.value = value

    def __str__(self):
        return f"{self.acronym} \033[38;2;{self.color}m{self.category}\033[0m {self.value}"

    class Color:
        def __init__(self, red: str, green: str, blue: str):
            self.red = red
            self.green = green
            self.blue = blue

        def __str__(self):
            return f"#{self.red};{self.green};{self.blue}"


        def __str__(self):
            return f"{self.acronym} \033[38;2;{self.color}m{self.category}\033[0m {self.value}"
        
        class Color:
            def __init__(self, red: str, green: str, blue: str):
                self.red = red
                self.green = green
                self.blue = blue

            def __str__(self):
                return f"#{self.red};{self.green};{self.blue}"