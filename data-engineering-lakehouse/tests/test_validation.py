from src.generator import generate_event
from src.validation import validate_event


def test_valid_event():
    ok, errors = validate_event(generate_event("SOLAR_001"))
    assert ok
    assert errors == []


def test_negative_power_is_rejected():
    event = generate_event()
    event["power_kw"] = -1
    ok, errors = validate_event(event)
    assert not ok
    assert "power_kw must be non negative" in errors
