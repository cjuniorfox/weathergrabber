import json
from unittest.mock import MagicMock

import pytest

from weathergrabber.adapter.tty.statistics_tty import StatisticsTTY
from weathergrabber.domain.adapter.output_enum import OutputEnum
from weathergrabber.domain.adapter.params import Params
from weathergrabber.domain.entities.statistics import Statistics


def test_statistics_tty_execute_tty_output(capsys):
    stats_uc = MagicMock()
    stats_uc.execute.return_value = Statistics(
        total_forecasts=5,
        unique_locations=3,
        unique_search_names=2,
        database_path="/tmp/weather.db",
    )
    params = MagicMock(spec=Params)
    params.output_format = OutputEnum.CONSOLE

    tty = StatisticsTTY(stats_uc)
    tty.execute(params)

    stats_uc.execute.assert_called_once_with(params)
    output = capsys.readouterr().out
    assert "WeatherGrabber Statistics" in output
    assert "Total Forecasts: 5" in output
    assert "Unique Locations: 3" in output
    assert "Unique Search Names: 2" in output
    assert "Database Path: /tmp/weather.db" in output


def test_statistics_tty_execute_json_output(capsys):
    stats_uc = MagicMock()
    stats_uc.execute.return_value = Statistics(
        total_forecasts=7,
        unique_locations=4,
        unique_search_names=3,
        database_path="/var/data/weather.db",
        error="boom",
    )
    params = MagicMock(spec=Params)
    params.output_format = OutputEnum.JSON

    tty = StatisticsTTY(stats_uc)
    tty.execute(params)

    stats_uc.execute.assert_called_once_with(params)
    output = capsys.readouterr().out.strip()
    payload = json.loads(output)
    assert payload == {
        "total_forecasts": 7,
        "unique_locations": 4,
        "unique_search_names": 3,
        "database_path": "/var/data/weather.db",
        "error": "boom",
    }
