import random
import weathergrabber
import os
import argparse
from itertools import cycle

cities_file = os.path.join(os.path.dirname(__file__), "cities.txt")

errors = []

with open(cities_file) as f:
    cities = [line.strip() for line in f if line.strip()]

parser = argparse.ArgumentParser(description="Test random cities in various languages")
parser.add_argument(
    "--languages",
    type=str,
    help="Comma-separated list of languages (e.g., 'en-US,pt-BR,fr-FR')",
)
parser.add_argument(
    "--cities-count",
    type=int,
    default=25,
    help="Number of random cities to test (default: 25)",
)
args = parser.parse_args()

languages = (
    [lang.strip() for lang in args.languages.split(",") if lang.strip()] if args.languages else [
        "en-US", "pt-BR", "fr-FR", "es-ES", "de-DE",
        "it-IT", "ru-RU", "ja-JP", "zh-CN", "ar-SA"
    ]
)

# Determine how many cities to sample and cycle languages if needed
cities_to_test = random.sample(cities, min(len(cities), args.cities_count))

for city, lang in zip(cities_to_test, cycle(languages)):
    print(f"Querying {city!r} in {lang!r}...")
    try:
        weathergrabber.main(
            log_level="DEBUG",
            location_name=city,
            location_id="",
            lang=lang,
            output="console",
            keep_open=False,
            icons="emoji",
            force_cache=False,
            cache_statistics=False,
        )
    except Exception as e:
        errors.append(f"Failed for {city!r} in {lang!r}: {e}")
        print(f"Failed for {city!r} in {lang!r}: {e}")

if errors:
    print("Errors occurred:")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)
