import random
import weathergrabber
import os

cities_file = os.path.join(os.path.dirname(__file__), "cities.txt")

with open(cities_file) as f:
    cities = [line.strip() for line in f if line.strip()]

languages = [
    "en-US", "pt-BR", "fr-FR", "es-ES", "de-DE",
    "it-IT", "ru-RU", "ja-JP", "zh-CN", "ar-SA"
]

for city, lang in zip(random.sample(cities, 5), random.sample(languages, 5)):
    print(f"Querying {city!r} in {lang!r}...")
    try:
        weathergrabber.main(
            log_level="WARNING",
            location_name=city,
            location_id="",
            lang=lang,
            output="json",
            keep_open=False,
            icons="emoji"
        )
    except Exception as e:
        print(f"Failed for {city!r} in {lang!r}: {e}")
        raise SystemExit(1)
