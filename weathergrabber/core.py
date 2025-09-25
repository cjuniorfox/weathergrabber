import logging
from weathergrabber.weathergrabber_application import WeatherGrabberApplication
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.output_enum import OutputEnum

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

def main(log_level: str, location_name: str, location_id: str, lang: str, output: str, persist: bool, icons: str):
    logging.getLogger().setLevel(log_level.upper())

    logging.info(f"Log level set to {log_level}")
    logging.info(f"Location name: {location_name}")
    logging.info(f"Location id: {location_id}")
    logging.info(f"Language: {lang}")
    logging.info(f"Output: {output}")
    logging.info(f"Persist: {persist}")
    logging.info(f"Icons: {icons}")

    params = Params(
        location=Params.Location(name=location_name, id=location_id),
        language=lang if lang else "en-US",
        output_format= OutputEnum(output),
        persist=persist,
        icons=icons
    )

    app = WeatherGrabberApplication(params)