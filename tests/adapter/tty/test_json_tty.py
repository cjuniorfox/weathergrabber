import pytest
import logging
from unittest.mock import MagicMock, patch
from weathergrabber.adapter.tty.json_tty import JsonTTY
from weathergrabber.domain.adapter.params import Params

@pytest.fixture
def mock_use_case():
    mock = MagicMock()
    mock.execute.return_value = MagicMock()
    return mock

@pytest.fixture
def mock_forecast_to_dict():
    with patch('weathergrabber.adapter.tty.json_tty.forecast_to_dict') as mock:
        mock.return_value = {"mocked": "forecast"}
        yield mock

@patch('builtins.print')
def test_execute_prints_json(mock_print, mock_use_case, mock_forecast_to_dict):
    params = MagicMock(spec=Params)
    tty = JsonTTY(mock_use_case)
    tty.execute(params)
    # Check that forecast_to_dict was called
    mock_forecast_to_dict.assert_called()
    # Check that print was called with the expected JSON string
    printed = mock_print.call_args[0][0]
    assert 'mocked' in printed
    assert 'forecast' in printed
