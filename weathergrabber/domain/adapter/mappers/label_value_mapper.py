from weathergrabber.domain.entities.label_value import LabelValue

def label_value_to_dict(lv: LabelValue) -> dict:
    return {
        "label": lv.label,
        "value": lv.value,
    }

def dict_to_label_value(data: dict) -> LabelValue:
    return LabelValue(
        label=data["label"],
        value=data["value"],
    )
