from weathergrabber.usecase.use_case import UseCase
from weathergrabber.domain.adapter.params import Params
import logging

class WaybarTTY:

    def __init__(self, use_case: UseCase):
        self.logger = logging.getLogger(__name__)
        self.use_case = use_case
        pass

    def execute(self, params: Params) -> None:
        self.logger.info("Executing Waybar output")
        self.use_case.execute(params)
        self.logger.info("Waybar output executed")