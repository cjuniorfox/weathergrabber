import pytest
from unittest.mock import patch, MagicMock
import json
from weathergrabber.domain.adapter.params import Params
from weathergrabber.adapter.tty.json_tty import JsonTTY

@patch('weathergrabber.adapter.tty.json_tty.forecast_to_dict')
def test_execute_json_output(mock_forecast_to_dict, capsys):
    mock_use_case = MagicMock()
    mock_forecast = MagicMock()
    mock_use_case.execute.return_value = mock_forecast
    mock_forecast_to_dict.return_value = {'mock_key': 'mock_value'}

    params = MagicMock(spec=Params)
    json_tty = JsonTTY(mock_use_case)

    json_tty.execute(params)

    mock_use_case.execute.assert_called_once_with(params)
    captured = capsys.readouterr()
    try:
        output = json.loads(captured.out)
        assert isinstance(output, dict)  # Assuming forecast_to_dict returns a dictionary
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON")