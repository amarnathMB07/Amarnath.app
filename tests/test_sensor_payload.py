import pytest

from weather import parse_sensor_moisture_payload


def test_parse_sensor_moisture_payload_percent_number():
    assert parse_sensor_moisture_payload({"moisture_pct": 42}) == 42.0
    assert parse_sensor_moisture_payload({"moisture_percent": 55.5}) == 55.5


def test_parse_sensor_moisture_payload_percent_fraction():
    assert parse_sensor_moisture_payload({"moisture": 0.42}) == 42.0


def test_parse_sensor_moisture_payload_percent_string():
    assert parse_sensor_moisture_payload({"soil_moisture": "42%"}) == 42.0


def test_parse_sensor_moisture_payload_adc_with_calibration():
    # dry_raw => 0%, wet_raw => 100%
    # raw=650, wet=300, dry=800 => (650-800)/(300-800)*100 = 30
    assert parse_sensor_moisture_payload({"adc": 650, "wet_raw": 300, "dry_raw": 800}) == 30.0


def test_parse_sensor_moisture_payload_legacy_key_as_raw_when_calibrated():
    assert parse_sensor_moisture_payload({"value": 650, "wet_raw": 300, "dry_raw": 800}) == 30.0


def test_parse_sensor_moisture_payload_adc_defaults_and_clamp():
    # With defaults wet=300/dry=800, raw below wet should clamp to 100.
    assert parse_sensor_moisture_payload({"raw": 250}) == 100.0


def test_parse_sensor_moisture_payload_missing_keys():
    with pytest.raises(ValueError):
        parse_sensor_moisture_payload({"hello": "world"})

