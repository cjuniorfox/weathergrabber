import pytest
from unittest.mock import patch, MagicMock
from weathergrabber.application.weathergrabber_application import WeatherGrabberApplication
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.adapter.output_enum import OutputEnum

@pytest.fixture(params=[OutputEnum.CONSOLE, OutputEnum.JSON, OutputEnum.WAYBAR])
def params(request):
    p = MagicMock(spec=Params)
    p.output_format = request.param
    p.keep_open = False
    p.cache_statistics = False
    return p

@pytest.fixture
def params_keep_open():
    p = MagicMock(spec=Params)
    p.output_format = OutputEnum.JSON
    p.keep_open = True
    p.force_cache = False
    p.cache_statistics = False
    return p

@pytest.fixture
def params_statistics():
    p = MagicMock(spec=Params)
    p.output_format = OutputEnum.JSON
    p.keep_open = False
    p.force_cache = False
    p.cache_statistics = True
    return p

@patch('weathergrabber.application.weathergrabber_application.WeatherGrabberApplication._beans')
@patch('weathergrabber.application.weathergrabber_application.WeatherGrabberApplication._define_controller')
def test_init_calls_beans_and_define_controller(mock_define, mock_beans, params):
    with patch.object(WeatherGrabberApplication, 'controller', create=True):
        WeatherGrabberApplication(params)
    mock_beans.assert_called_once()
    mock_define.assert_called_once_with(params)

@patch('weathergrabber.application.weathergrabber_application.sleep', side_effect=Exception("break loop"))
@patch('weathergrabber.application.weathergrabber_application.WeatherGrabberApplication._beans')
@patch('weathergrabber.application.weathergrabber_application.WeatherGrabberApplication._define_controller')
def test_init_keep_open(mock_define, mock_beans, mock_sleep, params_keep_open):
    # Patch controller to raise after first execute to break the loop
    with patch.object(WeatherGrabberApplication, 'controller', create=True) as mock_controller:
        mock_controller.execute = MagicMock(side_effect=None)
        with pytest.raises(Exception):
            WeatherGrabberApplication(params_keep_open)
        mock_controller.execute.assert_called_once_with(params_keep_open)
        mock_sleep.assert_called()

@patch('weathergrabber.application.weathergrabber_application.WeatherGrabberApplication._beans')
def test_define_controller_console(mock_beans):
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.weather_forecast_uc = MagicMock()
    app.logger = MagicMock()
    p = MagicMock(spec=Params)
    p.output_format = OutputEnum.CONSOLE
    p.cache_statistics = False
    app._define_controller(p)
    assert hasattr(app, 'controller')
    assert app.controller.__class__.__name__ == 'ConsoleTTY'
    

@patch('weathergrabber.application.weathergrabber_application.WeatherGrabberApplication._beans')
def test_define_controller_json(mock_beans):
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.weather_forecast_uc = MagicMock()
    app.logger = MagicMock()
    p = MagicMock(spec=Params)
    p.output_format = OutputEnum.JSON
    p.cache_statistics = False
    app._define_controller(p)
    assert hasattr(app, 'controller')
    assert app.controller.__class__.__name__ == 'JsonTTY'

@patch('weathergrabber.application.weathergrabber_application.WeatherGrabberApplication._beans')
def test_define_controller_waybar(mock_beans):
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.weather_forecast_uc = MagicMock()
    app.logger = MagicMock()
    p = MagicMock(spec=Params)
    p.output_format = OutputEnum.WAYBAR
    p.cache_statistics = False
    app._define_controller(p)
    assert hasattr(app, 'controller')
    assert app.controller.__class__.__name__ == 'WaybarTTY'
    
@patch('weathergrabber.application.weathergrabber_application.WeatherGrabberApplication._beans')
def test_define_controller_statistics(mock_beans):
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.weather_forecast_uc = MagicMock()
    app.statistics_uc = MagicMock()
    app.logger = MagicMock()
    p = MagicMock(spec=Params)
    p.output_format = OutputEnum.JSON
    p.cache_statistics = True
    app._define_controller(p)
    assert hasattr(app, 'controller')
    assert app.controller.__class__.__name__ == 'StatisticsTTY'

@patch('weathergrabber.application.weathergrabber_application.WeatherGrabberApplication._beans')
def test_define_controller_invalid(mock_beans):
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.weather_forecast_uc = MagicMock()
    app.logger = MagicMock()
    p = MagicMock(spec=Params)
    p.output_format = 'INVALID'
    p.cache_statistics = False
    with pytest.raises(ValueError):
        app._define_controller(p)

def test_beans_creates_all_services():
    app = WeatherGrabberApplication.__new__(WeatherGrabberApplication)
    app.logger = None  # Not needed for this test
    app._beans()
    assert hasattr(app, 'weather_search_api')
    assert hasattr(app, 'weather_api')
    assert hasattr(app, 'forecast_repository')
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
    assert hasattr(app, 'retrieve_forecast_from_cache_service')
    assert hasattr(app, 'save_forecast_to_cache_service')
    assert hasattr(app, 'retrieve_statistics_service')
    assert hasattr(app, 'weather_forecast_uc')
    assert hasattr(app, 'statistics_uc')