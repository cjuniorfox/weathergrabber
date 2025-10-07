import random
import weathergrabber
import os

cities_file = os.path.join(os.path.dirname(__file__), "cities.txt")

errors = []

with open(cities_file) as f:
    cities = [line.strip() for line in f if line.strip()]

languages = [
    "en-US", "pt-BR", "fr-FR", "es-ES", "de-DE",
    "it-IT", "ru-RU", "ja-JP", "zh-CN", "ar-SA"
]

for city, lang in zip(random.sample(cities, 25), random.sample(languages, 10)):
    print(f"Querying {city!r} in {lang!r}...")
    try:
        weathergrabber.main(
            log_level="DEBUG",
            location_name=city,
            location_id="",
            lang=lang,
            output="console",
            keep_open=False,
            icons="emoji"
        )
    except Exception as e:
        errors.append(f"Failed for {city!r} in {lang!r}: {e}")
        print(f"Failed for {city!r} in {lang!r}: {e}")

if errors:
    print("Errors occurred:")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)
