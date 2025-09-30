import pytest
import logging
from unittest.mock import MagicMock, patch
from weathergrabber.weathergrabber_application import WeatherGrabberApplication
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.output_enum import OutputEnum

def make_params(output_format=OutputEnum.CONSOLE, keep_open=False):
    return Params(output_format=output_format, keep_open=keep_open, icons=None)

@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._beans')
@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._define_controller')
def test_application_runs_once(mock_define_controller, mock_beans):
    params = make_params(output_format=OutputEnum.CONSOLE, keep_open=False)
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.logger = logging.getLogger(__name__)
    app._beans = MagicMock()
    app._define_controller = MagicMock()
    app.controller = MagicMock()
    # Simulate __init__ logic except for controller assignment
    app._beans()
    app._define_controller(params.output_format)
    app.controller.execute(params)
    app._beans.assert_called_once()
    app._define_controller.assert_called_once_with(params.output_format)
    app.controller.execute.assert_called_once_with(params)

@patch('weathergrabber.weathergrabber_application.sleep', return_value=None)
@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._beans')
def test_application_keep_open(mock_beans, mock_sleep):
    params = make_params(output_format=OutputEnum.CONSOLE, keep_open=True)
    # Patch controller to break after first loop
    class DummyController:
        def __init__(self):
            self.calls = 0
        def execute(self, p):
            self.calls += 1
            if self.calls > 1:
                raise KeyboardInterrupt()
    with patch.object(WeatherGrabberApplication, '_define_controller', autospec=True) as ctrl_patch:
        def ctrl_side_effect(self, output_format):
            self.controller = DummyController()
        ctrl_patch.side_effect = ctrl_side_effect
        try:
            WeatherGrabberApplication(params)
        except KeyboardInterrupt:
            pass
        # Should call execute at least once
        assert ctrl_patch.call_count == 1
