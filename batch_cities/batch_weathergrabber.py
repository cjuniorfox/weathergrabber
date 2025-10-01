import sys
from weathergrabber.core import main

# Adjust these as needed
default_log_level = "WARNING"
default_location_id = ""
default_lang = "en-US"
default_output = "console"
default_keep_open = False
default_icons = "emoji"

cities_file = "cities.txt"

with open(cities_file, "r", encoding="utf-8") as f:
    cities = [line.strip() for line in f if line.strip()]

errors = []

for city in cities:
    try:
        main(
            log_level=default_log_level,
            location_name=city,
            location_id=default_location_id,
            lang=default_lang,
            output=default_output,
            keep_open=default_keep_open,
            icons=default_icons
        )
    except Exception as e:
        errors.append((city, str(e)))
        print(f"Error processing city '{city}': {e}", file=sys.stderr)
print(errors)
