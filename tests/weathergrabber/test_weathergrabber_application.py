import pytest
from unittest.mock import patch, MagicMock
from weathergrabber.weathergrabber_application import WeatherGrabberApplication
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.output_enum import OutputEnum

@pytest.fixture(params=[OutputEnum.CONSOLE, OutputEnum.JSON, OutputEnum.WAYBAR])
def params(request):
    p = MagicMock(spec=Params)
    p.output_format = request.param
    p.keep_open = False
    return p

@pytest.fixture
def params_keep_open():
    p = MagicMock(spec=Params)
    p.output_format = OutputEnum.JSON
    p.keep_open = True
    return p

@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._beans')
@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._define_controller')
def test_init_calls_beans_and_define_controller(mock_define, mock_beans, params):
    with patch.object(WeatherGrabberApplication, 'controller', create=True):
        WeatherGrabberApplication(params)
    mock_beans.assert_called_once()
    mock_define.assert_called_once_with(params.output_format)

@patch('weathergrabber.weathergrabber_application.sleep', side_effect=Exception("break loop"))
@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._beans')
@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._define_controller')
def test_init_keep_open(mock_define, mock_beans, mock_sleep, params_keep_open):
    # Patch controller to raise after first execute to break the loop
    with patch.object(WeatherGrabberApplication, 'controller', create=True) as mock_controller:
        mock_controller.execute = MagicMock(side_effect=None)
        with pytest.raises(Exception):
            WeatherGrabberApplication(params_keep_open)
        mock_controller.execute.assert_called_once_with(params_keep_open)
        mock_sleep.assert_called()

@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._beans')
def test_define_controller_console(mock_beans):
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.use_case = MagicMock()
    app.logger = MagicMock()
    app._define_controller(OutputEnum.CONSOLE)
    assert hasattr(app, 'controller')
    assert app.controller.__class__.__name__ == 'ConsoleTTY'
    

@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._beans')
def test_define_controller_json(mock_beans):
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.use_case = MagicMock()
    app.logger = MagicMock()
    app._define_controller(OutputEnum.JSON)
    assert hasattr(app, 'controller')
    assert app.controller.__class__.__name__ == 'JsonTTY'

@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._beans')
def test_define_controller_waybar(mock_beans):
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.use_case = MagicMock()
    app.logger = MagicMock()
    app._define_controller(OutputEnum.WAYBAR)
    assert hasattr(app, 'controller')
    assert app.controller.__class__.__name__ == 'WaybarTTY'

@patch('weathergrabber.weathergrabber_application.WeatherGrabberApplication._beans')
def test_define_controller_invalid(mock_beans):
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.use_case = MagicMock()
    app.logger = MagicMock()
    with pytest.raises(ValueError):
        app._define_controller('INVALID')

def test_beans_creates_all_services():
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.logger = None  # Not needed for this test
    app._beans()
    assert hasattr(app, 'weather_search_api')
    assert hasattr(app, 'weather_api')
    assert hasattr(app, 'search_location_service')
    assert hasattr(app, 'read_weather_service')
    assert hasattr(app, 'extract_current_conditions_service')
    assert hasattr(app, 'extract_today_details_service')
    assert hasattr(app, 'extract_aqi_service')
    assert hasattr(app, 'extract_health_activities_service')
    assert hasattr(app, 'extract_hourly_forecast_service')
    assert hasattr(app, 'extract_hourly_forecast_oldstyle_service')
    assert hasattr(app, 'extract_daily_forecast_service')
    assert hasattr(app, 'extract_daily_forecast_oldstyle_service')
    assert hasattr(app, 'use_case')
