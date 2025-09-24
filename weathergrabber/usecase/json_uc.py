from weathergrabber.domain.adapter.params import Params

class JsonUC:
    def __init__(self):
        pass

    def execute(self, params: Params) -> None:
        print(f"Executing JSON use case with output format JSON")