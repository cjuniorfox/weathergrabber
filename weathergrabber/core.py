import logging
from weathergrabber.application.weathergrabber_application import WeatherGrabberApplication
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.output_enum import OutputEnum
from weathergrabber.domain.adapter.icon_enum import IconEnum

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

def main(log_level: str, location_name: str, location_id: str, lang: str, output: str, keep_open: bool, icons: str, force_cache: bool, cache_statistics: bool):
    logging.getLogger().setLevel(log_level.upper())

    logging.info(f"Log level set to {log_level}")
    logging.info(f"Location name: {location_name}")
    logging.info(f"Location id: {location_id}")
    logging.info(f"Language: {lang}")
    logging.info(f"Output: {output}")
    logging.info(f"Keep open: {keep_open}")
    logging.info(f"Icons: {icons}")
    logging.info(f"Force cache: {force_cache}")
    logging.info(f"Cache statistics: {cache_statistics}")

    params = Params(
        location=Params.Location(search_name=location_name, id=location_id),
        language=lang if lang else "en-US",
        output_format= OutputEnum(output),
        keep_open=keep_open,
        icons=IconEnum(icons),
        force_cache=force_cache,
        cache_statistics=cache_statistics,
    )

    app = WeatherGrabberApplication(params)