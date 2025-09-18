# ======================================================================
# 🎟️ EVENT REGISTRATION SYSTEM — Streamlit Edition (ULTIMATE)
# QR Tickets • Voice Guidance • Waitlists • Multi-Currency • Social Share
# Designed for scale, safety, and cinematic UX.
# ======================================================================

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
from typing import Optional, Tuple
import os
import time
import secrets
from urllib.parse import urlparse
from dotenv import load_dotenv
import qrcode
from io import BytesIO
import base64
from textwrap import dedent

import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("se.png")

st.markdown(
    f"""
    <h2 class="main-header">
        <center>  <img src="data:image/png;base64,{logo_base64}" width="40" style="vertical-align: middle; margin-left:5px;"></center>
           <center> Social Eagle Python Challenge </center>
        <center> Day 10 - Event Registration</center>
    </h2>
    """,
    unsafe_allow_html=True
)

# Load environment variables from .env file
load_dotenv()

# Admin password: reads from .env → fallback to "admin123"
ADMIN_PASSWORD = os.getenv("ADMIN_PASS", "admin123")

# CSV filenames
EVENTS_CSV = "events.csv"
REGS_CSV = "registrations.csv"
WAITLIST_CSV = "waitlist.csv"

# Auto-refresh interval for live stats (ms)
AUTO_REFRESH_INTERVAL = 3000

# Currency rates (base: USD)
CURRENCY_RATES = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.93
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "INR": "₹",
    "EUR": "€"
}

# ======================================================================
# 🎨 FUTURISTIC THEME + ANIMATED BACKGROUND
# ======================================================================

st.set_page_config(
    page_title="Hyperlane Events 🪐",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Animated starfield background
# Add custom CSS via st.css() (if available) or inject only necessary styles
st.markdown("""
<style>
    .stApp {
        background: #0a0a1a;
        color: #e0e0ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 15px);
        background-size: 150px 150px;
        background-position: 0 0, 75px 75px;
        animation: drift 75s linear infinite;
        pointer-events: none;
        z-index: -1;
        opacity: 0.3;
    }
    @keyframes drift {
        from { background-position: 0 0, 75px 75px; }
        to { background-position: 150px 150px, 225px 225px; }
    }


    /* Headings — neon cyan */
    h1, h2, h3, h4, h5 {
        background: linear-gradient(90deg, #00ffff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
        font-weight: 700;
    }

    /* Metric labels — electric purple */
    .stMetricLabel > div {
        color: #d480ff !important;
        font-weight: 600;
    }

    /* Metric values — bright cyan */
    .stMetricValue {
        color: #00ffff !important;
        text-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
        font-size: 1.4rem !important;
    }

    /* Buttons — glowing edges */
    .stButton > button {
        background: linear-gradient(135deg, #1e1e3a, #2a2a55);
        color: #00ffff;
        border: 1px solid #00aaff;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.6);
        transform: translateY(-2px);
    }

    /* Inputs — cyber terminal style */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(15, 15, 30, 0.7);
        color: #e0e0ff;
        border: 1px solid #00aaff;
        box-shadow: inset 0 0 8px rgba(0, 170, 255, 0.2);
        border-radius: 8px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 25, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 200, 255, 0.2);
    }

    /* Expander headers */
    .streamlit-expanderHeader {
        background: rgba(20, 20, 45, 0.6) !important;
        border: 1px solid rgba(0, 200, 255, 0.3) !important;
        border-radius: 8px !important;
    }

    /* Warning banners — urgency glow */
    .stAlert[data-baseweb="alert"] {
        background: rgba(40, 20, 60, 0.8);
        border: 1px solid #ff3366;
        box-shadow: 0 0 15px rgba(255, 51, 102, 0.4);
    }

    /* Success banners — quantum green */
    .stAlert + .stAlert {
        border-color: #00ffaa;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.4);
    }

    /* Data editor headers */
    .stDataFrame thead tr th {
        background: rgba(0, 50, 80, 0.8) !important;
        color: #00ffff !important;
        font-weight: 600;
    }

    /* Progress bar — neon energy */
    .stProgress > div > div {
        background: linear-gradient(90deg, #ff00ff, #00ffff) !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }

    /* Links */
    a {
        color: #FFFFFF !important;
        text-decoration: none;
        border-bottom: 1px dashed #00aaff;
    }
    a:hover {
        color: #00ffff !important;
        text-shadow: 0 0 8px rgba(0, 255, 255, 0.8);
    }

    /* QR Code container */
    .qr-container {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }

    /* Social share buttons */
    .share-buttons {
        display: flex;
        gap: 10px;
        margin: 1rem 0;
        flex-wrap: wrap;
        justify-content: center;
    }
    .share-btn {
        padding: 8px 16px;
        border-radius: 8px;
        color: black;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .share-btn.whatsapp { background: #25D366; }
    .share-btn.twitter { background: #1DA1F2; }
    .share-btn.linkedin { background: #0077B5; }
    .share-btn:hover { transform: translateY(-2px); opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# ======================================================================
# 📦 DATA SCHEMAS & INITIALIZERS
# ======================================================================

def parse_datetime_columns(df: pd.DataFrame, datetime_cols: list) -> pd.DataFrame:
    """Convert specified columns from string to datetime."""
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def init_events_df() -> pd.DataFrame:
    """Seed with sample events if no CSV exists."""
    df = pd.DataFrame([
        {
            "id": "evt_galactic_keynote",
            "name": "Galactic Keynote: Future of AI",
            "banner_url": "https://placehold.co/800x300/1a1a2e/ffffff?text=Galactic+Keynote",
            "start_at": datetime.datetime.now() + datetime.timedelta(hours=2),
            "end_at": datetime.datetime.now() + datetime.timedelta(hours=4),
            "capacity": 10,
            "price": 99.99,
            "offer_type": "flash",
            "offer_value": 20,
            "offer_start": datetime.datetime.now(),
            "offer_end": datetime.datetime.now() + datetime.timedelta(hours=1),
            "active": True
        },
        {
            "id": "evt_quantum_workshop",
            "name": "Quantum Workshop: Hands-On Entanglement",
            "banner_url": "https://placehold.co/800x300/16213e/ffffff?text=Quantum+Workshop",
            "start_at": datetime.datetime.now() + datetime.timedelta(days=1),
            "end_at": datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
            "capacity": 15,
            "price": 75.00,
            "offer_type": "early",
            "offer_value": 15,
            "offer_start": datetime.datetime.now(),
            "offer_end": datetime.datetime.now() + datetime.timedelta(hours=24),
            "active": True
        }
    ])
    datetime_cols = ["start_at", "end_at", "offer_start", "offer_end"]
    df = parse_datetime_columns(df, datetime_cols)
    return df

def init_regs_df() -> pd.DataFrame:
    return pd.DataFrame(columns=["ts", "name", "email", "event_id", "price_paid", "offer_applied", "currency"])

def init_waitlist_df() -> pd.DataFrame:
    return pd.DataFrame(columns=["ts", "name", "email", "event_id", "notified"])

# ======================================================================
# 💾 PERSISTENCE UTILS
# ======================================================================

@st.cache_data(ttl=10)
def load_csv(filename: str, default_df: pd.DataFrame) -> pd.DataFrame:
    try:
        df = pd.read_csv(filename)
        datetime_cols = ["start_at", "end_at", "offer_start", "offer_end", "ts"]
        df = parse_datetime_columns(df, datetime_cols)
        return df
    except FileNotFoundError:
        default_df.to_csv(filename, index=False)
        return default_df.copy()

def save_csv(df: pd.DataFrame, filename: str):
    df.to_csv(filename, index=False)

# ======================================================================
# 🧠 STATE INITIALIZATION
# ======================================================================

if "EVENTS" not in st.session_state:
    st.session_state.EVENTS = load_csv(EVENTS_CSV, init_events_df())

if "REGS" not in st.session_state:
    st.session_state.REGS = load_csv(REGS_CSV, init_regs_df())

if "WAITLIST" not in st.session_state:
    st.session_state.WAITLIST = load_csv(WAITLIST_CSV, init_waitlist_df())

if "INVENTORY" not in st.session_state:
    st.session_state.INVENTORY = {
        row["id"]: {"taken_seats": 0, "lock_until_ts": None}
        for _, row in st.session_state.EVENTS.iterrows()
    }
    for event_id in st.session_state.INVENTORY.keys():
        taken = len(st.session_state.REGS[st.session_state.REGS["event_id"] == event_id])
        st.session_state.INVENTORY[event_id]["taken_seats"] = taken

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "Home"

if "selected_currency" not in st.session_state:
    st.session_state.selected_currency = "INR"

if "voice_guidance_enabled" not in st.session_state:
    st.session_state.voice_guidance_enabled = False

# ======================================================================
# 🧮 BUSINESS LOGIC UTILS
# ======================================================================

def is_url_valid(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def normalize_email(email: str) -> str:
    return email.strip().lower()

def seats_remaining(event_id: str) -> int:
    event = st.session_state.EVENTS[st.session_state.EVENTS["id"] == event_id].iloc[0]
    taken = st.session_state.INVENTORY[event_id]["taken_seats"]
    return max(0, event["capacity"] - taken)

def is_event_locked(event_id: str) -> bool:
    lock_until = st.session_state.INVENTORY[event_id]["lock_until_ts"]
    if lock_until is None:
        return False
    return datetime.datetime.now() < lock_until

def acquire_lock(event_id: str, duration_sec: int = 3) -> bool:
    if is_event_locked(event_id):
        return False
    st.session_state.INVENTORY[event_id]["lock_until_ts"] = (
        datetime.datetime.now() + datetime.timedelta(seconds=duration_sec)
    )
    return True

def release_lock(event_id: str):
    st.session_state.INVENTORY[event_id]["lock_until_ts"] = None

def convert_price(price_usd: float, currency: str = "INR") -> float:
    rate = CURRENCY_RATES.get(currency, 1.0)
    return price_usd * rate

def apply_offer(event: pd.Series, now: datetime.datetime, seats_left: int) -> Tuple[float, Optional[str]]:
    base_price = event["price"]
    offer_name = None

    if pd.isna(event["start_at"]) or not isinstance(event["start_at"], datetime.datetime):
        return base_price, None

    if event["offer_type"] == "flash":
        time_to_start = (event["start_at"] - now).total_seconds()
        if time_to_start < 3600 and seats_left <= 5:
            discount = base_price * (event["offer_value"] / 100)
            return base_price - discount, "Flash Sale! ⚡"

    elif event["offer_type"] == "early":
        if not (pd.isna(event["offer_start"]) or pd.isna(event["offer_end"])):
            if event["offer_start"] <= now <= event["offer_end"]:
                discount = base_price * (event["offer_value"] / 100)
                return base_price - discount, "Early Bird 🐦"

    return base_price, None

def validate_registration_form(name: str, email: str, event_ids: list) -> Tuple[bool, str]:
    if not name.strip():
        return False, "Name is required."
    if not email.strip() or "@" not in email:
        return False, "Valid email is required."
    if not event_ids:
        return False, "Select at least one event."
    return True, ""

def atomic_register(name: str, email: str, event_ids: list, currency: str = "INR") -> Tuple[bool, str]:
    now = datetime.datetime.now()
    email_norm = normalize_email(email)
    success_events = []
    waitlist_events = []

    for event_id in event_ids:
        event_mask = (st.session_state.EVENTS["id"] == event_id) & (st.session_state.EVENTS["active"])
        if not event_mask.any():
            continue

        event = st.session_state.EVENTS[event_mask].iloc[0]

        if not acquire_lock(event_id):
            continue

        try:
            seats_left = seats_remaining(event_id)

            dup_mask = (
                (st.session_state.REGS["email"] == email_norm) &
                (st.session_state.REGS["event_id"] == event_id)
            )
            if dup_mask.any():
                continue

            final_price_usd, offer_name = apply_offer(event, now, seats_left)
            final_price = convert_price(final_price_usd, currency)

            if seats_left > 0:
                st.session_state.INVENTORY[event_id]["taken_seats"] += 1

                new_reg = pd.DataFrame([{
                    "ts": now.isoformat(timespec="seconds"),
                    "name": name.strip(),
                    "email": email_norm,
                    "event_id": event_id,
                    "price_paid": final_price,
                    "offer_applied": offer_name or "None",
                    "currency": currency
                }])

                st.session_state.REGS = pd.concat([st.session_state.REGS, new_reg], ignore_index=True)
                save_csv(st.session_state.REGS, REGS_CSV)
                success_events.append(event["name"])

            else:
                # Add to waitlist
                new_waitlist = pd.DataFrame([{
                    "ts": now.isoformat(timespec="seconds"),
                    "name": name.strip(),
                    "email": email_norm,
                    "event_id": event_id,
                    "notified": False
                }])
                st.session_state.WAITLIST = pd.concat([st.session_state.WAITLIST, new_waitlist], ignore_index=True)
                save_csv(st.session_state.WAITLIST, WAITLIST_CSV)
                waitlist_events.append(event["name"])

        finally:
            release_lock(event_id)

    messages = []
    if success_events:
        messages.append(f"✅ Registered for: {', '.join(success_events)}!")
    if waitlist_events:
        messages.append(f"⏳ Added to waitlist for: {', '.join(waitlist_events)} — we'll notify you if seats open!")

    if messages:
        return True, " ".join(messages)
    else:
        return False, "❌ Registration failed. Please try again."

# ✅ FIXED: Added missing parameter name 'data'
def generate_qr_code(data: str) -> bytes:
    """Generate QR code and return as PNG bytes."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#00ffff", back_color="#0a0a1a")
    
    # Convert PIL Image to bytes
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

# ======================================================================
# 🎙️ VOICE GUIDANCE COMPONENT
# ======================================================================

VOICE_GUIDANCE_SCRIPT = """
<script>
let speechSynthesis = window.speechSynthesis;
let voices = [];

function populateVoices() {
    voices = speechSynthesis.getVoices();
}

function speak(text) {
    if (!speechSynthesis) return;
    if (voices.length === 0) {
        populateVoices();
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1.1;
    if (voices.length > 0) {
        utterance.voice = voices.find(v => v.lang.includes('en')) || voices[0];
    }
    speechSynthesis.speak(utterance);
}

// Load voices
if (speechSynthesis && speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = populateVoices;
}
populateVoices();

// Expose to window
window.speakGuidance = speak;
</script>
"""

def render_voice_guidance():
    """Render voice guidance toggle and inject script."""
    st.markdown(VOICE_GUIDANCE_SCRIPT, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3,1])
    with col1:
        st.caption("🎙️ Enable Voice Guidance for immersive registration")
    with col2:
        voice_on = st.toggle("Voice ON", value=st.session_state.voice_guidance_enabled, key="voice_toggle")
        st.session_state.voice_guidance_enabled = voice_on

    if st.session_state.voice_guidance_enabled:
        st.markdown("""
        <script>
        if (window.speakGuidance) {
            window.speakGuidance("Welcome to Hyperlane Events. Select an event to begin your quantum journey.");
        }
        </script>
        """, unsafe_allow_html=True)

# ======================================================================
# 🎨 UI COMPONENTS
# ======================================================================

def render_event_banner(event: pd.Series):
    banner_url = event["banner_url"]
    if not is_url_valid(banner_url):
        st.markdown(
            f"""
            <div style="
                height: 120px;
                background: linear-gradient(135deg, #6e45e2 0%, #88d3ce 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 1.5rem;
                font-weight: bold;
                border-radius: 8px;
                margin: 10px 0;
            ">
                {event['name']}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.image(banner_url, use_container_width=True)

def render_urgency_badge(event: pd.Series, seats_left: int):
    now = datetime.datetime.now()
    if pd.isna(event["start_at"]) or not isinstance(event["start_at"], datetime.datetime):
        time_to_start = float('inf')
    else:
        time_to_start = (event["start_at"] - now).total_seconds()

    cols = st.columns([1, 3])
    with cols[0]:
        if seats_left <= 5 and seats_left > 0:
            st.warning(f"Only {seats_left} left! ⚡", icon="🚨")
        elif seats_left == 0:
            st.error("Sold out", icon="⛔")
    with cols[1]:
        if 0 < time_to_start < 3600:
            mins = int(time_to_start // 60)
            st.error(f"Starts in {mins} min → Flash offer active! 🕒", icon="⏳")
        elif time_to_start < 0:
            st.info("Event started", icon="🎯")

def render_offer_banner(event: pd.Series, seats_left: int):
    now = datetime.datetime.now()
    _, offer_name = apply_offer(event, now, seats_left)
    if offer_name:
        st.success(f"✨ {offer_name} — Warp-speed deal unlocked!", icon="🚀")



# def render_social_share(event_name: str, event_id: str):
#     """Render social share buttons."""
#     share_text = f"Join me at '{event_name}' on Hyperlane Events! Secure your quantum slot before spacetime folds. #HyperlaneEvents #FutureTech"
#     encoded_text = share_text.replace(" ", "%20")
    
#     whatsapp_url = f"https://wa.me/?text={encoded_text}"
#     twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
#     linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://hyperlane.events/{event_id}"
    
#     st.markdown(f"""
#     <div class="share-buttons">
#         <a href="{whatsapp_url}" target="_blank" class="share-btn whatsapp">WhatsApp</a>
#         <a href="{twitter_url}" target="_blank" class="share-btn twitter">Twitter/X</a>
#         <a href="{linkedin_url}" target="_blank" class="share-btn linkedin">LinkedIn</a>
#     </div>
#     """, unsafe_allow_html=True)
 
def render_social_share(event_name: str, event_id: str):
    st.caption("✨ Share this event with your crew")   
   # """Render social share buttons with official brand icons."""
    share_text = f"Join me at '{event_name}' on Hyperlane Events! Secure your quantum slot before spacetime folds. #HyperlaneEvents #FutureTech"
    encoded_text = share_text.replace(" ", "%20")
    
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
    linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://hyperlane.events/{event_id}"
    
    st.markdown(f"""
    <style>
    .share-btn svg {{
        vertical-align: middle;
        margin-right: 6px;
        width: 18px;
        height: 18px;
    }}
    </style>
    <div class="share-buttons">
        <a href="{whatsapp_url}" target="_blank" class="share-btn whatsapp">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.047 24l6.305-1.654a11.882 11.882 0 005.693 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413" />
            </svg>
            WhatsApp
        </a>
        <a href="{twitter_url}" target="_blank" class="share-btn twitter">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723 10.054 10.054 0 01-3.127 1.184 4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.937 4.937 0 004.604 3.417 9.868 9.868 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.054 0 13.999-7.496 13.999-13.986 0-.209 0-.42-.015-.63a9.936 9.936 0 002.46-2.548" />
            </svg>
            Twitter/X
        </a>
        <a href="{linkedin_url}" target="_blank" class="share-btn linkedin">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
            LinkedIn
        </a>
    </div>
    """, unsafe_allow_html=True)


# ======================================================================
# 🖥️ UI PAGES
# ======================================================================

def render_homepage_tab():
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 0;'>🚀 HYPERLANE EVENTS</h1>
        <p style='font-size: 1.2rem; color: #aaaaff; max-width: 800px; margin: 1rem auto;'>
            Where quantum thinkers, AI pioneers, and cosmic creators collide.
            Reserve your seat before spacetime folds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Currency selector
    st.markdown("### 💱 Select Currency")
    currency = st.radio(
        "Currency",
        options=list(CURRENCY_SYMBOLS.keys()),
        horizontal=True,
        label_visibility="collapsed",
        index=list(CURRENCY_SYMBOLS.keys()).index(st.session_state.selected_currency)
    )
    st.session_state.selected_currency = currency

    if st.session_state.EVENTS.empty:
        st.info("No events scheduled. The void awaits...")
        return

    for _, event in st.session_state.EVENTS.iterrows():
        if not event["active"]:
            continue

        event_id = event["id"]
        seats_left = seats_remaining(event_id)
        now = datetime.datetime.now()

        price_display = convert_price(event["price"], st.session_state.selected_currency)
        final_price_usd, offer_name = apply_offer(event, now, seats_left)
        final_price_display = convert_price(final_price_usd, st.session_state.selected_currency)
        symbol = CURRENCY_SYMBOLS[st.session_state.selected_currency]

        with st.container():
            render_event_banner(event)
            render_social_share(event["name"], event_id)

            #chatgpt code below
            if event_id == "evt_galactic_keynote":
                price_display_str = f"{price_display:,.0f}"
                final_price_display_str = f"{final_price_display:,.0f}"
                offer_str = f" — {offer_name}" if offer_name else ""
                html_galactic = """

<div style='background: rgba(20, 20, 50, 0.6); padding: 1.5rem; border-radius: 12px; border: 1px solid #00aaff; margin: 1rem 0;'>
    <!-- YouTube Video (Hover to Play) -->
    <div id="yt-hover-galactic" style="position: relative; width: 100%; aspect-ratio: 16/9; overflow: hidden; border-radius: 8px; box-shadow: 0 0 15px rgba(0, 255, 255, 0.3); cursor: pointer;">
        <iframe 
            id="ytplayer-galactic"
            src="https://www.youtube.com/embed/5IvQ3fYKnfM?enablejsapi=1&rel=0&showinfo=0&modestbranding=1"
            title="The Future of Artificial Intelligence"
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;">
        </iframe>

        <!-- Optional: subtle hover hint -->
        <div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; pointer-events:none;">
            <div style="background:rgba(0,0,0,0.25); padding:6px 10px; border-radius:8px; font-size:0.9rem; color:#e0e0ff;">
                Hover to play • Move away to pause
            </div>
        </div>
    </div>

    <!-- Description Below Video -->
    <div style='font-size: 1.1rem; line-height: 1.6; color: #e0e0ff; margin-top: 1rem;'>
        You’ve been selected. The Galactic Council of AI has convened for the first time in 300 years.
        Witness the unveiling of Sentient Model Ω — the last AI before the Singularity.
        Seats are quantum-entangled. Only [[SEATS_LEFT]] remain in this spacetime.
    </div>

    <!-- Price -->
    <div style='color: #ff9900; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; margin-top: 1rem;'>
        <span style="color: #00ffff;">⚡</span>
        <span>Investment: <s>[[SYMBOL]][[PRICE_DISPLAY]]</s> → <span style='color: #00ffaa; font-size: 1.2em;'>[[SYMBOL]][[FINAL_PRICE_DISPLAY]]</span></span>
        [[OFFER_STR]]
    </div>
</div>

<!-- Load YouTube API once -->
<script>
  (function loadYT() {
    if (window.__yt_api_loading || window.YT) return;
    window.__yt_api_loading = true;
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    document.head.appendChild(tag);
  })();
</script>

<script>
  // Keep state across reruns
  window.__yt_players = window.__yt_players || {};

  function createOrGetPlayer(playerId) {
    if (window.__yt_players[playerId]) return window.__yt_players[playerId];
    // Create a placeholder; real YT.Player will attach later when API ready
    window.__yt_players[playerId] = { ready: false, ref: null, queue: [] };
    return window.__yt_players[playerId];
  }

  // YouTube API callback
  window.onYouTubeIframeAPIReady = function() {
    Object.keys(window.__yt_players).forEach(function(id) {
      if (!window.__yt_players[id].ready) {
        var p = new YT.Player(id, {
          events: {
            'onReady': function(e) {
              var obj = window.__yt_players[id];
              obj.ready = true;
              obj.ref = e.target;
              // Apply any queued actions (from early hover)
              obj.queue.forEach(function(fn) { try { fn(obj.ref); } catch(e) {} });
              obj.queue = [];
            }
          }
        });
      }
    });
  };

  // Attach hover handlers
  (function setupHover() {
    var wrapperId = "yt-hover-galactic";
    var playerId  = "ytplayer-galactic";
    var wrapper   = document.getElementById(wrapperId);
    if (!wrapper) return;

    var playerObj = createOrGetPlayer(playerId);

    function withPlayer(fn) {
      if (playerObj.ready && playerObj.ref) {
        try { fn(playerObj.ref); } catch (e) {}
      } else {
        playerObj.queue.push(fn);
      }
    }

    // Play on hover
    wrapper.addEventListener("mouseenter", function() {
      withPlayer(function(p) {
        try { p.playVideo(); } catch(e) {}
      });
    });

    // Pause when mouse leaves
    wrapper.addEventListener("mouseleave", function() {
      withPlayer(function(p) {
        try { p.pauseVideo(); } catch(e) {}
      });
    });
  })();
</script>
"""
                html_galactic = (html_galactic
                                 .lstrip()
                                 .replace('[[SEATS_LEFT]]', str(seats_left))
                                 .replace('[[SYMBOL]]', symbol)
                                 .replace('[[PRICE_DISPLAY]]', price_display_str)
                                 .replace('[[FINAL_PRICE_DISPLAY]]', final_price_display_str)
                                 .replace('[[OFFER_STR]]', offer_str))
                components.html(html_galactic, height=600, scrolling=False)

            elif event_id == "evt_quantum_workshop":
                # Prepare display strings to avoid f-string conflicts in HTML/JS
                price_display_str = f"{price_display:,.0f}"
                final_price_display_str = f"{final_price_display:,.0f}"
                offer_str = f" — {offer_name}" if offer_name else ""

                html_quantum = """
<div style='background: rgba(20, 20, 50, 0.6); padding: 1.5rem; border-radius: 12px; border: 1px solid #00aaff; margin: 1rem 0;'>
  <!-- YouTube Video (Hover to Play) -->
  <div id="yt-hover-quantum" style="position: relative; width: 100%; aspect-ratio: 16/9; overflow: hidden; border-radius: 8px; box-shadow: 0 0 15px rgba(0, 255, 255, 0.3); cursor: pointer;">
      <iframe 
          id="ytplayer-quantum"
          src="https://www.youtube.com/embed/BJykdUpIslc?enablejsapi=1&rel=0&showinfo=0&modestbranding=1"
          title="Quantum Workshop: Hands-On Entanglement"
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          allowfullscreen 
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;">
      </iframe>

      <!-- One-time sound gate (required by autoplay policies) -->
      <div id="yt-sound-gate-quantum" style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; background:rgba(0,0,0,0.35); color:#e0e0ff; font-weight:700; font-size:1rem; cursor:pointer;">
          🔊 Click once to enable sound
      </div>

      <!-- Subtle hover hint -->
      <div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; pointer-events:none;">
          <div style="background:rgba(0,0,0,0.25); padding:6px 10px; border-radius:8px; font-size:0.9rem; color:#e0e0ff;">
              Hover to play • Move away to pause
          </div>
      </div>
  </div>

  <!-- Description -->
  <div style='font-size: 1.1rem; line-height: 1.6; color: #e0e0ff; margin-top: 1rem;'>
      Break causality. Entangle qubits with your bare hands.
      In this zero-gravity lab, you’ll build a quantum circuit that hacks parallel universes.
      Warning: May cause temporary timeline divergence. [[SEATS_LEFT]] slots left before collapse.
  </div>

  <!-- Price -->
  <div style='color: #ff9900; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; margin-top: 1rem;'>
      <span style="color: #00ffff;">⚡</span>
      <span>Investment: <s>[[SYMBOL]][[PRICE_DISPLAY]]</s> → <span style='color: #00ffaa; font-size: 1.2em;'>[[SYMBOL]][[FINAL_PRICE_DISPLAY]]</span></span>
      [[OFFER_STR]]
  </div>
</div>

<!-- Load YouTube API once (safe to include multiple times) -->
<script>
  (function loadYT() {
    if (window.__yt_api_loading || window.YT) return;
    window.__yt_api_loading = true;
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    document.head.appendChild(tag);
  })();
</script>

<script>
  // Shared state/setup (safe if defined elsewhere)
  window.__yt_players = window.__yt_players || {};
  window.__yt_allow_sound = (sessionStorage.getItem('yt_allow_sound') === '1');

  function markUserGesture() {
    try { sessionStorage.setItem('yt_allow_sound', '1'); } catch (e) {}
    window.__yt_allow_sound = true;
    Object.keys(window.__yt_players || {}).forEach(function(id){
      var obj = window.__yt_players[id];
      if (obj && obj.ready && obj.ref && obj.ref.unMute) {
        try { obj.ref.unMute(); } catch(e) {}
      }
    });
  }

  window.addEventListener('click', markUserGesture, { once: false, passive: true });
  window.addEventListener('touchstart', markUserGesture, { once: false, passive: true });

  function createOrGetPlayer(playerId) {
    if (window.__yt_players[playerId]) return window.__yt_players[playerId];
    window.__yt_players[playerId] = { ready: false, ref: null, queue: [] };
    return window.__yt_players[playerId];
  }

  // Chainable API ready hook
  window.onYouTubeIframeAPIReady = (function(prev){
    return function() {
      if (typeof prev === 'function') { try { prev(); } catch(e) {} }
      Object.keys(window.__yt_players).forEach(function(id) {
        if (!window.__yt_players[id].ready) {
          var p = new YT.Player(id, {
            events: {
              'onReady': function(e) {
                var obj = window.__yt_players[id];
                obj.ready = true;
                obj.ref = e.target;
                obj.queue.forEach(function(fn) { try { fn(obj.ref); } catch(e) {} });
                obj.queue = [];
              }
            }
          });
        }
      });
    };
  })(window.onYouTubeIframeAPIReady);

  // Quantum-specific hover wiring
  (function setupHoverQuantum() {
    var wrapperId = "yt-hover-quantum";
    var playerId  = "ytplayer-quantum";
    var wrapper   = document.getElementById(wrapperId);
    if (!wrapper) return;

    var gate = document.getElementById('yt-sound-gate-quantum');
    if (gate) {
      gate.style.display = window.__yt_allow_sound ? 'none' : 'flex';
      gate.addEventListener('click', function () {
        try { markUserGesture(); } catch (e) {}
        gate.style.display = 'none';
        var obj = createOrGetPlayer(playerId);
        if (obj && obj.ready && obj.ref) {
          try { if (obj.ref.unMute) obj.ref.unMute(); } catch(e) {}
          try { obj.ref.playVideo(); } catch(e) {}
        }
      });
    }

    var playerObj = createOrGetPlayer(playerId);

    function withPlayer(fn) {
      if (playerObj.ready && playerObj.ref) {
        try { fn(playerObj.ref); } catch (e) {}
      } else {
        playerObj.queue.push(fn);
      }
    }

    wrapper.addEventListener("mouseenter", function() {
      withPlayer(function(p) {
        try {
          if (!window.__yt_allow_sound && p.mute) { p.mute(); }
          else if (window.__yt_allow_sound && p.unMute) { p.unMute(); }
          p.playVideo();
        } catch(e) {}
      });
    });

    wrapper.addEventListener("mouseleave", function() {
      withPlayer(function(p) {
        try { p.pauseVideo(); } catch(e) {}
      });
    });
  })();
</script>
"""

                html_quantum = (html_quantum
                                .lstrip()
                                .replace('[[SEATS_LEFT]]', str(seats_left))
                                .replace('[[SYMBOL]]', symbol)
                                .replace('[[PRICE_DISPLAY]]', price_display_str)
                                .replace('[[FINAL_PRICE_DISPLAY]]', final_price_display_str)
                                .replace('[[OFFER_STR]]', offer_str))

                components.html(html_quantum, height=600, scrolling=False)
            render_urgency_badge(event, seats_left)
            if offer_name:
                st.success(f"✨ {offer_name} — Temporal discount active!", icon="⏳")

            if seats_left > 0:
                # ✅ FIXED: use_container_width → width="stretch"
                if st.button(f"🔗 SECURE MY QUANTUM SLOT — {symbol}{final_price_display:,.0f}", key=f"home_cta_{event_id}", width="stretch"):
                    st.session_state.selected_event_for_register = event_id
                    st.session_state.nav_to_register = True
                    st.rerun()
            else:
                # ✅ FIXED: use_container_width → width="stretch"
                if st.button(f"⏳ JOIN WAITLIST — {symbol}{final_price_display:,.0f}", key=f"waitlist_{event_id}", width="stretch"):
                    st.session_state.selected_event_for_register = event_id
                    st.session_state.nav_to_register = True
                    st.rerun()

            st.divider()

#STARTOFBLOCKER
        
                #ENDOFBLOCKR
    if "nav_to_register" in st.session_state and st.session_state.nav_to_register:
        st.session_state.nav_to_register = False
        st.session_state.selected_tab = "Register"
        st.rerun()

def render_register_tab():
    st.header("🚀 Hyperlane to Checkout")
    render_voice_guidance()

    currency = st.session_state.selected_currency
    symbol = CURRENCY_SYMBOLS[currency]

    active_events = st.session_state.EVENTS[st.session_state.EVENTS["active"]].copy()
    if active_events.empty:
        st.info("No active events. Check back later or contact admin.")
        return

    event_options = {}
    for _, event in active_events.iterrows():
        event_id = event["id"]
        seats_left = seats_remaining(event_id)
        now = datetime.datetime.now()

        with st.container():
            render_event_banner(event)
            render_offer_banner(event, seats_left)
            render_urgency_badge(event, seats_left)

            final_price_usd, _ = apply_offer(event, now, seats_left)
            final_price_display = convert_price(final_price_usd, currency)
            st.markdown(f"**{symbol}{final_price_display:,.0f}** • {event['start_at'].strftime('%a, %b %d @ %I:%M %p')}")
            st.divider()

        if seats_left > 0:
            event_options[event["name"]] = event_id

    if not event_options:
        st.warning("All events are currently sold out. You can still join the waitlist!")
        return

    with st.form("registration_form", clear_on_submit=True):
        name = st.text_input("Your Name ✍️", placeholder="Alex Rivera")
        email = st.text_input("Email Address 📧", placeholder="alex@hyperlane.dev")
        selected_events = st.multiselect(
            "Choose Events 🎟️",
            options=list(event_options.keys()),
            format_func=lambda x: f"{x} (Seats left: {seats_remaining(event_options[x])})"
        )

        # ✅ FIXED: use_container_width → width="stretch"
        submitted = st.form_submit_button("WARP SPEED REGISTER 🚀", width="stretch")

        if submitted:
            event_ids = [event_options[name] for name in selected_events]
            is_valid, msg = validate_registration_form(name, email, event_ids)
            if not is_valid:
                st.error(msg)
            else:
                with st.spinner("Reserving your seat in the quantum realm..."):
                    success, msg = atomic_register(name, email, event_ids, currency)
                    if success:
                        st.balloons()
                        st.success(msg)
                        
                        if st.session_state.voice_guidance_enabled:
                            st.markdown(f"""
                            <script>
                            if (window.speakGuidance) {{
                                window.speakGuidance("Registration successful! Check your tickets tab for QR codes.");
                            }}
                            </script>
                            """, unsafe_allow_html=True)
                    else:
                        st.error(msg)

def render_my_tickets_tab():
    st.header("🎫 My Quantum Tickets")
    email = st.text_input("Enter your email to view tickets", placeholder="alex@hyperlane.dev")
    
    if not email.strip():
        st.info("Enter your email to see your registered events and QR tickets.")
        return

    email_norm = normalize_email(email)
    user_regs = st.session_state.REGS[st.session_state.REGS["email"] == email_norm]

    if user_regs.empty:
        st.warning("No registrations found for this email. Register for an event first!")
        return

    for _, reg in user_regs.iterrows():
        event = st.session_state.EVENTS[st.session_state.EVENTS["id"] == reg["event_id"]].iloc[0]
        
        with st.container():
            st.subheader(f"🎟️ {event['name']}")
            st.write(f"**Date:** {event['start_at'].strftime('%a, %b %d @ %I:%M %p')}")
            st.write(f"**Price Paid:** {CURRENCY_SYMBOLS.get(reg['currency'], '$')}{reg['price_paid']:,.0f}")
            if reg["offer_applied"] != "None":
                st.write(f"**Offer Applied:** {reg['offer_applied']}")
            
            
            # Generate QR Code
            qr_data = f"EVENT:{event['id']};EMAIL:{reg['email']};NAME:{reg['name']};TS:{reg['ts']}"
            qr_bytes = generate_qr_code(qr_data)
            st.image(qr_bytes, caption="Scan this QR code at event entrance", width=200)
            
            st.divider()

def render_live_stats_tab():
    st.header("📊 Live Command Center")
    st.markdown("Real-time metrics. Updates every 3 seconds.")

    total_regs = len(st.session_state.REGS)
    total_waitlist = len(st.session_state.WAITLIST)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Registrations", total_regs)
    col2.metric("Waitlist Size", total_waitlist)

    if st.session_state.EVENTS.empty:
        st.info("No events created yet.")
        return

    for _, event in st.session_state.EVENTS.iterrows():
        taken = st.session_state.INVENTORY[event["id"]]["taken_seats"]
        capacity = event["capacity"]
        fill_rate = taken / capacity * 100 if capacity > 0 else 0
        waitlist_count = len(st.session_state.WAITLIST[st.session_state.WAITLIST["event_id"] == event["id"]])

        with st.expander(f"📈 {event['name']}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Registered", taken)
            col2.metric("Capacity", capacity)
            col3.metric("Fill Rate", f"{fill_rate:.1f}%")
            col4.metric("Waitlist", waitlist_count)

            st.progress(fill_rate / 100.0)

            if not pd.isna(event["start_at"]) and isinstance(event["start_at"], datetime.datetime):
                time_to_start = (event["start_at"] - datetime.datetime.now()).total_seconds()
                if time_to_start > 0:
                    st.caption(f"Starts in: {int(time_to_start // 60)} minutes")
                else:
                    st.caption("Event in progress!")

            offer_redemptions = st.session_state.REGS[
                (st.session_state.REGS["event_id"] == event["id"]) &
                (st.session_state.REGS["offer_applied"] != "None")
            ]
            if len(offer_redemptions) > 0:
                st.caption(f"🔥 Offers redeemed: {len(offer_redemptions)}")



def render_admin_tab():
    """Render admin interface for managing events and viewing registrations."""
    st.header("🛠️ Admin Control Deck")

    if not st.session_state.admin_authenticated:
        pwd = st.text_input("Admin Password", type="password")
        if st.button("Authenticate", width="stretch"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("Access granted. Welcome, Captain.")
                st.rerun()
            else:
                st.error("Incorrect password.")
        return

    if st.button("🚪 Logout Admin", width="stretch"):
        st.session_state.admin_authenticated = False
        st.rerun()
        return

    # ================
    # EVENT MANAGEMENT
    # ================
    st.subheader("🌌 Event Management")

    edited_df = st.data_editor(
        st.session_state.EVENTS,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.TextColumn("ID", disabled=True),
            "start_at": st.column_config.DatetimeColumn("Start"),
            "end_at": st.column_config.DatetimeColumn("End"),
            "capacity": st.column_config.NumberColumn("Capacity", min_value=1, step=1),
            "price": st.column_config.NumberColumn("Price ($)", min_value=0.0, step=0.01),
            "offer_value": st.column_config.NumberColumn("Offer %", min_value=0, max_value=100, step=1),
            "offer_start": st.column_config.DatetimeColumn("Offer Start"),
            "offer_end": st.column_config.DatetimeColumn("Offer End"),
        }
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Save Events", width="stretch"):
            datetime_cols = ["start_at", "end_at", "offer_start", "offer_end"]
            edited_df = parse_datetime_columns(edited_df, datetime_cols)
            st.session_state.EVENTS = edited_df
            save_csv(edited_df, EVENTS_CSV)
            st.session_state.INVENTORY = {
                row["id"]: {
                    "taken_seats": len(st.session_state.REGS[st.session_state.REGS["event_id"] == row["id"]]),
                    "lock_until_ts": None
                }
                for _, row in edited_df.iterrows()
            }
            st.success("Events saved & inventory recomputed!")
            st.rerun()

    with col2:
        if st.button("📥 Export Registrations (CSV)", width="stretch"):
            csv_bytes = st.session_state.REGS.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv_bytes,
                file_name="hyperlane_registrations.csv",
                mime="text/csv",
                width="stretch"
            )

    with col3:
        if st.button("🔄 Recompute All Seats", width="stretch"):
            for event_id in st.session_state.INVENTORY.keys():
                taken = len(st.session_state.REGS[st.session_state.REGS["event_id"] == event_id])
                st.session_state.INVENTORY[event_id]["taken_seats"] = taken
            st.success("Seat counts refreshed from registration log.")

    st.divider()

    # ====================
    # REGISTRATIONS TABLE
    # ====================
    st.subheader("📋 Registrations Dashboard")

    if st.session_state.REGS.empty:
        st.info("No registrations yet.")
    else:
        # Merge with EVENTS to get event names
        regs_with_names = st.session_state.REGS.merge(
            st.session_state.EVENTS[["id", "name"]].rename(columns={"name": "event_name", "id": "event_id"}),
            on="event_id",
            how="left"
        )

        # Reorder columns for readability
        display_cols = ["ts", "name", "email", "event_name", "price_paid", "offer_applied", "currency"]
        regs_display = regs_with_names[display_cols].copy()

        # Rename for UI
        regs_display = regs_display.rename(columns={
            "ts": "Timestamp",
            "name": "Attendee Name",
            "email": "Email",
            "event_name": "Event",
            "price_paid": "Paid (Local)",
            "offer_applied": "Offer",
            "currency": "Currency"
        })

        # Add filter by event
        event_names = ["All Events"] + regs_display["Event"].dropna().unique().tolist()
        selected_event = st.selectbox("FilterWhere Event", event_names, index=0)

        if selected_event != "All Events":
            regs_display = regs_display[regs_display["Event"] == selected_event]

        # Show data editor (read-only for now)
        st.dataframe(
            regs_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
                "Attendee Name": st.column_config.TextColumn("Attendee Name", width="medium"),
                "Email": st.column_config.TextColumn("Email", width="large"),
                "Event": st.column_config.TextColumn("Event", width="medium"),
                "Paid (Local)": st.column_config.NumberColumn("Paid (Local)", format="%.2f"),
                "Offer": st.column_config.TextColumn("Offer", width="small"),
                "Currency": st.column_config.TextColumn("Currency", width="small"),
            }
        )

        st.caption(f"Total Registrations: {len(regs_display)}")

    st.divider()
    st.subheader("⏳ Waitlist")

    if st.session_state.WAITLIST.empty:
        st.info("No waitlisted users.")
    else:
        waitlist_with_names = st.session_state.WAITLIST.merge(
            st.session_state.EVENTS[["id", "name"]].rename(columns={"name": "event_name", "id": "event_id"}),
            on="event_id",
            how="left"
        )

        waitlist_display = waitlist_with_names.rename(columns={
            "ts": "Added At",
            "name": "Name",
            "email": "Email",
            "event_name": "Event",
            "notified": "Notified"
        })

        st.dataframe(
            waitlist_display[["Added At", "Name", "Email", "Event", "Notified"]],
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Waitlist Size: {len(waitlist_display)}")       


# ======================================================================
# 🧭 MAIN APP NAVIGATION
# ======================================================================

def main():
    st.sidebar.title("🚀 Hyperlane Events")
    st.sidebar.caption("Where time, space, and tickets collide.")

    default_tab = st.session_state.get("selected_tab", "Home")
    tab = st.sidebar.radio(
        "Navigate",
        ["Home", "Register", "My Tickets", "Live Stats", "Admin"],
        index=["Home", "Register", "My Tickets", "Live Stats", "Admin"].index(default_tab),
        key="main_nav"
    )
    st.session_state.selected_tab = tab

    if tab == "Live Stats":
        st_autorefresh = st.empty()
        # ✅ FIXED: use_container_width → width="stretch"
        if st_autorefresh.button("Manual Refresh", key="manual_refresh", width="stretch"):
            st.rerun()
        try:
            from streamlit_extras.autorefresh import st_autorefresh
            st_autorefresh(interval=AUTO_REFRESH_INTERVAL, key="live_stats_refresh")
        except ImportError:
            st.sidebar.info(f"Auto-refresh every {AUTO_REFRESH_INTERVAL//1000}s")

    if tab == "Home":
        render_homepage_tab()
    elif tab == "Register":
        render_register_tab()
    elif tab == "My Tickets":
        render_my_tickets_tab()
    elif tab == "Live Stats":
        render_live_stats_tab()
    elif tab == "Admin":
        render_admin_tab()

    st.sidebar.markdown("---")
    st.sidebar.caption("v2.0 • Built with Streamlit & Quantum Entanglement")

if __name__ == "__main__":
    main()

        # Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)