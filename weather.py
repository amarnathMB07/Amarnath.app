from __future__ import annotations

import json
import urllib.parse
import urllib.request
import urllib.error
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class GeoResult:
    name: str
    latitude: float
    longitude: float
    country: str | None = None
    admin1: str | None = None


_WEATHER_CODE = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def _http_get_json(url: str, timeout_s: float = 10.0) -> dict[str, Any]:
    """HTTP GET JSON with a small amount of retry logic.

    Open-Meteo may return HTTP 429 (Too Many Requests) if the app is re-run
    frequently (Streamlit reruns on widget changes) or multiple users share the
    same outbound IP. When that happens we back off briefly and retry.
    """
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AgroSmart/1.0 (+streamlit)",
            "Accept": "application/json",
        },
        method="GET",
    )

    last_err: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                data = resp.read()
            return json.loads(data.decode("utf-8"))
        except urllib.error.HTTPError as e:
            last_err = e
            # 429 is a transient rate limit; respect Retry-After if present.
            if getattr(e, "code", None) == 429 and attempt < 2:
                retry_after = e.headers.get("Retry-After") if getattr(e, "headers", None) else None
                try:
                    sleep_s = float(retry_after) if retry_after else 1.5 * (attempt + 1)
                except Exception:
                    sleep_s = 1.5 * (attempt + 1)
                time.sleep(max(0.5, min(10.0, sleep_s)))
                continue
            raise
        except Exception as e:
            last_err = e
            raise

    if last_err:
        raise last_err
    raise RuntimeError("HTTP request failed")


def _geocode_open_meteo(name: str, *, count: int = 5) -> list[GeoResult]:
    """Resolve a human location name into lat/lon via Open-Meteo geocoding."""
    q = urllib.parse.urlencode(
        {"name": name, "count": count, "language": "en", "format": "json"}
    )
    url = f"https://geocoding-api.open-meteo.com/v1/search?{q}"
    payload = _http_get_json(url)
    if payload.get("error"):
        raise ValueError(str(payload.get("reason") or "Geocoding API error"))
    results = payload.get("results") or []
    out: list[GeoResult] = []
    for r in results:
        try:
            out.append(
                GeoResult(
                    name=str(r.get("name") or name),
                    latitude=float(r["latitude"]),
                    longitude=float(r["longitude"]),
                    country=(str(r["country"]) if r.get("country") else None),
                    admin1=(str(r["admin1"]) if r.get("admin1") else None),
                )
            )
        except Exception:
            continue
    return out


def _geocode_nominatim(name: str, *, count: int = 5) -> list[GeoResult]:
    """Fallback geocoder using OpenStreetMap Nominatim."""
    q = urllib.parse.urlencode({"q": name, "format": "json", "limit": count})
    url = f"https://nominatim.openstreetmap.org/search?{q}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AgroSmart/1.0 (+streamlit; geocoding)",
            "Accept": "application/json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=10.0) as resp:
        data = resp.read()
    payload = json.loads(data.decode("utf-8"))
    if not isinstance(payload, list):
        return []
    out: list[GeoResult] = []
    for r in payload:
        try:
            out.append(
                GeoResult(
                    name=str(r.get("display_name") or r.get("name") or name),
                    latitude=float(r["lat"]),
                    longitude=float(r["lon"]),
                    country=None,
                    admin1=None,
                )
            )
        except Exception:
            continue
    return out


def geocode(name: str, *, count: int = 5) -> list[GeoResult]:
    """Resolve a human location name into lat/lon.

    Tries Open-Meteo geocoding first, then falls back to Nominatim if it
    returns no results (or the API response omits `results`).
    """
    try:
        results = _geocode_open_meteo(name, count=count)
        if results:
            return results
    except Exception:
        # fall back to Nominatim
        pass

    try:
        return _geocode_nominatim(name, count=count)
    except Exception:
        return []


def get_current_weather(latitude: float, longitude: float) -> dict[str, Any]:
    """Fetch current conditions and (best-effort) current hour rain probability."""
    q = urllib.parse.urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                ]
            ),
            "hourly": "precipitation_probability",
            "forecast_days": 1,
            "timezone": "auto",
        }
    )
    url = f"https://api.open-meteo.com/v1/forecast?{q}"
    payload = _http_get_json(url)
    if payload.get("error"):
        raise ValueError(str(payload.get("reason") or "Weather API error"))

    current = payload.get("current") or {}
    code = current.get("weather_code")
    description = _WEATHER_CODE.get(int(code), "Unknown") if code is not None else "Unknown"

    rain_prob: int | None = None
    try:
        hourly = payload.get("hourly") or {}
        times = hourly.get("time") or []
        probs = hourly.get("precipitation_probability") or []
        current_time = current.get("time")
        if current_time and times and probs and len(times) == len(probs):
            if current_time in times:
                idx = times.index(current_time)
                rain_prob = int(probs[idx]) if probs[idx] is not None else None
            else:
                rain_prob = int(probs[0]) if probs[0] is not None else None
    except Exception:
        rain_prob = None

    return {
        "temperature_c": current.get("temperature_2m"),
        "humidity_pct": current.get("relative_humidity_2m"),
        "wind_kph": current.get("wind_speed_10m"),
        "precip_mm": current.get("precipitation"),
        "weather_code": code,
        "condition": description,
        "rain_probability_pct": rain_prob,
        "asof": current.get("time") or datetime.now(timezone.utc).isoformat(),
    }


def fetch_sensor_moisture(url: str) -> float:
    """Fetch soil moisture from a simple HTTP JSON endpoint.

    Accepts JSON keys: moisture, soil_moisture, value. Returns a percentage 0-100.
    If the value appears to be 0-1, it is treated as a fraction and converted to percent.
    """
    payload = _http_get_json(url, timeout_s=5.0)
    for key in ("moisture", "soil_moisture", "value"):
        if key in payload:
            val = payload[key]
            break
    else:
        raise ValueError("JSON does not contain moisture/soil_moisture/value")

    moisture = float(val)
    if 0.0 <= moisture <= 1.0:
        moisture *= 100.0
    return max(0.0, min(100.0, moisture))
