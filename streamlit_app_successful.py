import streamlit as st
from datetime import datetime, timedelta

# database helpers initialize on import
import database
import weather
import reporting

database.init_db()

# Page config must be set after importing streamlit
st.set_page_config(page_title="AgroSmart", page_icon="🌾", layout="centered")

# --- Styles (green / natural theme) ---
st.markdown(
    """
    <style>
    .reportview-container { background: linear-gradient(#f7fff7, #eaf8eb); }
    .stApp { color: #034d23; }
    h1, h2, h3, h4, h5, h6 { color: #034d23; }
    .stButton>button { background-color: #2e7d32; color: white; }

    /* Final review reveal animation */
    @keyframes finalReveal {
      from { opacity: 0; transform: translateY(10px); }
      to   { opacity: 1; transform: translateY(0px); }
    }
    .final-report.reveal { animation: finalReveal 650ms ease-out; }
    .final-header { display:flex; gap:12px; align-items:flex-start; justify-content:space-between; margin-bottom:10px; }
    .final-title { font-size: 1.15rem; font-weight: 700; }
    .muted { color: rgba(3,77,35,0.72); font-size: 0.92rem; }
    .grid2 { display:grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .card { background: rgba(255,255,255,0.78); border: 1px solid rgba(3,77,35,0.15); border-radius: 12px; padding: 12px; }
    .card-title { font-weight: 700; margin-bottom: 8px; }
    .k { font-size: 0.86rem; color: rgba(3,77,35,0.72); }
    .v { font-size: 0.98rem; }
    .sp { height: 8px; }
    .badge { border-radius: 999px; padding: 6px 10px; font-weight: 700; border: 1px solid rgba(3,77,35,0.15); background: rgba(255,255,255,0.65); }
    .badge-good { background: rgba(46,125,50,0.12); }
    .badge-warn { background: rgba(255,193,7,0.18); }
    .badge-bad  { background: rgba(244,67,54,0.14); }
    .tbl { width: 100%; border-collapse: collapse; font-size: 0.92rem; }
    .tbl th, .tbl td { border-bottom: 1px solid rgba(3,77,35,0.10); padding: 6px 4px; vertical-align: top; }
    @media (max-width: 900px) { .grid2 { grid-template-columns: 1fr; } }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session state defaults ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ''


def _safe_rerun():
    """Try to rerun the Streamlit script. If the current Streamlit
    build doesn't expose `experimental_rerun`, fall back to setting a
    query param and stopping the script which causes a reload in the
    browser."""
    try:
        # Preferred - available in many Streamlit versions
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
            return
        # Older/newer variants
        if hasattr(st, "rerun"):
            st.rerun()
            return
    except Exception:
        pass

    # Fallback: change query params to force a rerun, then stop execution
    try:
        st.experimental_set_query_params(_rerun=str(datetime.now().timestamp()))
    except Exception:
        # If even that fails, just stop (user can refresh)
        pass
    st.stop()

def parse_days(text):
    # expect something like '120 days' or '90-120 days'
    try:
        parts = text.split()[0]
        if '-' in parts:
            return int(parts.split('-')[0])
        return int(parts)
    except Exception:
        return None


import os
import assistant_kb

try:
    import openai
except ImportError:
    openai = None


def generate_assistant_response(question: str, crop: str, info: dict) -> str:
    """Produce a response given the user's question.

    If an OpenAI API key is configured in the environment, send the prompt to
    the ChatCompletion API and return the model's reply. Otherwise fall back to
    a simple rule-based answer implemented in this module.

    The rule engine also handles basic greetings and offers tips on how to
    use the system. Interactions are logged to console for debugging.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key and openai:
        try:
            openai.api_key = api_key
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful farming assistant."},
                    {"role": "user", "content": f"Question: {question}\nCrop: {crop}\nInfo: {info}"},
                ],
                max_tokens=150,
                temperature=0.7,
            )
            return completion.choices[0].message.content.strip()
        except Exception:
            # if the API call fails, fall back to rules
            pass

    # rule-based fallback with conversational rules
    q = question.strip().lower()
    # greetings - match whole words to avoid false positives (e.g. 'this')
    q_words = q.replace("?", "").replace("!", "").split()
    greetings = ["hi", "hello", "hey", "good", "good morning", "good afternoon", "good evening"]
    if any(word in greetings for word in q_words) or any(q.startswith(g) for g in ["good morning", "good afternoon", "good evening"]):
        return (
            "Hello! I'm AgroSmart, your farming assistant. You can ask me things like 'What fertilizer should I use?' or 'When is harvest time?'."
        )
    if "thank" in q:
        return "You're welcome! Glad I could help."
    if "help" in q or ("how" in q and "use" in q):
        return (
            "Ask me about soil, water needs, fertilizers, seasons, or harvest times. "
            "You can also just say hello!"
        )

    kb_answer = assistant_kb.answer_question(question, crop, info)
    if kb_answer:
        return kb_answer
    if "soil" in q:
        if crop.lower() == "rice":
            return (
                "Rice prefers heavy, water-retentive soil and flooded conditions. "
                "Maintain high moisture for best results."
            )
        else:
            return (
                "Soil suitability varies. Make sure the soil meets the temperature "
                "and moisture requirements of the crop."
            )
    if "fertil" in q:
        # provide main fertilizer and alternates
        main = info.get("fertilizer", "a balanced NPK fertilizer")
        alternates = {
            "Wheat": ["urea", "DAP", "NPK 20-20-0"],
            "Corn": ["NPK 16-20-0", "urea", "ammonium nitrate"],
            "Rice": ["urea", "DAP", "organic compost"],
            "Tomato": ["potassium sulfate", "phosphate-rich fertilizers"],
            "Soybean": ["legume inoculants", "phosphorus fertilizers"],
        }
        alts = alternates.get(crop, [])
        msg = f"Main recommendation: {main}."
        if alts:
            msg += " Alternate options: " + ", ".join(alts) + "."
        return msg
    if "water" in q:
        return f"{info.get('water', 'Moderate')} water requirement."
    if "harvest" in q:
        return f"Typical harvest time is {info.get('harvest', 'unknown')}"
    if "season" in q:
        return info.get('season', 'Depends on local climate.')
    # fallback
    return (
        "I'm not sure about that. Try asking about soil, water, fertilizer, season, or harvest."
    )


def show_login():
    st.title("AgroSmart 🌱 — Farm Dashboard")
    st.write("Welcome — please log in to continue.")
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    register = st.checkbox("Register instead")

    if st.button("Continue"):
        # Basic validation
        if not email or not password:
            st.error("Please enter both email and password.")
            return

        if register:
            if database.create_user(email, password):
                st.success("Registration complete. You can now log in.")
            else:
                st.error("Email already registered.")
            return

        # authentication
        if database.authenticate_user(email, password):
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success("Login successful — redirecting to dashboard...")
            _safe_rerun()
        else:
            st.error("Invalid credentials. If you don't have an account, check the register box.")

def show_dashboard():
    st.sidebar.title("AgroSmart 🌾")
    st.sidebar.write("Green insights for your farm")

    st.sidebar.subheader("Location")
    if "location_query" not in st.session_state:
        st.session_state.location_query = "San Francisco, CA"
    st.session_state.location_query = st.sidebar.text_input(
        "City / Place", st.session_state.location_query
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.email = ''
        _safe_rerun()

    st.header(f"Welcome, {st.session_state.email} 🌿")
    st.caption(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- Crop Information ---
    st.subheader("Crop Information 🌾")
    crops = database.get_crops()
    crop = st.selectbox("Select a crop", crops)

    info = database.get_crop_info(crop)
    st.write(f"**Optimal Temperature (°C):** {info.get('temp')}")
    st.write(f"**Water Requirement:** {info.get('water')}")
    st.write(f"**Typical Harvest Time:** {info.get('harvest')}")

    # allow manual planting date adjustment
    st.write("---")
    planting_date = st.date_input("Select planting date", datetime.now().date())
    harvest_days = parse_days(info.get('harvest', '')) or 0
    harvest_date = datetime.combine(planting_date, datetime.min.time()) + timedelta(days=harvest_days)
    st.write(f"Expected harvest around: **{harvest_date.strftime('%Y-%m-%d')}**")

    # --- Crop Q&A ---
    st.subheader("Ask about your crop ❓")
    questions = [
        "Is my soil good for rice?",
        "What fertilizer should I use?",
        "How much water does this crop need?",
        "When is harvest time?",
        "Which season is best?",
        "Which crop is selected right now?",
        "Tell me about this crop",
        "What are the requirements of this crop?",
        "Is this crop suitable for my land?",
        "What is the growth duration of this crop?",
        "How many days to harvest?",
    ]
    q = st.selectbox("Select a question", questions)

    # helper values are now in the crop info retrieved earlier
    season_db = {crop: database.get_crop_info(crop).get('season') for crop in crops}
    fertilizer_db = {crop: database.get_crop_info(crop).get('fertilizer') for crop in crops}


    answer = ""
    if q == "Is my soil good for rice?":
        if crop == "Rice":
            answer = (
                "Rice prefers heavy, water-retentive soil and flooded conditions. "
                "Maintain high moisture for best results."
            )
        else:
            answer = "That question is specific to rice; select rice to evaluate."
    elif q == "What fertilizer should I use?":
        answer = fertilizer_db.get(crop, "Use a balanced NPK fertilizer and adjust based on soil test.")
    elif q == "Which season is best?":
        answer = season_db.get(crop, "Depends on local climate.")
    elif q == "How much water does this crop need?":
        answer = f"{info.get('water')} water requirement."
    elif q == "When is harvest time?":
        answer = f"Typical harvest time is {info.get('harvest')}."
    elif q == "Which season is best?":
        answer = season_db.get(crop, "Depends on local climate.")
    elif q == "Which crop is selected right now?":
        answer = f"You have selected {crop}."
    elif q == "Tell me about this crop":
        answer = (
            f"{crop}: optimal temp {info.get('temp')}°C, "
            f"water {info.get('water')}, harvest in {info.get('harvest')}."
        )
    elif q == "What are the requirements of this crop?":
        answer = answer = (
            f"Requires temperatures {info.get('temp')}°C and {info.get('water')} water. "
            f"Harvest around {info.get('harvest')}.")
    elif q == "Is this crop suitable for my land?":
        answer = (
            "Suitability depends on your soil type, moisture and climate. "
            "If you can meet its temperature and water needs, it should be okay."
        )
    elif q == "What is the growth duration of this crop?":
        answer = info.get('harvest')
    elif q == "How many days to harvest?":
        days = parse_days(info.get('harvest',''))
        answer = f"Approximately {days} days." if days else "N/A"

    if answer:
        st.info(answer)

    # --- Simple assistant / chat interface ---
    st.subheader("Ask the AgroSmart assistant 💬")
    st.markdown("*Examples: 'Hello', 'What fertilizer should I use?', 'When is harvest time?'")
    if "assistant_history" not in st.session_state:
        st.session_state.assistant_history = []
    if st.button("Clear conversation"):
        st.session_state.assistant_history = []
    # choose widget based on Streamlit version
    if hasattr(st, "chat_input") and hasattr(st, "chat_message"):
        user_input = st.chat_input("Ask me anything about farming or your selected crop...")
        if user_input:
            resp = generate_assistant_response(user_input, crop, info)
            st.session_state.assistant_history.append(("user", user_input))
            st.session_state.assistant_history.append(("assistant", resp))

        for role, msg in st.session_state.assistant_history:
            st.chat_message(role).write(msg)
    else:
        # fallback for older Streamlit: use text_input + button
        user_input = st.text_input("Your question to the assistant")
        if st.button("Ask") and user_input:
            resp = generate_assistant_response(user_input, crop, info)
            st.session_state.assistant_history.append(("user", user_input))
            st.session_state.assistant_history.append(("assistant", resp))

        for role, msg in st.session_state.assistant_history:
            if role == "user":
                st.markdown(f"**You:** {msg}")
            else:
                st.markdown(f"**Assistant:** {msg}")

    # --- Harvest flowchart ---
    st.subheader("Harvest timeline 📅")
    harvest_days = parse_days(info.get('harvest', '')) or 0
    # use planting_date from user input if available
    if 'planting_date' not in locals():
        planting_dt = datetime.now()
    else:
        planting_dt = datetime.combine(planting_date, datetime.min.time())
    harvest_date = planting_dt + timedelta(days=harvest_days)
    chart = (
        f"Planting ({planting_dt.strftime('%Y-%m-%d')}) → "
        f"Harvest (~{harvest_date.strftime('%Y-%m-%d')})"
    )
    # display as code block to preserve formatting
    st.code(chart)

    # --- Weather Status ---
    st.subheader("Weather Status ☀️🌧️")

    @st.cache_data(ttl=60 * 15)
    def _resolve_location(q: str):
        results = weather.geocode(q, count=5)
        return [r.__dict__ for r in results]

    @st.cache_data(ttl=60 * 30)
    def _fetch_weather(lat: float, lon: float):
        return weather.get_current_weather(lat, lon)

    location_query = st.session_state.get("location_query") or ""

    if st.button("Refresh weather"):
        try:
            _fetch_weather.clear()
        except Exception:
            pass
        try:
            _resolve_location.clear()
        except Exception:
            pass

    use_manual_coords = st.checkbox("Use manual latitude/longitude", value=False)
    manual_lat = st.number_input("Latitude", value=37.7749, format="%.6f", disabled=not use_manual_coords)
    manual_lon = st.number_input("Longitude", value=-122.4194, format="%.6f", disabled=not use_manual_coords)

    if use_manual_coords:
        try:
            w = _fetch_weather(float(manual_lat), float(manual_lon))
            st.session_state["last_weather"] = w
            temp_c = w.get("temperature_c")
            st.metric(label="Temperature", value=f"{temp_c} °C" if temp_c is not None else "N/A")
            st.write(f"**Condition:** {w.get('condition', 'Unknown')}  ")
            if w.get("rain_probability_pct") is not None:
                st.write(f"**Chance of rain (this hour):** {w['rain_probability_pct']}%")
            if w.get("humidity_pct") is not None:
                st.write(f"**Humidity:** {w['humidity_pct']}%")
            if w.get("wind_kph") is not None:
                st.write(f"**Wind:** {w['wind_kph']} km/h")
            st.caption(f"As of: {w.get('asof')}")
        except Exception as e:
            st.warning(f"Weather fetch failed: {e}")
    else:
        try:
            loc_results = _resolve_location(location_query) if location_query else []
        except Exception as e:
            loc_results = []
            st.warning(f"Location lookup failed: {e}")

        if not loc_results:
            if location_query.strip():
                st.warning(
                    "No matching places found. Check spelling and your internet connection, or use manual coordinates."
                )
            else:
                st.info("Enter a city/place name in the sidebar to load real weather.")
        else:
            labels = []
            for r in loc_results:
                parts = [r.get("name")]
                if r.get("admin1"):
                    parts.append(r["admin1"])
                if r.get("country"):
                    parts.append(r["country"])
                labels.append(", ".join([p for p in parts if p]))

            pick = st.selectbox(
                "Weather location", list(range(len(labels))), format_func=lambda i: labels[i]
            )
            loc = loc_results[pick]
            try:
                w = _fetch_weather(float(loc["latitude"]), float(loc["longitude"]))
                st.session_state["last_weather"] = w
                temp_c = w.get("temperature_c")
                st.metric(label="Temperature", value=f"{temp_c} °C" if temp_c is not None else "N/A")
                st.write(f"**Condition:** {w.get('condition', 'Unknown')}  ")
                if w.get("rain_probability_pct") is not None:
                    st.write(f"**Chance of rain (this hour):** {w['rain_probability_pct']}%")
                if w.get("humidity_pct") is not None:
                    st.write(f"**Humidity:** {w['humidity_pct']}%")
                if w.get("wind_kph") is not None:
                    st.write(f"**Wind:** {w['wind_kph']} km/h")
                st.caption(f"As of: {w.get('asof')}")
            except Exception as e:
                msg = str(e)
                if "HTTP Error 429" in msg or "429" in msg:
                    st.warning(
                        "Weather fetch failed due to rate limiting (HTTP 429). "
                        "Wait a minute and click 'Refresh weather' to try again."
                    )
                else:
                    st.warning(f"Weather fetch failed: {e}")

    # --- Soil Moisture ---
    st.subheader("Soil Moisture 🌱")
    source = st.selectbox(
        "Moisture source",
        ["Database (last saved)", "Sensor URL (HTTP JSON)", "Manual (save to DB)"],
    )

    moisture_val: float | None = None
    moisture_source: str | None = None
    moisture_ts: str | None = None

    if source.startswith("Database"):
        latest = database.get_latest_soil_moisture_reading(st.session_state.email, crop=crop)
        if latest:
            moisture_val = float(latest["moisture_pct"])
            moisture_source = str(latest["source"])
            moisture_ts = str(latest["created_at"])
        else:
            st.info("No saved soil moisture readings yet. Use Manual or Sensor URL to add one.")

    elif source.startswith("Sensor"):
        default_url = os.environ.get("SOIL_MOISTURE_URL", "http://localhost:5000/moisture")
        sensor_url = st.text_input("Sensor endpoint URL", default_url)
        st.caption(
            "Expected JSON examples: "
            "`{\"moisture_pct\": 42}` or `{\"moisture\": 0.42}` (fraction), "
            "or Arduino ADC style `{\"adc\": 650, \"wet_raw\": 300, \"dry_raw\": 800}`."
        )
        if st.button("Fetch sensor reading"):
            try:
                moisture_val = float(weather.fetch_sensor_moisture(sensor_url))
                moisture_source = f"sensor:{sensor_url}"
                database.add_soil_moisture_reading(
                    st.session_state.email, crop, moisture_val, moisture_source
                )
                moisture_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.success("Saved sensor reading to database.")
            except Exception as e:
                st.error(f"Sensor fetch failed: {e}")

    else:  # Manual
        latest = database.get_latest_soil_moisture_reading(st.session_state.email, crop=crop)
        default_moist = int(round(float(latest["moisture_pct"]))) if latest else 45
        moisture_val = float(st.slider("Soil moisture (%)", 0, 100, int(default_moist)))
        moisture_source = "manual"
        if st.button("Save reading"):
            database.add_soil_moisture_reading(
                st.session_state.email, crop, moisture_val, moisture_source
            )
            moisture_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success("Saved reading.")

    if moisture_val is not None:
        st.progress(int(round(moisture_val)))
        st.write(f"**Moisture:** {moisture_val:.1f}%")
        if moisture_source:
            st.caption(f"Source: {moisture_source}")
        if moisture_ts:
            st.caption(f"Saved/As of: {moisture_ts}")
        st.session_state["last_moisture_val"] = float(moisture_val)
        st.session_state["last_moisture_ts"] = moisture_ts
        st.session_state["last_moisture_source"] = moisture_source

        if moisture_val < 30:
            st.warning("Soil is dry — consider irrigation or mulching.")
        elif moisture_val > 80:
            st.info("Soil moisture is high — check drainage.")
        else:
            st.success("Soil moisture is in a healthy range.")

    # --- Quick Tips ---
    st.subheader("Quick Farming Tips 🚜")
    st.markdown("- Rotate crops to maintain soil health.\n- Use organic compost where possible.\n- Monitor weather forecasts and irrigate accordingly.")

    # --- Final Review / Report ---
    st.subheader("Final Review ✅")
    st.caption(
        "Generate a detailed review for the selected crop using your saved data (soil moisture readings, questions asked, timeline, and hazards)."
    )

    if "final_review_html" not in st.session_state:
        st.session_state.final_review_html = None

    if st.button("Generate detailed review", type="primary"):
        with st.spinner("Generating your final review..."):
            recent = database.get_recent_soil_moisture_readings(
                st.session_state.email, crop=crop, limit=8
            )
            moisture_recent = [
                reporting.MoistureReading(
                    moisture_pct=float(r["moisture_pct"]),
                    created_at=str(r.get("created_at") or ""),
                    source=str(r.get("source") or ""),
                )
                for r in recent
            ]

            last_weather = st.session_state.get("last_weather")
            weather_snap = None
            if isinstance(last_weather, dict):
                weather_snap = reporting.WeatherSnapshot(
                    temperature_c=(
                        float(last_weather["temperature_c"])
                        if last_weather.get("temperature_c") is not None
                        else None
                    ),
                    humidity_pct=(
                        float(last_weather["humidity_pct"])
                        if last_weather.get("humidity_pct") is not None
                        else None
                    ),
                    wind_kph=(
                        float(last_weather["wind_kph"])
                        if last_weather.get("wind_kph") is not None
                        else None
                    ),
                    rain_probability_pct=(
                        int(last_weather["rain_probability_pct"])
                        if last_weather.get("rain_probability_pct") is not None
                        else None
                    ),
                    condition=str(last_weather.get("condition") or ""),
                    asof=str(last_weather.get("asof") or ""),
                )

            assistant_questions = []
            for role, msg in st.session_state.get("assistant_history", []):
                if role == "user":
                    assistant_questions.append(str(msg))

            latest_moisture = st.session_state.get("last_moisture_val")
            if latest_moisture is None:
                latest_row = database.get_latest_soil_moisture_reading(
                    st.session_state.email, crop=crop
                )
                if latest_row:
                    latest_moisture = float(latest_row["moisture_pct"])

            harvest_date_for_report = None
            try:
                harvest_date_for_report = harvest_date.date()
            except Exception:
                harvest_date_for_report = None

            st.session_state.final_review_html = reporting.build_final_review_html(
                email=st.session_state.email,
                crop=crop,
                crop_info=info,
                location_query=st.session_state.get("location_query"),
                planting_date=planting_date if "planting_date" in locals() else None,
                harvest_date=harvest_date_for_report,
                harvest_days=int(harvest_days) if harvest_days else None,
                moisture_recent=moisture_recent,
                latest_moisture=float(latest_moisture) if latest_moisture is not None else None,
                assistant_questions=assistant_questions,
                weather=weather_snap,
            )

    if st.session_state.final_review_html:
        st.markdown(st.session_state.final_review_html, unsafe_allow_html=True)

# --- App flow ---
if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()
