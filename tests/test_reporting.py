from datetime import date

from reporting import (
    MoistureReading,
    WeatherSnapshot,
    build_final_review_html,
)


def test_build_final_review_html_includes_core_fields():
    html = build_final_review_html(
        email="a@example.com",
        crop="Rice",
        crop_info={
            "temp": "20-35",
            "water": "Very high",
            "season": "Summer/Monsoon",
            "fertilizer": "Organic compost plus urea or DAP.",
            "harvest": "120-150 days",
        },
        location_query="Chennai, India",
        planting_date=date(2026, 1, 1),
        harvest_date=date(2026, 5, 15),
        harvest_days=120,
        moisture_recent=[
            MoistureReading(moisture_pct=55.0, created_at="2026-03-01 10:00:00", source="manual"),
        ],
        latest_moisture=55.0,
        assistant_questions=["What is crop rotation?", "How long does rice take to grow?"],
        weather=WeatherSnapshot(
            temperature_c=36.0,
            humidity_pct=85.0,
            wind_kph=10.0,
            rain_probability_pct=80,
            condition="Clear",
            asof="2026-03-08T10:00:00Z",
        ),
    )
    assert "Final Crop Review" in html
    assert "Rice" in html
    assert "Chennai" in html
    assert "Saved soil moisture" in html
    assert "Likely hazards" in html


def test_build_final_review_html_escapes_email():
    html = build_final_review_html(
        email="<script>alert(1)</script>",
        crop="Wheat",
        crop_info={},
        location_query=None,
        planting_date=None,
        harvest_date=None,
        harvest_days=None,
        moisture_recent=[],
        latest_moisture=None,
        assistant_questions=[],
        weather=None,
    )
    assert "<script>" not in html

