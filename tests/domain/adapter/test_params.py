import pytest
from weathergrabber.domain.adapter.params import Params

class DummyOutputEnum:
    def __str__(self):
        return "console"
class DummyIconEnum:
    def __str__(self):
        return "emoji"

def test_location_properties():
    loc = Params.Location("TestCity", "12345")
    assert loc.search_name == "TestCity"
    assert loc.id == "12345"
    s = str(loc)
    assert "Location(" in s
    assert "search_name=TestCity" in s
    assert "id=12345" in s

def test_params_properties():
    loc = Params.Location("TestCity", "12345")
    params = Params(
        location=loc,
        language="fr-FR",
        output_format=DummyOutputEnum(),
        keep_open=True,
        icons=DummyIconEnum()
    )
    assert params.location is loc
    assert params.language == "fr-FR"
    assert params.output_format.__str__() == "console"
    assert params.keep_open is True
    assert params.icons.__str__() == "emoji"
    s = str(params)
    assert "Params(" in s
    assert "location=" in s
    assert "language=fr-FR" in s
    assert "output_format=console" in s
    assert "keep_open=True" in s
    assert "icons=emoji" in s
