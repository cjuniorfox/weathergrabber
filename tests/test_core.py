import pytest
from unittest.mock import patch, MagicMock
import logging

@patch('weathergrabber.core.WeatherGrabberApplication')
def test_main_invokes_application(mock_app):
    from weathergrabber.core import main
    params = {
        'log_level': 'info',
        'location_name': 'London',
        'location_id': '123',
        'lang': 'en-US',
        'output': 'console',
        'keep_open': False,
        'icons': 'emoji',
        'force_cache': False,
        'cache_statistics': False,
    }
    main(**params)
    mock_app.assert_called_once()
    # Check Params object
    args, kwargs = mock_app.call_args
    assert hasattr(args[0], 'location')
    assert args[0].location.search_name == 'London'
    assert args[0].location.id == '123'
    assert args[0].language == 'en-US'
    assert args[0].output_format.name.lower() == 'console'
    assert args[0].keep_open is False
    assert args[0].icons.name.lower() == 'emoji'
    assert args[0].force_cache is False
    assert args[0].cache_statistics is False
    
@patch('weathergrabber.core.WeatherGrabberApplication')
def test_main_sets_log_level(mock_app):
    from weathergrabber.core import main
    main(
        log_level='debug',
        location_name='Paris',
        location_id='456',
        lang='fr-FR',
        output='json',
        keep_open=True,
        icons='fa',
        force_cache=False,
        cache_statistics=False,
    )
    assert logging.getLogger().level == logging.DEBUG
