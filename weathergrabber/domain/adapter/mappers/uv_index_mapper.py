from weathergrabber.domain.entities.uv_index import UVIndex

def uv_index_to_dict(uv: UVIndex) -> dict:
    return {
        "string_value": uv.string_value,
        "index": uv.index,
        "of": uv.of,
        "label": uv.label,
    }

def dict_to_uv_index(data: dict) -> UVIndex:
    return UVIndex(
        string_value=data.get("string_value"),
        index=data.get("index"),
        of=data.get("of"),
        label=data.get("label"),
    )
