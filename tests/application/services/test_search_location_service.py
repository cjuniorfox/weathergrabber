import pytest
from unittest.mock import MagicMock
from weathergrabber.application.services.search_location_service import SearchLocationService

class DummyApi:
    def __init__(self, response):
        self._response = response
    def search(self, location_name, lang):
        return self._response

def test_execute_success():
    location_id = "abc123"
    api_response = {
        "dal": {
            "getSunV3LocationSearchUrlConfig": {
                "key1": {
                    "data": {
                        "location": {
                            "placeId": [location_id]
                        }
                    }
                }
            }
        }
    }
    api = DummyApi(api_response)
    service = SearchLocationService(api)
    result = service.execute("London", "en-US")
    assert result == location_id

def test_execute_no_location_name():
    api = DummyApi(None)
    service = SearchLocationService(api)
    result = service.execute("", "en-US")
    assert result is None

def test_execute_not_found():
    api = DummyApi({})
    service = SearchLocationService(api)
    with pytest.raises(ValueError, match="Could not find location 'Paris'."):
        service.execute("Paris", "en-US")

def test_execute_api_error():
    class ErrorApi:
        def search(self, location_name, lang):
            raise Exception("API error")
    api = ErrorApi()
    service = SearchLocationService(api)
    with pytest.raises(ValueError, match="Could not find location 'Berlin'."):
        service.execute("Berlin", "en-US")
