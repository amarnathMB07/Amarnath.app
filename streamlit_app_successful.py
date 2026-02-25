import streamlit as st
import random
from datetime import datetime, timedelta

# database helpers initialize on import
import database

database.init_db()

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
