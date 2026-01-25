from weathergrabber.domain.entities.timestamp import Timestamp

def timestamp_to_dict(ts: Timestamp) -> dict:
    return {
        "time": ts.time,
        "gmt": ts.gmt,
        "text": ts.text,
    }

def dict_to_timestamp(data: dict) -> Timestamp:
    return Timestamp(
        time=data.get("time"),
        gmt=data.get("gmt"),
        text=data.get("text"),
    )
