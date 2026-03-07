from __future__ import annotations

import html
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class WeatherSnapshot:
    temperature_c: float | None = None
    humidity_pct: float | None = None
    wind_kph: float | None = None
    rain_probability_pct: int | None = None
    condition: str | None = None
    asof: str | None = None


@dataclass(frozen=True)
class MoistureReading:
    moisture_pct: float
    created_at: str | None = None
    source: str | None = None


def _esc(s: Any) -> str:
    if s is None:
        return ""
    return html.escape(str(s))


def _fmt_pct(x: float | None) -> str:
    if x is None:
        return "N/A"
    return f"{x:.1f}%"


def _class_for_moisture(m: float | None) -> str:
    if m is None:
        return "neutral"
    if m < 30:
        return "bad"
    if m > 80:
        return "warn"
    return "good"


def _stage_for_days(days_since_planting: int, harvest_days: int) -> str:
    if harvest_days <= 0:
        return "Unknown stage"
    progress = max(0.0, min(1.0, days_since_planting / float(harvest_days)))
    if progress < 0.15:
        return "Germination / Seedling"
    if progress < 0.55:
        return "Vegetative growth"
    if progress < 0.80:
        return "Flowering / Fruiting"
    return "Maturity / Pre-harvest"


def _crop_hazards(crop: str) -> list[str]:
    c = (crop or "").strip().lower()
    if c == "rice":
        return [
            "Stem borer, leaf folder, planthoppers (insects)",
            "Blast and sheath blight (fungal diseases, higher risk in humid weather)",
            "Waterlogging vs. drought stress depending on irrigation control",
            "Weed pressure in early stages if water levels are not managed",
        ]
    if c == "wheat":
        return [
            "Rust diseases (yellow/brown rust), especially in cool humid weather",
            "Aphids and termites (region dependent)",
            "Heat stress during grain filling (late-season high temperature)",
            "Lodging if excessive nitrogen + wind/rain",
        ]
    if c == "tomato":
        return [
            "Early blight / late blight (higher risk with humidity and leaf wetness)",
            "Fruit borer and whiteflies (can spread viral diseases)",
            "Blossom end rot (often linked to irregular watering / calcium uptake issues)",
            "Cracking and fungal issues if watering/rain fluctuates",
        ]
    if c == "corn" or c == "maize":
        return [
            "Fall armyworm / stem borers",
            "Leaf blights and downy mildew (humidity dependent)",
            "Drought stress during tasseling/silking",
        ]
    return [
        "Pest/disease pressure (varies by region and season)",
        "Heat/cold stress outside the crop’s optimal temperature range",
        "Water stress (too dry or too wet) depending on soil type and irrigation",
    ]


def _crop_prevention(crop: str) -> list[str]:
    c = (crop or "").strip().lower()
    if c == "rice":
        return [
            "Use resistant varieties where available; follow district advisory for seed selection.",
            "Keep field drainage channels clear; avoid stagnant water for long periods if disease pressure is high.",
            "Monitor pests weekly (especially stem borer/planthoppers); use traps and targeted control if thresholds are crossed.",
            "Use balanced fertilizer (avoid excess nitrogen which increases pest/disease risk).",
        ]
    if c == "wheat":
        return [
            "Choose rust-resistant varieties; inspect leaves for rust spots in cool/humid periods.",
            "Avoid excess nitrogen; split doses and ensure good potassium for stronger stems.",
            "Irrigate at critical stages (crown root initiation, tillering, heading) without waterlogging.",
            "Keep weeds controlled early to avoid nutrient and moisture competition.",
        ]
    if c == "tomato":
        return [
            "Stake plants and keep good spacing for airflow; avoid wetting leaves late in the day.",
            "Mulch to keep moisture stable; irregular watering increases blossom end rot and cracking.",
            "Use yellow sticky traps and monitor whiteflies; remove heavily infected plants early if viral symptoms appear.",
            "Follow a preventive spray schedule only if needed and as per local guidance; rotate modes of action.",
        ]
    if c in ("corn", "maize"):
        return [
            "Scout for fall armyworm early; use pheromone traps and destroy egg masses if found.",
            "Ensure adequate moisture during tasseling/silking; drought here reduces yield the most.",
            "Avoid lodging with balanced nutrition and proper plant spacing.",
        ]
    return [
        "Use certified seed suited to your season and soil.",
        "Do soil testing and apply balanced nutrients (NPK + micronutrients if needed).",
        "Keep soil moisture in the crop’s safe range; ensure drainage after heavy rain.",
        "Scout weekly for pests/disease and act early using IPM methods.",
    ]


def _future_threats_and_solutions(crop: str) -> list[tuple[str, str]]:
    c = (crop or "").strip().lower()
    common = [
        ("Heat waves", "Use mulching, timely irrigation, shade nets (for vegetables), and heat-tolerant varieties."),
        ("Irregular rainfall", "Improve drainage, harvest rainwater, and use soil moisture–based irrigation scheduling."),
        ("New pest pressure", "Regular scouting + traps, rotate pesticides responsibly, and use resistant varieties when available."),
        ("Soil fertility decline", "Add compost/FYM, use cover crops/green manure, and rotate crops to rebuild organic matter."),
    ]
    if c == "rice":
        return [
            ("Blast/sheath blight outbreaks", "Use resistant varieties, avoid excess nitrogen, and manage water + spacing to reduce humidity in canopy."),
            ("Planthopper surges", "Avoid overuse of nitrogen, preserve beneficial insects, and use threshold-based sprays."),
        ] + common
    if c == "wheat":
        return [
            ("Rust epidemics", "Plant rust-resistant varieties and follow timely fungicide only when advised; avoid late sowing in risky zones."),
            ("Terminal heat stress", "Prefer timely sowing and heat-tolerant varieties; ensure irrigation during grain filling."),
        ] + common
    if c == "tomato":
        return [
            ("Late blight during humid spells", "Improve airflow, avoid leaf wetness, and use preventive protection only when conditions are favorable for blight."),
            ("Viral diseases via whiteflies", "Use nets/traps, remove infected plants early, and control vector population."),
        ] + common
    return common


def _weather_risk_notes(w: WeatherSnapshot | None) -> list[str]:
    if not w:
        return []
    notes: list[str] = []
    if w.temperature_c is not None and w.temperature_c >= 35:
        notes.append("High temperature: risk of heat stress and faster water loss.")
    if w.temperature_c is not None and w.temperature_c <= 10:
        notes.append("Low temperature: risk of slowed growth or cold stress (crop dependent).")
    if w.humidity_pct is not None and w.humidity_pct >= 80:
        notes.append("High humidity: higher fungal disease risk; improve airflow and monitor leaf spots.")
    if w.rain_probability_pct is not None and w.rain_probability_pct >= 70:
        notes.append("High chance of rain: avoid over-irrigation; ensure field drainage.")
    if w.wind_kph is not None and w.wind_kph >= 25:
        notes.append("Strong wind: risk of lodging for tall crops and faster evaporation.")
    return notes


def _question_topics(questions: Sequence[str]) -> list[str]:
    topics: list[str] = []
    joined = " ".join(q.lower() for q in questions)
    if any(k in joined for k in ("soil", "ph", "fertility", "loamy", "clay", "sandy")):
        topics.append("Soil")
    if any(k in joined for k in ("moisture", "water", "irrigation", "drip", "sprinkler")):
        topics.append("Irrigation/Water")
    if any(k in joined for k in ("fertil", "npk", "urea", "dap")):
        topics.append("Fertilizer/Nutrients")
    if any(k in joined for k in ("pest", "disease", "fung", "insect")):
        topics.append("Pests/Diseases")
    if any(k in joined for k in ("season", "weather", "rain", "temperature", "climate")):
        topics.append("Season/Weather")
    if any(k in joined for k in ("harvest", "days", "grow", "duration")):
        topics.append("Harvest/Growth duration")
    return topics


def build_final_review_html(
    *,
    email: str,
    crop: str,
    crop_info: Mapping[str, Any],
    location_query: str | None,
    planting_date: date | None,
    harvest_date: date | None,
    harvest_days: int | None,
    moisture_recent: Sequence[MoistureReading],
    latest_moisture: float | None,
    assistant_questions: Sequence[str],
    weather: WeatherSnapshot | None = None,
) -> str:
    crop_name = crop or "Unknown crop"
    temp = crop_info.get("temp")
    water_req = crop_info.get("water")
    season = crop_info.get("season")
    fertilizer = crop_info.get("fertilizer")
    harvest_text = crop_info.get("harvest")

    q_topics = _question_topics(assistant_questions)
    hazards = _crop_hazards(crop_name)
    prevention = _crop_prevention(crop_name)
    future_threats = _future_threats_and_solutions(crop_name)
    weather_notes = _weather_risk_notes(weather)

    today = datetime.now().date()
    days_since = None
    stage = None
    if planting_date:
        days_since = max(0, (today - planting_date).days)
        if harvest_days:
            stage = _stage_for_days(days_since, int(harvest_days))

    moisture_class = _class_for_moisture(latest_moisture)
    moisture_note = ""
    if latest_moisture is not None:
        if latest_moisture < 30:
            moisture_note = "Soil is dry — consider irrigation or mulching."
        elif latest_moisture > 80:
            moisture_note = "Soil is very wet — check drainage and avoid over-irrigation."
        else:
            moisture_note = "Soil moisture is in a healthy range."

    def li(items: Sequence[str]) -> str:
        if not items:
            return "<li>None</li>"
        return "".join(f"<li>{_esc(x)}</li>" for x in items)

    def li_pairs(items: Sequence[tuple[str, str]]) -> str:
        if not items:
            return "<li>None</li>"
        out = ""
        for title, body in items:
            out += f"<li><b>{_esc(title)}:</b> {_esc(body)}</li>"
        return out

    moisture_rows = ""
    for r in list(moisture_recent)[:8]:
        moisture_rows += (
            "<tr>"
            f"<td>{_esc(r.created_at or '')}</td>"
            f"<td style='text-align:right'>{_esc(f'{r.moisture_pct:.1f}%')}</td>"
            f"<td>{_esc(r.source or '')}</td>"
            "</tr>"
        )
    if not moisture_rows:
        moisture_rows = "<tr><td colspan='3'>No saved soil moisture readings for this crop.</td></tr>"

    weather_block = ""
    if weather:
        weather_block = f"""
          <div class="card">
            <div class="card-title">Weather snapshot</div>
            <div class="grid2">
              <div><span class="k">Condition</span><br><span class="v">{_esc(weather.condition or 'N/A')}</span></div>
              <div><span class="k">As of</span><br><span class="v">{_esc(weather.asof or 'N/A')}</span></div>
              <div><span class="k">Temperature</span><br><span class="v">{_esc(_fmt_pct(weather.temperature_c).replace('%',''))} °C</span></div>
              <div><span class="k">Humidity</span><br><span class="v">{_esc(_fmt_pct(float(weather.humidity_pct) if weather.humidity_pct is not None else None))}</span></div>
              <div><span class="k">Wind</span><br><span class="v">{_esc(_fmt_pct(float(weather.wind_kph) if weather.wind_kph is not None else None).replace('%',''))} km/h</span></div>
              <div><span class="k">Chance of rain</span><br><span class="v">{_esc(str(weather.rain_probability_pct) + '%' if weather.rain_probability_pct is not None else 'N/A')}</span></div>
            </div>
          </div>
        """

    loc = (location_query or "").strip()
    loc_line = f"<div class='muted'>Location: {_esc(loc) if loc else 'N/A'}</div>"

    planting_line = "N/A"
    if planting_date:
        planting_line = planting_date.strftime("%Y-%m-%d")
    harvest_line = "N/A"
    if harvest_date:
        harvest_line = harvest_date.strftime("%Y-%m-%d")

    stage_line = stage or "N/A"
    if days_since is None:
        days_since_line = "N/A"
    else:
        days_since_line = str(days_since)

    questions_preview = [q.strip() for q in assistant_questions if q.strip()][-6:]
    questions_preview.reverse()

    html_out = f"""
    <style>
      @keyframes finalReveal {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to   {{ opacity: 1; transform: translateY(0px); }}
      }}
      .final-report {{ font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; color: #05391f; }}
      .final-report.reveal {{ animation: finalReveal 650ms ease-out; }}
      .final-header {{ display:flex; gap:12px; align-items:flex-start; justify-content:space-between; margin-bottom:10px; }}
      .final-title {{ font-size: 1.15rem; font-weight: 800; }}
      .muted {{ color: rgba(3,77,35,0.72); font-size: 0.92rem; }}
      .grid2 {{ display:grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
      .card {{ background: rgba(255,255,255,0.92); border: 1px solid rgba(3,77,35,0.15); border-radius: 12px; padding: 12px; }}
      .card-title {{ font-weight: 800; margin-bottom: 8px; }}
      .k {{ font-size: 0.86rem; color: rgba(3,77,35,0.72); }}
      .v {{ font-size: 0.98rem; }}
      .sp {{ height: 8px; }}
      .badge {{ border-radius: 999px; padding: 6px 10px; font-weight: 800; border: 1px solid rgba(3,77,35,0.15); background: rgba(255,255,255,0.75); white-space: nowrap; }}
      .badge-good {{ background: rgba(46,125,50,0.12); }}
      .badge-warn {{ background: rgba(255,193,7,0.18); }}
      .badge-bad  {{ background: rgba(244,67,54,0.14); }}
      .tbl {{ width: 100%; border-collapse: collapse; font-size: 0.92rem; }}
      .tbl th, .tbl td {{ border-bottom: 1px solid rgba(3,77,35,0.10); padding: 6px 4px; vertical-align: top; }}
      ul {{ margin: 6px 0 0 18px; }}
      .callout {{ border-left: 4px solid rgba(46,125,50,0.55); padding-left: 10px; margin-top: 8px; }}
      @media (max-width: 900px) {{ .grid2 {{ grid-template-columns: 1fr; }} .badge {{ white-space: normal; }} }}
    </style>

    <div class="final-report reveal">
      <div class="final-header">
        <div>
          <div class="final-title">Final Crop Review</div>
          <div class="muted">User: {_esc(email)} · Crop: <b>{_esc(crop_name)}</b></div>
          {loc_line}
        </div>
        <div class="badge badge-{_esc(moisture_class)}">Soil moisture: {_esc(_fmt_pct(latest_moisture))}</div>
      </div>

      <div class="grid2">
        <div class="card">
          <div class="card-title">Crop profile</div>
          <div><span class="k">Optimal temperature</span><br><span class="v">{_esc(temp or 'N/A')} °C</span></div>
          <div class="sp"></div>
          <div><span class="k">Water requirement</span><br><span class="v">{_esc(water_req or 'N/A')}</span></div>
          <div class="sp"></div>
          <div><span class="k">Best season</span><br><span class="v">{_esc(season or 'N/A')}</span></div>
          <div class="sp"></div>
          <div><span class="k">Fertilizer note</span><br><span class="v">{_esc(fertilizer or 'N/A')}</span></div>
          <div class="sp"></div>
          <div><span class="k">Typical harvest time</span><br><span class="v">{_esc(harvest_text or 'N/A')}</span></div>
        </div>

        <div class="card">
          <div class="card-title">Your timeline</div>
          <div><span class="k">Planting date</span><br><span class="v">{_esc(planting_line)}</span></div>
          <div class="sp"></div>
          <div><span class="k">Expected harvest date</span><br><span class="v">{_esc(harvest_line)}</span></div>
          <div class="sp"></div>
          <div><span class="k">Days since planting</span><br><span class="v">{_esc(days_since_line)}</span></div>
          <div class="sp"></div>
          <div><span class="k">Estimated growth stage</span><br><span class="v">{_esc(stage_line)}</span></div>
          <div class="sp"></div>
          <div><span class="k">Notes</span><br><span class="v">{_esc(str(moisture_note) if moisture_note else '')}</span></div>
        </div>
      </div>

      {weather_block}

      <div class="grid2">
        <div class="card">
          <div class="card-title">Saved soil moisture (recent)</div>
          <table class="tbl">
            <thead><tr><th>Time</th><th style="text-align:right">Moisture</th><th>Source</th></tr></thead>
            <tbody>{moisture_rows}</tbody>
          </table>
          <div class="muted">Tip: Calibrate your sensor (wet_raw/dry_raw) for more accurate % values.</div>
        </div>

        <div class="card">
          <div class="card-title">Your questions</div>
          <div class="muted">Recent topics: {_esc(", ".join(q_topics) if q_topics else "N/A")}</div>
          <ul>{li(questions_preview or [])}</ul>
        </div>
      </div>

      <div class="grid2">
        <div class="card">
          <div class="card-title">Likely hazards to watch</div>
          <ul>{li(hazards)}</ul>
          <div class="callout"><b>Prevention checklist</b><ul>{li(prevention)}</ul></div>
        </div>
        <div class="card">
          <div class="card-title">Weather + field risk notes</div>
          <ul>{li(weather_notes)}</ul>
          <div class="sp"></div>
          <div class="card-title">Future threats (and avoidable solutions)</div>
          <ul>{li_pairs(future_threats)}</ul>
          <div class="muted">Always confirm with local agricultural advisories for your district.</div>
        </div>
      </div>

      <div class="muted">
        Generated on {today.strftime("%Y-%m-%d")}. This is an advisory summary based on the data available in the app.
      </div>
    </div>
    """
    return html_out
