from streamlit_app_successful import parse_days


def test_parse_days_basic():
    assert parse_days("120 days") == 120
    assert parse_days("90-120 days") == 90
    assert parse_days("nonsense") is None
