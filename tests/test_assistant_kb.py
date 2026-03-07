from streamlit_app_successful import generate_assistant_response


def test_kb_crop_rotation_definition():
    resp = generate_assistant_response("What is crop rotation?", "Wheat", {})
    assert "crop rotation" in resp.lower()


def test_kb_hot_climate_crops():
    resp = generate_assistant_response("Which crops grow well in hot climates?", "Wheat", {})
    assert "millet" in resp.lower() or "millets" in resp.lower()


def test_kb_tamil_nadu_crops():
    resp = generate_assistant_response("What crops grow best in Tamil Nadu?", "Wheat", {})
    assert "tamil nadu" in resp.lower() or "rice" in resp.lower()


def test_kb_growth_duration_rice():
    resp = generate_assistant_response("How long does rice take to grow?", "Wheat", {})
    assert "120" in resp or "150" in resp


def test_kb_ideal_soil_moisture_rice():
    resp = generate_assistant_response("What is the ideal soil moisture for rice?", "Wheat", {})
    assert "70" in resp or "90" in resp


def test_kb_temperature_for_selected_crop_uses_info():
    resp = generate_assistant_response("What is the best temperature for crop growth?", "Wheat", {"temp": "10-25"})
    assert "10-25" in resp

