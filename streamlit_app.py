import streamlit as st
import random
from datetime import datetime, timedelta

# Page config must be set after importing streamlit
st.set_page_config(page_title="AgroSmart", page_icon="🌾", layout="centered")

# --- Styles (green / natural theme) ---
st.markdown(
    """
    <style>
    .reportview-container { background: linear-gradient(#f7fff7, #eaf8eb); }
    .stApp { color: #034d23; }
    .stButton>button { background-color: #2e7d32; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session state defaults ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ''

# --- Dummy credentials ---
HARD_CODED_EMAIL = "farmer@example.com"
HARD_CODED_PASSWORD = "harvest123"


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

def show_login():
    st.title("AgroSmart 🌱 — Farm Dashboard")
    st.write("Welcome — please log in to continue.")

    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Basic validation
        if not email or not password:
            st.error("Please enter both email and password.")
            return
        # Dummy authentication
        if email == HARD_CODED_EMAIL and password == HARD_CODED_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success("Login successful — redirecting to dashboard...")
            _safe_rerun()
        else:
            st.error("Invalid credentials. Try: farmer@example.com / harvest123")

def show_dashboard():
    st.sidebar.title("AgroSmart 🌾")
    st.sidebar.write("Green insights for your farm")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.email = ''
        _safe_rerun()

    st.header(f"Welcome, {st.session_state.email} 🌿")
    st.caption(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- Crop Information ---
    st.subheader("Crop Information 🌾")
    crop = st.selectbox("Select a crop", ["Wheat", "Corn", "Rice", "Tomato", "Soybean"])

    # user inputs
    st.text_input("Soil type (e.g. loam, clay, sandy)", key="soil_type")
    st.text_input("Fertilizer currently used", key="fertilizer_used")

    crop_db = {
        "Wheat": {"temp": "10-25", "water": "Moderate", "harvest": "120 days"},
        "Corn": {"temp": "18-27", "water": "High", "harvest": "90-120 days"},
        "Rice": {"temp": "20-35", "water": "Very high", "harvest": "120-150 days"},
        "Tomato": {"temp": "18-27", "water": "Moderate", "harvest": "60-85 days"},
        "Soybean": {"temp": "15-30", "water": "Moderate", "harvest": "80-120 days"},
    }

    info = crop_db.get(crop, {})
    st.write(f"**Optimal Temperature (°C):** {info.get('temp')}")
    st.write(f"**Water Requirement:** {info.get('water')}")
    st.write(f"**Typical Harvest Time:** {info.get('harvest')}")

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

    # helper data
    season_db = {
        "Wheat": "Winter/Spring",
        "Corn": "Spring/Summer",
        "Rice": "Summer/Monsoon",
        "Tomato": "Summer",
        "Soybean": "Summer",
    }
    fertilizer_db = {
        "Wheat": "Nitrogen-rich (urea) and phosphate fertilizers.",
        "Corn": "Balanced NPK with extra nitrogen.",
        "Rice": "Organic compost plus urea or DAP.",
        "Tomato": "High potassium and phosphorus fertilizers.",
        "Soybean": "Legume inoculants and low nitrogen (fixes its own).",
    }

    def parse_days(text):
        # expect something like '120 days' or '90-120 days'
        try:
            parts = text.split()[0]
            if '-' in parts:
                return int(parts.split('-')[0])
            return int(parts)
        except Exception:
            return None

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
        recommended = fertilizer_db.get(crop, "Use a balanced NPK fertilizer and adjust based on soil test.")
        used = st.session_state.get("fertilizer_used", "none")
        answer = f"Recommended: {recommended}  (you entered: {used})"
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
        soil = st.session_state.get("soil_type", "unspecified")
        answer = (
            f"Suitability depends on your soil type ({soil}), moisture and climate. "
            "If you can meet its temperature and water needs, it should be okay."
        )
    elif q == "What is the growth duration of this crop?":
        answer = info.get('harvest')
    elif q == "How many days to harvest?":
        days = parse_days(info.get('harvest',''))
        answer = f"Approximately {days} days." if days else "N/A"

    if answer:
        st.info(answer)

    # --- Harvest flowchart ---
    st.subheader("Harvest timeline 📅")
    harvest_days = parse_days(info.get('harvest', '')) or 0
    planting_date = datetime.now()
    harvest_date = planting_date + timedelta(days=harvest_days)
    chart = (
        f"Planting ({planting_date.strftime('%Y-%m-%d')}) → "
        f"Harvest (~{harvest_date.strftime('%Y-%m-%d')})"
    )
    # display as code block to preserve formatting
    st.code(chart)

    # --- Weather Status ---
    st.subheader("Weather Status ☀️🌧️")
    temp = random.randint(12, 36)
    condition = random.choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Stormy"])
    rain_prob = random.randint(0, 100)

    st.metric(label="Temperature", value=f"{temp} °C", delta=f"{random.randint(-2,3)}°")
    st.write(f"**Condition:** {condition}  ")
    st.write(f"**Chance of rain:** {rain_prob}%")

    # --- Soil Moisture ---
    st.subheader("Soil Moisture 🌱")
    default_moist = random.randint(25, 65)
    moisture = st.slider("Soil moisture (%)", 0, 100, default_moist)
    st.progress(moisture)

    if moisture < 30:
        st.warning("Soil is dry — consider irrigation or mulching.")
    elif moisture > 80:
        st.info("Soil moisture is high — check drainage.")
    else:
        st.success("Soil moisture is in a healthy range.")

    # --- Quick Tips ---
    st.subheader("Quick Farming Tips 🚜")
    st.markdown("- Rotate crops to maintain soil health.\n- Use organic compost where possible.\n- Monitor weather forecasts and irrigate accordingly.")

# --- App flow ---
if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()
