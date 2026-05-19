# Amarnath.app

## Soil moisture sensor JSON format (for “Sensor URL”)

The Streamlit app expects your sensor URL to return HTTP JSON. It can handle either:

- Percent:
  - `{"moisture_pct": 42}`
  - `{"moisture": 0.42}` (fraction 0–1)
  - `{"soil_moisture": "42%"}`
- Arduino analog/ADC raw (0–1023) with optional calibration:
  - `{"adc": 650, "wet_raw": 300, "dry_raw": 800}`
  - `{"raw": 650}` (uses defaults `wet_raw=300`, `dry_raw=800`)

Note: An Arduino Uno cannot serve HTTP by itself; you’ll need a Wi‑Fi/Ethernet module (or use an ESP8266/ESP32), or run a small “serial to HTTP” bridge on your computer.
