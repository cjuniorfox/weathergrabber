# Weather Forecast CLI Script

## Overview

This script fetches and parses weather forecast data from Weather.com and formats it for display in various environments such as a terminal or Waybar, a status bar tool. It leverages `pyquery` for HTML parsing and provides detailed weather information, including hourly and daily predictions, formatted for ease of use.

### Waybar widget

![Weather widget on Waybar](image.png)

### Terminal Console

![Weather widget on terminal console](image-1.png)

## Features

- Retrieves current weather and forecasts for a specified location.
- Displays weather data in different formats:
  - **Console output**: Richly formatted weather data with icons.
  - **Waybar JSON**: For integration with Waybar.
- Supports multiple languages for Weather.com data.
- **Offline support**: Automatically retrieves cached weather data when internet connection is unavailable.
- **Cache management**: SQLite-based caching system for storing weather forecasts and enabling offline access.
- Includes data such as:
  - Current temperature and "feels-like" temperature.
  - Wind speed, humidity, visibility, and air quality.
  - Hourly and daily forecasts with icons and precipitation chances.

## Requirements

Requires Python 3 or newer.

Install the package and all dependencies with:

```sh
pip install .
```

Or, for development (editable install with dev dependencies):

```sh
pip install -e .[dev]
```

### Output Formats

#### Console Output

The script displays a formatted weather summary, including:

- Current weather status.
- Temperature (current, max/min).
- Wind, humidity, visibility, and air quality.
- Hourly and daily forecasts with icons.

#### Waybar JSON

The JSON includes:

- `text`: Current weather icon and temperature.
- `alt`: Weather status.
- `tooltip`: Detailed weather information.
- `class`: Status code for further customization.

### JSON General output

Here the following [JSON Schema](schema.json) for this output.

The key values for this json is:

- `temperature`: An object containing the temperature information with the following fields:
  - `current`: The current temperature.
  - `feel`: The temperature feel
  - `max` : The maximum temperature
  - `min` : The minimum temperature

There's also other fields like `hourly_predictions` and `daily_predictions` containing lists of predictions informations. More defaults on [JSON Schema](schema.json).

### Integration with Waybar

To integrate the script with Waybar:

1. Add a custom script module in Waybar's configuration:

   ```json
   {
       "modules-left": ["custom/weather"],
       "custom/weather": {
           "exec": "weathergrabber --output waybar",
           "interval": 600
       }
   }
   ```

2. Reload Waybar to apply the changes.

## Error Handling

- Validates `weather_id` and `lang` inputs.
- Handles HTTP errors gracefully, including 404 errors for invalid locations.

## CI & Test Coverage

![Test Status](https://github.com/cjuniorfox/weathergrabber/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/cjuniorfox/weathergrabber/graph/badge.svg?token=SC5CRMC3YW)](https://codecov.io/gh/cjuniorfox/weathergrabber)

The test suite is run automatically on every push and pull request using GitHub Actions. Coverage results are uploaded to Codecov and displayed above.

To run tests and check coverage locally:

```sh
pytest --cov=weathergrabber --cov-report=term
```

## License

This script is open-source and available under the MIT License.

## CLI Usage

You can run the CLI as an installed command:

```sh
weathergrabber [location_name] [options]
```

Or as a Python module:

```sh
python -m weathergrabber [location_name] [options]
```

### Importing as a Python module

You can also use the main API or CLI entry point in your own Python code:

```python
import weathergrabber

# Call the main API
weathergrabber.main(log_level="INFO", location_name="London", location_id="", lang="en-GB", output="console", keep_open=False, icons="emoji")

# Or run the CLI programmatically
weathergrabber.main_cli()
```

### Arguments

- `location_name` (positional, optional): City name, zip code, etc. If not provided, you can use `--location-id` or the `WEATHER_LOCATION_ID` environment variable.

### Options

- `--location-id`, `-l`     : 64-character-hex code for location (from Weather.com)
- `--lang`, `-L`            : Language (e.g., `pt-BR`, `fr-FR`). Defaults to system locale if not set.
- `--output`, `-o`          : Output format. One of `console`, `json`, `waybar`, or `statistics`. Default: `console`.
- `--keep-open`, `-k`       : Keep open and refresh every 5 minutes (only makes sense for `console` output).
- `--force-cache`           : Retrieve weather data from cache regardless of internet connection availability. Useful for offline mode.
- `--cache-statistics`      : Display cache database statistics including total forecasts, unique locations, unique search names, and database file path.
- `--icons`, `-i`           : Icon set. `fa` for Font-Awesome, `emoji` for emoji icons. Default: `emoji`.
- `--log`                   : Set logging level. One of `debug`, `info`, `warning`, `error`, `critical`. Default: `critical`.

### Environment Variables

- `LANG`                  : Used as default language if `--lang` is not set.
- `WEATHER_LOCATION_ID`   : Used as default location if neither `location_name` nor `--location-id` is set.

## Cache & Offline Support

The script maintains a SQLite cache database for storing weather forecasts. This enables several key features:

- **Automatic offline fallback**: When internet connection is unavailable, the script automatically retrieves the most recent cached weather data for the requested location.
- **Forced cache retrieval**: Use `--force-cache` to retrieve data exclusively from the cache, regardless of internet availability. This is useful for offline scenarios or reducing API calls.
- **Cache statistics**: Use `--cache-statistics` to display information about the cache database, including:
  - Total number of cached forecasts
  - Number of unique locations searched
  - Number of unique search names used
  - Database file path

By default, the cache database is stored in the system's temporary directory (`/tmp` on Linux/macOS).

### Example Usage

```sh
weathergrabber "London" --output console --lang en-GB
weathergrabber --location-id 1234567890abcdef... --output json
weathergrabber "Paris" -o waybar -i fa
weathergrabber "New York" --force-cache
weathergrabber --cache-statistics
```

Or as a Python module:

```sh
python -m weathergrabber "London" --output console --lang en-GB
python -m weathergrabber --location-id 1234567890abcdef... --output json
python -m weathergrabber "Paris" -o waybar -i fa
python -m weathergrabber "Toronto" --force-cache
python -m weathergrabber --cache-statistics
```
