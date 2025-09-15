import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import random
import time
from datetime import datetime, timedelta
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
        <center> Day 7 - Gym Workout Logger</center>
    </h2>
    """,
    unsafe_allow_html=True
)
# ----------------------------
# 🔌 FIREBASE SETUP (Replace with your config)
# ----------------------------

try:
    import pyrebase

    firebaseConfig = {
        "apiKey": "AIzaSyATiZs8yaYLpEoy_jeQ-TJqkH4OPW9wtTU",
        "authDomain": "neurolift-39f68.firebaseapp.com",
        "databaseURL": "https://neurolift-39f68-default-rtdb.firebaseio.com",
        "projectId": "neurolift-39f68",
        "storageBucket": "neurolift-39f68.firebasestorage.app",
        "messagingSenderId": "373430031305",
        "appId": "1:373430031305:web:3cf69ead6681697a378e18",
        "measurementId": "G-RP8YQ88M39"
    }
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    auth = firebase.auth()
    cloud_sync_enabled = True
except:
    cloud_sync_enabled = False
    _FIREBASE_NOTICE = "Firebase not configured. Running in local mode."

# Ensure _FIREBASE_NOTICE is always defined
_FIREBASE_NOTICE = globals().get('_FIREBASE_NOTICE', None)

# ----------------------------
# 🔊 SOUND SETUP (Optional)
# ----------------------------

SOUND_ENABLED = False
try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except Exception:
    pygame = None
    SOUND_ENABLED = False

def play_sound(sound_name):
    if SOUND_ENABLED:
        try:
            pygame.mixer.music.load(f"sounds/{sound_name}.mp3")
            pygame.mixer.music.play()
        except:
            pass

# ----------------------------
# 🎨 CONFIG & STYLING
# ----------------------------

def inject_custom_css(dark_mode=True):
    bg_url = 'https://images.unsplash.com/photo-1687954023975-1d1c8a4e6f9b?q=80&w=1920&auto=format&fit=crop'
    text_color = "#e0f7ff" if dark_mode else "#0A0A14"
    bg_color = "rgba(10, 10, 20, 0.9)" if dark_mode else "rgba(255, 255, 255, 0.9)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap');

    .stApp {{
        background: url('{bg_url}');
        background-size: cover;
        color: {text_color};
        font-family: 'Rajdhani', sans-serif;
    }}

    h1, h2, h3 {{
        font-family: 'Orbitron', sans-serif;
        color: #00F5FF;
        text-shadow: 0 0 10px #00F5FF, 0 0 20px #00F5FF;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, #00F5FF, #B026FF);
        color: #0A0A14;
        font-family: 'Orbitron', sans-serif;
        border-radius: 12px;
        border: none;
        box-shadow: 0 0 15px #00F5FF;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 25px #00F5FF, 0 0 35px #B026FF;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>select {{
        background-color: {bg_color};
        border: 1px solid #00F5FF;
        color: {text_color};
        border-radius: 8px;
        box-shadow: inset 0 0 8px rgba(0, 245, 255, 0.3);
    }}

    .stDataFrame {{
        background: {bg_color};
        border-radius: 12px;
        border: 1px solid #B026FF;
        box-shadow: 0 0 15px rgba(176, 38, 255, 0.4);
    }}

    .css-1d391kg {{
        background: {bg_color};
        backdrop-filter: blur(10px);
        border-right: 1px solid #00F5FF;
    }}

    .pr-glow {{
        animation: glow 1.5s ease-in-out infinite alternate;
    }}
    @keyframes glow {{
        from {{ box-shadow: 0 0 5px #FF00C1; }}
        to {{ box-shadow: 0 0 20px #FF00C1, 0 0 30px #FF00C1; }}
    }}

    .svg-container {{
        width: 80px;
        height: 80px;
        margin: 10px auto;
    }}

    .level-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        background: linear-gradient(45deg, #FF00C1, #00F5FF);
        font-weight: bold;
        margin: 5px;
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# 🤖 ROBO-TRAINER NEX-9000 WITH ANIMATED SVG & VOICE
# ----------------------------

class RoboTrainer:
    def __init__(self):
        self.quotes = [
            "Muscle memory is just firmware upgrading. Reboot stronger.",
            "Your last set triggered a 0.7% neural adaptation. Proceed.",
            "Error 404: Excuse not found. Add weight.",
            "Biological limits are temporary. Override them.",
            "Efficiency rating: 94%. Optimal form detected.",
            "Adrenaline levels rising. Recommend heavy compound lift.",
            "You are 87% synced with peak performance mode.",
            "Warning: Rest period exceeded. Reactivate kinetic drive."
        ]
        self.motivation_assets = [
            {"gif": "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif", "text": "⚡ Rise, cyborg. The city waits for no one."},
            {"gif": "https://media.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif", "text": "💀 Push harder—upgrade your body like your code."},
            {"gif": "https://media.giphy.com/media/l3vR9O3vpOCDRo8rC/giphy.gif", "text": "🛰️ Systems online. Initiate strength protocol."},
            {"gif": "https://media.giphy.com/media/xTiTnGx8dQxV2zV2x6/giphy.gif", "text": "🔧 Repair. Reinforce. Rebuild. Then add plates."},
            {"gif": "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif", "text": "🚨 Overclock engaged. Deliver maximum output."}
        ]
        self.upgrades = {
            "Optic Overlay": {"cost": 500, "unlocked": False, "desc": "See predicted 1RMs floating above equipment."},
            "Kinetic Sync": {"cost": 750, "unlocked": False, "desc": "Auto-adjust suggested weights based on fatigue."},
            "Adrenaline Injector": {"cost": 1000, "unlocked": False, "desc": "Temporary +5% volume boost (tracked for fun)."}
        }
        self.neuro_credits = 0
        self.level = 1
        self.xp = 0
        self.xp_needed = 1000
        self.badges = []
        # Adrenaline boost (temporary reward multiplier)
        self.adrenaline_active_until = None
        self.adrenaline_multiplier = 1.05  # +5%
        self.engine = None
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
        except Exception:
            self.engine = None

    def is_adrenaline_active(self):
        if self.adrenaline_active_until is None:
            return False
        return datetime.now() < self.adrenaline_active_until

    def adrenaline_time_left_min(self):
        if not self.is_adrenaline_active():
            return 0
        remaining = self.adrenaline_active_until - datetime.now()
        return max(0, int(remaining.total_seconds() // 60))

    def speak(self, message, use_voice=False):
        container = f"""
        <div style='background: rgba(0,0,0,0.6); padding: 12px; border-radius: 10px; border-left: 4px solid #00F5FF; overflow:hidden;'>
            <div class="svg-container">
                {self.get_svg()}
            </div>
            <p style='font-family: Rajdhani; margin:6px 0 0 0; color:#e0f7ff; line-height:1.2;'><b>NEX-9000:</b> {message}</p>
            <div style='clear:both;'></div>
        </div>
        """
        st.sidebar.markdown(container, unsafe_allow_html=True)
        st.sidebar.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if use_voice and self.engine:
            try:
                self.engine.say(message)
                self.engine.runAndWait()
            except Exception:
                pass

    def get_svg(self):
        return """
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
            <circle cx="50" cy="40" r="25" fill="#0A0A14" stroke="#00F5FF" stroke-width="2"/>
            <circle cx="40" cy="35" r="4" fill="#00F5FF" opacity="0.8"/>
            <circle cx="60" cy="35" r="4" fill="#00F5FF" opacity="0.8"/>
            <circle cx="40" cy="35" r="2" fill="#FF00C1">
                <animate attributeName="r" values="2;3;2" dur="2s" repeatCount="indefinite"/>
            </circle>
            <circle cx="60" cy="35" r="2" fill="#FF00C1">
                <animate attributeName="r" values="2;3;2" dur="2s" repeatCount="indefinite"/>
            </circle>
            <path d="M 40 50 Q 50 55, 60 50" stroke="#B026FF" stroke-width="2" fill="none"/>
            <path d="M 45 45 L 45 55" stroke="#00F5FF" stroke-width="1" opacity="0.6"/>
            <path d="M 55 45 L 55 55" stroke="#00F5FF" stroke-width="1" opacity="0.6"/>
            <line x1="50" y1="35" x2="50" y2="25" stroke="#00F5FF" stroke-width="2"/>
            <circle cx="50" cy="25" r="2" fill="#FF00C1"/>
        </svg>
        """

    def motivate(self):
        return random.choice(self.quotes)

    def award_credits(self, amount, quiet: bool = False):
        # Apply adrenaline multiplier if active
        mult = self.adrenaline_multiplier if self.is_adrenaline_active() else 1.0
        amt = int(round(amount * mult))
        self.neuro_credits += amt
        if quiet:
            return amt
        if mult > 1.0:
            self.speak(f"+{amt} NeuroCredits (Boost x{mult:.2f}) — Total: {self.neuro_credits}")
        else:
            self.speak(f"+{amt} NeuroCredits awarded! Total: {self.neuro_credits}")
        return amt

    def unlock_upgrade(self, upgrade_name, show_card: bool = True):
        """Attempt to unlock an upgrade.
        Returns True if unlocked, False otherwise.
        """
        if upgrade_name not in self.upgrades:
            return False
        # Already unlocked → treat as no-op
        if self.upgrades[upgrade_name]["unlocked"]:
            return False

        cost = self.upgrades[upgrade_name]["cost"]
        if self.neuro_credits < cost:
            msg = f"⚠️ Not enough NeuroCredits. Need {cost - self.neuro_credits} more."
            if show_card:
                self.speak(msg)
            else:
                st.sidebar.warning(msg)
            return False

        # Deduct and unlock
        self.neuro_credits -= cost
        self.upgrades[upgrade_name]["unlocked"] = True

        if upgrade_name == "Adrenaline Injector":
            self.adrenaline_active_until = datetime.now() + timedelta(minutes=60)
            msg = "🧪 Adrenaline online. +5% rewards for the next 60 minutes!"
        else:
            msg = f"✅ {upgrade_name} unlocked! {self.upgrades[upgrade_name]['desc']}"

        if show_card:
            self.speak(msg)
        else:
            st.sidebar.success(msg)
        play_sound("levelup")
        return True

    def add_xp(self, amount, quiet: bool = False):
        mult = self.adrenaline_multiplier if self.is_adrenaline_active() else 1.0
        amt = int(round(amount * mult))
        self.xp += amt
        if self.xp >= self.xp_needed:
            self.level_up()
        return self.xp

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_needed = int(1000 * (1.5 ** (self.level - 1)))
        badge = f"Level {self.level} Cyborg"
        if badge not in self.badges:
            self.badges.append(badge)
        st.sidebar.success(f"🎉 LEVEL UP! You are now Level {self.level}!")
        st.toast("LEVEL UP! 🔥")
        play_sound("levelup")

    def get_status(self):
        return f"Lv.{self.level} | XP: {self.xp}/{self.xp_needed} | NeuroCredits: {self.neuro_credits}"


# ----------------------------
# 🎛️ LISTENING WIDGET (Animated Mic)
# ----------------------------

def render_listening_widget(limit_sec=10):
    """Show an animated mic + equalizer while recording.
    Returns the placeholder so the caller can clear it when done.
    """
    placeholder = st.empty()
    html = f"""
    <style>
    .mic-wrap {{
        background: rgba(0,0,0,0.55);
        border: 1px solid #00F5FF;
        border-radius: 12px; padding: 12px; display:flex; align-items:center; gap:14px;
        box-shadow: 0 0 12px rgba(0,245,255,0.25);
    }}
    .mic {{ width: 28px; height: 28px; border-radius: 50%; background:#00F5FF; position:relative; animation:pulse 1s infinite; }}
    .mic:after {{ content:''; position:absolute; inset:6px; border-radius:50%; background:#0A0A14; }}
    .bars {{ display:flex; gap:3px; align-items:flex-end; height:18px; margin-left:4px; }}
    .bars span {{ width:3px; background:#B026FF; animation: bounce 1s infinite ease-in-out; }}
    .bars span:nth-child(2){{ animation-delay:.1s }}
    .bars span:nth-child(3){{ animation-delay:.2s }}
    .bars span:nth-child(4){{ animation-delay:.3s }}
    @keyframes bounce {{ 0%,100%{{height:4px}} 50%{{height:18px}} }}
    @keyframes pulse {{ 0%{{ box-shadow:0 0 0 0 rgba(0,245,255,0.6)}} 70%{{ box-shadow:0 0 0 12px rgba(0,245,255,0)}} 100%{{ box-shadow:0 0 0 0 rgba(0,245,255,0)}} }}
    .mic-text {{ font-family:'Rajdhani',sans-serif; color:#e0f7ff; }}
    </style>
    <div class='mic-wrap'>
      <div class='mic'></div>
      <div class='bars'><span></span><span></span><span></span><span></span></div>
      <div class='mic-text'>Listening… up to {limit_sec}s. Say: <code>Log Bench Press 3 sets 8 reps 135 pounds</code></div>
    </div>
    """
    placeholder.markdown(html, unsafe_allow_html=True)
    return placeholder

# ----------------------------
# 🎙️ VOICE RECOGNITION MODULE
# ----------------------------

def recognize_speech():
    try:
        import speech_recognition as sr
    except ImportError:
        st.error("❌ SpeechRecognition not installed. Run: `pip install SpeechRecognition`\n\nIf you want to use the microphone on macOS, also install PortAudio and PyAudio:\n`brew install portaudio` then `pip install pyaudio`")
        return None

    try:
        r = sr.Recognizer()
        ui = None
        try:
            limit = 10
            ui = render_listening_widget(limit)
            with sr.Microphone() as source:
                # st.info("🎙️ Listening... Speak now (e.g., 'Log Bench Press 3 sets 8 reps 185 pounds')")
                audio = r.listen(source, timeout=5, phrase_time_limit=limit)
                text = r.recognize_google(audio)
                st.toast("✅ Recorded")
                st.success(f"🗣️ You said: {text}")
                ui.empty()
                return text
        except sr.WaitTimeoutError:
            st.error("⏱️ Listening timed out. Try again in a quieter environment.")
            try:
                ui.empty()
            except Exception:
                pass
            return None
        except sr.UnknownValueError:
            st.error("🤷 Could not understand the audio. Please speak clearly and try again.")
            try:
                ui.empty()
            except Exception:
                pass
            return None
        except sr.RequestError as e:
            st.error(f"🌐 Speech API error: {e}")
            try:
                ui.empty()
            except Exception:
                pass
            return None
        except Exception as e:
            st.error(f"❌ Microphone error: {e}")
            try:
                ui.empty()
            except Exception:
                pass
            return None
    except ImportError:
        st.error("❌ SpeechRecognition not installed. Run: `pip install SpeechRecognition`\n\nIf you want to use the microphone on macOS, also install PortAudio and PyAudio:\n`brew install portaudio` then `pip install pyaudio`")
        return None

def parse_voice_command(text):
    if not text:
        return None

    raw = text
    t = text.lower().strip()

    import re

    # --- 1) Convert number words → digits (basic 1–20)
    words2num = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20
    }
    def replace_num_words(s):
        return re.sub(r"\b(" + "|".join(words2num.keys()) + r")\b",
                      lambda m: str(words2num[m.group(1)]), s)
    t = replace_num_words(t)

    # --- 2) Normalize fillers
    t = t.replace("lbs", " pounds").replace(" lb", " pounds")
    t = t.replace(" x ", " x ").replace(" at ", " ").replace(" for ", " ").replace(" of ", " ")

    # Helper to pull last-known defaults
    def get_defaults():
        # Defaults
        defaults = {"exercise": "Bench Press", "sets": 1, "reps": 8, "weight": 45.0}
        try:
            last = st.session_state.get("last_quick_log")
            if last:
                defaults.update({
                    "exercise": last.get("exercise", defaults["exercise"]),
                    "reps": int(last.get("reps", defaults["reps"])),
                    "weight": float(last.get("weight", defaults["weight"]))
                })
            logger = st.session_state.get("logger")
            if logger is not None and not logger.data.empty:
                recent = logger.data.iloc[-1]
                defaults.setdefault("exercise", str(recent.get("exercise", defaults["exercise"])))
                if pd.notnull(recent.get("reps")):
                    defaults["reps"] = int(recent.get("reps"))
                if pd.notnull(recent.get("weight")):
                    defaults["weight"] = float(recent.get("weight"))
        except Exception:
            pass
        return defaults

    # --- 3) Strong patterns (with explicit numbers)
    patterns = [
        r"(?:log\s+)?(?P<exercise>[a-z\s]+?)\s+(?P<sets>\d+)\s*sets?\s+(?P<reps>\d+)\s*reps?\s+(?P<weight>\d+(?:\.\d+)?)\s*(?:pounds|kg|kilograms)?",
        r"(?:log\s+)?(?P<exercise>[a-z\s]+?)\s+(?P<sets>\d+)\s*x\s*(?P<reps>\d+)\s*@\s*(?P<weight>\d+(?:\.\d+)?)\s*(?:pounds|kg|kilograms)?",
        r"(?:log\s+)?(?P<exercise>[a-z\s]+?)\s+(?P<sets>\d+)\s*by\s*(?P<reps>\d+)\s+(?P<weight>\d+(?:\.\d+)?)\s*(?:pounds|kg|kilograms)?",
    ]
    for pat in patterns:
        m = re.search(pat, t)
        if m:
            try:
                ex = re.sub(r"\s+", " ", m.group("exercise").strip()).title()
                return {
                    "exercise": ex,
                    "sets": int(m.group("sets")),
                    "reps": int(m.group("reps")),
                    "weight": float(m.group("weight"))
                }
            except Exception:
                pass

    # --- 4) Softer pattern: "bench press 3 sets" (reps/weight defaulted)
    m = re.search(r"^(?:log\s+)?(?P<exercise>[a-z\s]+?)\s+(?P<sets>\d+)\s*sets?\b", t)
    if m:
        d = get_defaults()
        ex = re.sub(r"\s+", " ", m.group("exercise").strip()).title()
        return {"exercise": ex, "sets": int(m.group("sets")), "reps": d["reps"], "weight": d["weight"]}

    # --- 5) Minimal: just exercise name → use all defaults
    # e.g., "bench press" or "log bench press"
    m = re.search(r"^(?:log\s+)?(?P<exercise>[a-z\s]{3,})$", t)
    if m:
        d = get_defaults()
        ex = re.sub(r"\s+", " ", m.group("exercise").strip()).title()
        return {"exercise": ex, "sets": d["sets"], "reps": d["reps"], "weight": d["weight"]}

    # --- 6) Fallback: first three numbers = sets, reps, weight
    nums = re.findall(r"\d+(?:\.\d+)?", t)
    if len(nums) >= 3:
        d = get_defaults()
        # Try to guess exercise name before first number
        cut = t.find(nums[0])
        ex = re.sub(r"\s+", " ", t[:cut].replace("log", "").strip()).title() or d["exercise"]
        try:
            return {
                "exercise": ex,
                "sets": int(float(nums[0])),
                "reps": int(float(nums[1])),
                "weight": float(nums[2])
            }
        except Exception:
            pass

    st.warning("⚠️ Could not parse voice command. Try simpler: 'Bench press 3 sets' or full: 'Log Bench Press 3 sets 8 reps 135 pounds'")
    st.caption(f"Heard: '{raw}'")
    return None

# ----------------------------
# 🖐️ GESTURE DETECTION MODULE (OpenCV)
# ----------------------------


def detect_gesture():
    """Run a lightweight gesture detector without creating native OpenCV windows.
    Renders frames inside Streamlit to avoid macOS thread issues.
    Returns "LOG", "UNDO", or None.
    """
    try:
        import cv2
        import time as _time
        import math as _math
        import numpy as _np
    except ImportError:
        st.error("❌ OpenCV not installed. Run: `pip install opencv-python`")
        return None

    # Try AVFoundation first (macOS), then fallback to default
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        cap.release()
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error(
            "📷 Camera could not be opened. On macOS, go to System Settings → Privacy & Security → Camera and allow access for Terminal/IDE (Python).\n\n"
            "If you still don't see a prompt, close this app and run a one-time helper: `python camera_auth_test.py` to trigger the OS prompt from the main thread."
        )
        return None

    st.info("🖐️ Camera active. Show ✌️ (two fingers) to LOG or 🖐️ (open palm) to UNDO. Close tab or wait to stop.")
    frame_slot = st.empty()
    gesture = None

    def _analyze(th):
        # Find largest contour and compute geometry
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            return None
        cnt = max(cnts, key=cv2.contourArea)
        area = cv2.contourArea(cnt)
        perim = cv2.arcLength(cnt, True)
        circularity = (4 * _math.pi * area) / (perim * perim) if perim > 0 else 0
        if area < 5000:  # ignore tiny/noisy blobs
            return None
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull) if hull is not None else 0
        solidity = (area / hull_area) if hull_area > 0 else 0

        hull_idx = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull_idx) if hull_idx is not None and len(hull_idx) >= 3 else None
        gaps = 0
        if defects is not None:
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = cnt[s][0]
                end = cnt[e][0]
                far = cnt[f][0]
                a = _math.dist(end, far)
                b = _math.dist(start, far)
                c = _math.dist(start, end)
                if a == 0 or b == 0:
                    continue
                angle = _math.degrees(_math.acos(max(-1.0, min(1.0, (a*a + b*b - c*c) / (2*a*b + 1e-6)))))
                depth = d / 256.0
                # Stricter: only count deep, sharp valleys as finger gaps
                if angle < 70 and depth > 20:
                    gaps += 1
        
        
        

        fingers = max(0, min(5, gaps + 1))  # rough estimate based on gap count
        return {
        'cnt': cnt,
        'hull': hull,
        'solidity': solidity,
        'gaps': gaps,
        'fingers': fingers,
        'area': area,
        'circularity': circularity
}
    try:
        max_runtime_s = 12
        warmup_s = 0.6
        required_stable_frames = 4
        start = _time.time()
        warmup_end = start + warmup_s
        prev_detect = None
        stable = 0

        while _time.time() - start < max_runtime_s:
            ok, frame = cap.read()
            if not ok or frame is None:
                _time.sleep(0.03)
                continue

            # Center ROI to reduce background noise
            h, w = frame.shape[:2]
            x0, y0 = int(w*0.15), int(h*0.15)
            x1, y1 = int(w*0.85), int(h*0.85)
            roi = frame[y0:y1, x0:x1]

            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (7, 7), 0)
            _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Compute white-pixel ratio
            white = cv2.countNonZero(th)
            total = th.shape[0] * th.shape[1]
            ratio = white / max(total, 1)

            # --- Decision block using solidity, convexity defects, circularity, and ratio ---
            geom = _analyze(th)
            current = None
            if geom is not None:
                gaps = geom['gaps']
                solidity = geom['solidity']
                circ = geom['circularity']
                # LOG (fist): very compact silhouette → high solidity or high circularity or low area ratio
                if gaps == 0 and (solidity >= 0.85 or circ >= 0.80 or ratio < 0.38):
                    current = "LOG"
                # UNDO (peace/open): at least one clear finger gap and not too solid, with larger area ratio
                elif (1 <= gaps <= 3) and (0.55 <= solidity <= 0.92) and ratio >= 0.38:
                    current = "UNDO"
                else:
                    current = None
            else:
                # Fallback on shape area ratio only
                if ratio < 0.38:
                    current = "LOG"
                elif ratio <= 0.62:
                    current = "UNDO"
                else:
                    current = None

            # Warmup ignores early detections
            if _time.time() < warmup_end:
                current = None
                stable = 0
                prev_detect = None

            # Debounce: require stable frames
            if current is not None:
                if current == prev_detect:
                    stable += 1
                else:
                    prev_detect = current
                    stable = 1
            else:
                prev_detect = None
                stable = 0

            geom = _analyze(th)
            current = None
            if geom is not None:
                fingers = geom.get('fingers', 0)
            # ✌️ exactly two fingers → LOG
                if fingers == 2:
                    current = "LOG"
                # 🖐️ open palm (4 or 5 fingers) → UNDO
                elif fingers >= 4:
                    current = "UNDO"
                else:
                    current = None
            else:
        # Fallback using area ratio: large hand likely open palm → UNDO; moderate segmented likely two fingers → LOG
                if ratio >= 0.55:
                 current = "UNDO"
                elif 0.30 <= ratio < 0.55:
                 current = "LOG"
                else:
                 current = None

            # HUD overlay
            overlay = roi.copy()
            info = (
            f"Fingers:{geom.get('fingers',0)} Gap:{geom['gaps']} Sol:{geom['solidity']:.2f} Circ:{geom['circularity']:.2f} R:{ratio:.2f}"
            if geom is not None else f"Analyzing… R:{ratio:.2f}"
        )
            cv2.putText(overlay, info, (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
            cv2.putText(overlay, f"Detect: {current or '-'}  Stable: {stable}/{required_stable_frames}", (10, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
            cv2.rectangle(frame, (x0,y0), (x1,y1), (0,255,255), 1)
            frame[y0:y1, x0:x1] = overlay

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_slot.image(frame_rgb, channels="RGB", use_container_width=True, caption="Gesture Control")

            if current is not None and stable >= required_stable_frames:
                gesture = current
                break

            _time.sleep(0.03)
    except Exception as e:
        st.error(f"❌ Camera error: {e}")
        gesture = None
    finally:
        try:
            cap.release()
        except Exception:
            pass

    return gesture
# ----------------------------
# 💾 DATA MANAGER (WITH FIREBASE SYNC)
# ----------------------------

class WorkoutLogger:
    def __init__(self, filename="workout_data.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        def _normalize_records(val):
            # Accept list or dict and return list[dict]
            if val is None:
                return []
            if isinstance(val, list):
                return [r for r in val if isinstance(r, dict)]
            if isinstance(val, dict):
                return [r for r in val.values() if isinstance(r, dict)]
            return []

        def _ensure_schema_df(df):
            # Ensure required columns exist with sane defaults
            required = {
                'date': None,
                'timestamp': None,
                'exercise': '',
                'sets': 0,
                'reps': 0,
                'weight': 0.0,
                'rpe': 0,
                'volume': 0.0,
            }
            for k, default in required.items():
                if k not in df.columns:
                    df[k] = default
            # Cast to JSON-safe primitives
            df['exercise'] = df['exercise'].astype(str)
            for c in ['sets', 'reps', 'rpe']:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
            for c in ['weight', 'volume']:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0).astype(float)
            # Coerce dates
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
            # Timestamps: ensure strings if present
            if 'timestamp' in df.columns:
                df['timestamp'] = df['timestamp'].astype(str)
            return df[ ['date','timestamp','exercise','sets','reps','weight','rpe','volume'] ]

        # Try Firebase first
        if cloud_sync_enabled:
            try:
                user_id = "default_user"  # Replace with auth if needed
                snapshot = db.child("users").child(user_id).child("workouts").get()
                records = _normalize_records(snapshot.val())
                if records:
                    df = pd.DataFrame(records)
                    return _ensure_schema_df(df)
            except Exception:
                pass

        # Fallback to local
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    raw = json.load(f)
                records = _normalize_records(raw)
                if records:
                    df = pd.DataFrame(records)
                    return _ensure_schema_df(df)
            except Exception:
                pass

        # Empty default
        return pd.DataFrame(columns=["date", "timestamp", "exercise", "sets", "reps", "weight", "rpe", "volume"]) 

    def save_data(self):
        # Prepare a JSON-safe list of records (no NaN/NaT, only primitives)
        df_safe = self.data.copy()
        # Convert NaN/NaT to None
        df_safe = df_safe.where(pd.notnull(df_safe), None)
        records = df_safe.to_dict(orient='records')
        # Ensure timestamps are strings
        for rec in records:
            if isinstance(rec.get('timestamp'), (pd.Timestamp,)):
                rec['timestamp'] = rec['timestamp'].isoformat()

        # Save to Firebase
        if cloud_sync_enabled:
            try:
                user_id = "default_user"
                # Write an array at the path; Firebase requires valid JSON
                db.child("users").child(user_id).child("workouts").set(records)
            except Exception as e:
                st.warning(f"⚠️ Cloud sync failed: {e}")

        # Save locally as well (always JSON-safe)
        try:
            with open(self.filename, 'w') as f:
                json.dump(records, f, indent=2, allow_nan=False)
        except TypeError:
            # Fallback: coerce anything weird to string
            with open(self.filename, 'w') as f:
                json.dump([{k: (v if isinstance(v, (str, int, float, bool)) or v is None else str(v)) for k, v in r.items()} for r in records], f, indent=2, allow_nan=False)

    def log_workout(self, exercise, sets, reps, weight, rpe=7):
        volume = sets * reps * weight
        new_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(timespec='seconds'),
            "exercise": str(exercise),
            "sets": int(sets),
            "reps": int(reps),
            "weight": float(weight),
            "rpe": int(rpe),
            "volume": float(volume)
        }
        self.data = pd.concat([self.data, pd.DataFrame([new_entry])], ignore_index=True)
        self.save_data()
        return new_entry

    def get_weekly_progress(self):
        df = self.data.copy()
        if df.empty or 'date' not in df.columns or 'volume' not in df.columns:
            return pd.DataFrame(columns=['week','volume','weight'])
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        if df.empty:
            return pd.DataFrame(columns=['week','volume','weight'])
        df['week'] = df['date'].dt.isocalendar().week
        weekly = df.groupby('week').agg({
            'volume': 'sum',
            'weight': 'mean'
        }).reset_index()
        return weekly

    def get_prs(self):
        prs = self.data.groupby('exercise')['weight'].max().reset_index()
        prs.columns = ['exercise', 'PR']
        return prs

    def predict_next_weight(self, exercise):
        df = self.data[self.data['exercise'] == exercise].copy()
        if len(df) < 3:
            return None
        df = df.sort_values('date').reset_index(drop=True)
        df['session_num'] = range(1, len(df)+1)
        try:
            from sklearn.linear_model import LinearRegression
        except ImportError:
            return None
        model = LinearRegression()
        X = df[['session_num']]
        y = df['weight']
        model.fit(X, y)
        next_session = len(df) + 1
        import pandas as _pd
        pred = model.predict(_pd.DataFrame([[next_session]], columns=['session_num']))[0]
        return round(pred, 1)

    def clear_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.data = self.data[self.data['date'] != today].reset_index(drop=True)
        self.save_data()

    def delete_by_index(self, idx: int):
        try:
            if idx in self.data.index:
                self.data = self.data.drop(idx).reset_index(drop=True)
                self.save_data()
        except Exception:
            pass

# ----------------------------
# 📊 GRAPH RENDERER
# ----------------------------

def plot_weekly_volume(df):
    fig = px.line(df, x='week', y='volume',
                  title='⚡ Weekly Volume Progress',
                  markers=True,
                  line_shape='spline')
    fig.update_traces(line_color='#00F5FF', line_width=4)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Rajdhani",
        font_color="#e0f7ff",
        title_font_size=24,
        title_font_color="#00F5FF"
    )
    fig.update_xaxes(showgrid=False, color='#B026FF')
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0, 245, 255, 0.2)', color='#B026FF')
    return fig

def plot_pr_comparison(pr_df):
    fig = px.bar(pr_df, x='exercise', y='PR',
                 title='🏆 Personal Records',
                 color_discrete_sequence=['#FF00C1'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Rajdhani",
        font_color="#e0f7ff",
        title_font_size=24,
        title_font_color="#FF00C1"
    )
    return fig

# ----------------------------
# 🎮 GAMIFICATION MANAGER
# ----------------------------

def check_achievements(data, trainer):
    if len(data) > 0:
        last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        recent = data[data['date'] >= last_week]
        if len(recent) >= 5:
            trainer.award_credits(100)
            trainer.add_xp(200)
        if recent['volume'].sum() > 5000:
            trainer.award_credits(200)
            trainer.add_xp(300)
        if len(recent) > 0 and recent['weight'].max() > recent['weight'].quantile(0.9):
            trainer.award_credits(150)
            trainer.add_xp(250)

# ----------------------------
# 🧠 MAIN APP
# ----------------------------

def main():
    st.set_page_config(
        page_title="NeuroLift — AI Cyber Gym Logger",
        page_icon="🏋️‍♂️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Dark/Light Mode Toggle
    dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=True)
    inject_custom_css(dark_mode)

    # Initialize session state
    if 'trainer' not in st.session_state:
        st.session_state.trainer = RoboTrainer()
    if 'logger' not in st.session_state:
        st.session_state.logger = WorkoutLogger()

    trainer = st.session_state.trainer
    logger = st.session_state.logger

    if not cloud_sync_enabled and _FIREBASE_NOTICE:
        st.sidebar.warning(_FIREBASE_NOTICE)

    # Sidebar — Robo-Trainer + Stats
    with st.sidebar:
        st.markdown("### 🤖 NEX-9000")
        st.markdown(f"**Status:** `{trainer.get_status()}`")
        for badge in trainer.badges:
            st.markdown(f'<div class="level-badge">{badge}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🎯 Quick Actions")
        # Adrenaline badge
        if trainer.is_adrenaline_active():
            st.markdown(f"`Adrenaline Active: {trainer.adrenaline_time_left_min()}m left (x{trainer.adrenaline_multiplier:.2f})`")
        motivate_slot = st.empty()
        def _normalize_youtube_url(u: str):
            import re
            # Convert Shorts or youtu.be to standard watch URL and capture ID
            vid_id = None
            m = re.search(r"youtube\.com/shorts/([\w-]{5,})", u)
            if m:
                vid_id = m.group(1)
            else:
                m = re.search(r"(?:v=|youtu\.be/)([\w-]{5,})", u)
                if m:
                    vid_id = m.group(1)
            watch = f"https://www.youtube.com/watch?v={vid_id}" if vid_id else u
            embed = f"https://www.youtube.com/embed/{vid_id}" if vid_id else None
            return watch, embed, vid_id
        # Only show "Close Video" once a video has been loaded
        if st.button("🎯 Motivate Me"):
            motivate_slot.empty()
            shorts = [
                "https://www.youtube.com/shorts/TfkP-834xhI",
                "https://www.youtube.com/shorts/ptMKRHmhmgY",
                "https://www.youtube.com/shorts/mcqdO_STJcM",
                "https://www.youtube.com/shorts/YBG7-zjFOdc",
                "https://www.youtube.com/shorts/A2hwOybGIe0",
                "https://www.youtube.com/shorts/CBvAmCGHcQs",
                "https://www.youtube.com/shorts/_EpXvoi9kho",
                "https://www.youtube.com/shorts/YAhtQxlcH0M",
                "https://www.youtube.com/shorts/KZ5dNjNTVHE",
                "https://www.youtube.com/shorts/D2HPo2gPQE4",
                "https://www.youtube.com/shorts/9lrcMljD3Vc",
                "https://www.youtube.com/shorts/hR6gabyY9gY"
            ]
            raw = random.choice(shorts)
            watch_url, embed_url, vid_id = _normalize_youtube_url(raw)
            if vid_id:
                params = "?autoplay=1&mute=0&playsinline=1&rel=0&modestbranding=1&controls=1&enablejsapi=1"
                iframe = f"<iframe width='100%' height='360' src='https://www.youtube.com/embed/{vid_id}{params}' frameborder='0' allow='autoplay; accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share' allowfullscreen></iframe>"
                motivate_slot.markdown(iframe, unsafe_allow_html=True)
            else:
                with motivate_slot:
                    st.video(watch_url)
            st.toast("⚡ Quick motivation engaged — autoplay")
            # Show close button only after video appears
            if st.button("✖️ Close Video"):
                motivate_slot.empty()
                st.toast("Video closed")
        if st.button("🔓 Unlock Kinetic Sync (750)"):
            if trainer.unlock_upgrade("Kinetic Sync", show_card=False):
                st.info("Kinetic Sync activated: AI suggestions will auto-adjust based on your recent RPE and fatigue.")
        if st.button("🧪 Simulate Adrenaline (1000)"):
            if trainer.unlock_upgrade("Adrenaline Injector", show_card=False):
                st.info(f"Adrenaline active: +5% XP & NeuroCredits for {trainer.adrenaline_time_left_min()} minutes.")
        st.markdown("---")
        st.markdown("### 📈 Weekly Stats")
        weekly = logger.get_weekly_progress()
        if not weekly.empty:
            delta = weekly.iloc[-1]['volume'] - weekly.iloc[0]['volume'] if len(weekly) > 1 else 0
            st.metric("Volume Trend", f"{weekly.iloc[-1]['volume']:.0f}", f"{delta:+.0f}")
        st.markdown("### 💡 Cyber Upgrades Guide")
        st.info("Earn **NeuroCredits** by logging workouts. Use them to unlock futuristic upgrades:\n- 🔓 Kinetic Sync (750): Auto-adjust weights based on fatigue.\n- 🧪 Adrenaline Injector (1000): +5% rewards for 60 minutes.\n- 👁️ Optic Overlay (500): See predicted 1RMs above equipment.\n\nLevel up with XP from volume logged and unlock badges as you progress!")
        if cloud_sync_enabled:
            st.success("🌐 Cloud Sync: ACTIVE")
        # Remove any RoboTrainer.speak or SVG robot face rendering for this info section.

    # Header
    st.markdown("<h1 style='text-align:center;'>⚡ NEUROLIFT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2em;'>Train like a cyborg. Recover like an AI. Dominate like a machine.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Log Workout", "🎙️ Voice/Gesture", "📊 Progress", "💾 History", "🎮 Cyber Upgrades"])

    # TAB 1: LOG WORKOUT
    with tab1:
        st.markdown("### 📥 Log Your Set")
        col1, col2 = st.columns(2)

        with col1:
            exercise = st.selectbox("Exercise", [
                "Bench Press", "Squat", "Deadlift", "Overhead Press", "Barbell Row",
                "Pull-Up", "Dumbbell Curl", "Leg Press", "Lat Pulldown"
            ])
            sets = st.number_input("Sets", min_value=1, max_value=10, value=3)
            reps = st.number_input("Reps", min_value=1, max_value=20, value=8)

        with col2:
            weight = st.number_input("Weight (lbs)", min_value=0.0, step=2.5, value=135.0)
            rpe = st.slider("RPE (Rate of Perceived Exertion)", 1, 10, 7)
            pred = logger.predict_next_weight(exercise)
            if pred:
                adjusted = pred
                adj_note = ""
                if trainer.upgrades.get("Kinetic Sync", {}).get("unlocked"):
                    # Compute fatigue from last 3 RPEs for this exercise
                    recent_ex = logger.data[logger.data['exercise'] == exercise].tail(3)
                    if not recent_ex.empty and 'rpe' in recent_ex.columns:
                        avg_rpe = float(pd.to_numeric(recent_ex['rpe'], errors='coerce').dropna().mean()) if not recent_ex['rpe'].empty else None
                    else:
                        avg_rpe = None
                    def _round_to_plate(x):
                        try:
                            return round(x / 2.5) * 2.5
                        except Exception:
                            return x
                    if avg_rpe is not None:
                        if avg_rpe >= 9:
                            adjusted = max(0.0, pred - 5.0)
                            adj_note = f" (Kinetic Sync: −5 based on avg RPE {avg_rpe:.1f})"
                        elif avg_rpe >= 8:
                            adjusted = max(0.0, pred - 2.5)
                            adj_note = f" (Kinetic Sync: −2.5 based on avg RPE {avg_rpe:.1f})"
                        elif avg_rpe <= 5:
                            adjusted = pred + 5.0
                            adj_note = f" (Kinetic Sync: +5 based on avg RPE {avg_rpe:.1f})"
                        elif avg_rpe <= 6:
                            adjusted = pred + 2.5
                            adj_note = f" (Kinetic Sync: +2.5 based on avg RPE {avg_rpe:.1f})"
                        adjusted = _round_to_plate(adjusted)
                st.info(f"🤖 AI Suggestion: Try **{adjusted} lbs** next for {exercise}{adj_note}")

        if st.button("✅ LOG SET — ACTIVATE NEURAL SYNC", use_container_width=True):
            entry = logger.log_workout(exercise, sets, reps, weight, rpe)
            # Remember last quick-log template for gesture logging
            st.session_state["last_quick_log"] = {
                "exercise": exercise,
                "reps": reps,
                "weight": weight,
                "rpe": rpe
            }
            volume = entry['volume']
            st.success(f"✅ Logged: {exercise} | {sets}x{reps} @ {weight}lbs → Volume: {volume}")
            trainer.award_credits(int(volume / 100), quiet=True)
            trainer.add_xp(int(volume / 10), quiet=True)
            check_achievements(logger.data, trainer)
            st.toast("Neural sync: set saved ✅")
            play_sound("log")

    # TAB 2: VOICE & GESTURE
    with tab2:
        st.markdown("### 🎙️ Voice Command Logging")
        if st.button("🎤 Start Listening"):
            text = recognize_speech()
            command = parse_voice_command(text)
            if command:
                entry = logger.log_workout(
                    command["exercise"],
                    command["sets"],
                    command["reps"],
                    command["weight"],
                    7
                )
                # Update last quick log template for gesture use
                st.session_state["last_quick_log"] = {
                    "exercise": command["exercise"],
                    "reps": command["reps"],
                    "weight": command["weight"],
                    "rpe": 7
                }
                st.toast("💪 Voice set logged")
                volume = entry['volume']
                trainer.award_credits(int(volume / 100), quiet=True)
                trainer.add_xp(int(volume / 10), quiet=True)
                play_sound("log")

        st.markdown("### 🖐️ Gesture Control (✌️ = Log, 🖐️ = Undo)")
        if st.button("🖐️ Start Camera Gesture Detection"):
            gesture = detect_gesture()
            if gesture == "LOG":
                st.success("👊 Gesture: LOG detected! Logging a quick set…")
                last = st.session_state.get("last_quick_log")
                if last:
                    entry = logger.log_workout(last["exercise"], 1, last["reps"], last["weight"], last.get("rpe", 7))
                elif not logger.data.empty:
                    recent = logger.data.iloc[-1]
                    entry = logger.log_workout(str(recent["exercise"]), 1, int(recent["reps"]), float(recent["weight"]), int(recent.get("rpe", 7)))
                else:
                    entry = logger.log_workout("Bench Press", 1, 8, 45.0, 6)
                volume = entry['volume']
                trainer.award_credits(int(volume / 100), quiet=True)
                trainer.add_xp(int(volume / 10), quiet=True)
                play_sound("log")
                st.toast("Quick set logged via gesture ✨")
            elif gesture == "UNDO":
                if not logger.data.empty:
                    last_idx = logger.data.index[-1]
                    last_row = logger.data.iloc[-1]
                    logger.delete_by_index(last_idx)
                    st.success(f"✌️ Undid last entry: {last_row['exercise']} {int(last_row['sets'])}x{int(last_row['reps'])} @ {last_row['weight']}lbs")
                    st.toast("Last set removed 🧹")
                    play_sound("log")
                    st.caption("📷 Camera paused — holding last frame")
                else:
                    st.info("No entries to undo.")

    # TAB 3: PROGRESS GRAPHS
    with tab3:
        st.markdown("### 📈 Weekly Progress")
        weekly = logger.get_weekly_progress()
        if not weekly.empty:
            st.plotly_chart(plot_weekly_volume(weekly), use_container_width=True)
        else:
            st.info("Log some workouts to see progress!")

        st.markdown("### 🏆 Personal Records")
        prs = logger.get_prs()
        if not prs.empty:
            st.plotly_chart(plot_pr_comparison(prs), use_container_width=True)
        else:
            st.info("PRs will appear after you log lifts!")

    # TAB 4: HISTORY
    with tab4:
        st.markdown("### 💾 Holographic Workout Log")
        if not logger.data.empty:
            df_display = logger.data.copy()
            pr_map = logger.get_prs().set_index('exercise')['PR'].to_dict()
            df_display['is_pr'] = df_display.apply(lambda row: row['weight'] == pr_map.get(row['exercise'], 0), axis=1)
            if 'timestamp' in df_display.columns:
                df_display['time'] = pd.to_datetime(df_display['timestamp']).dt.strftime('%H:%M')
            else:
                df_display['time'] = ''
            df_display['date'] = pd.to_datetime(df_display['date']).dt.strftime('%a %b %d, %Y')
            df_display = df_display.sort_values('date', ascending=False).reset_index(drop=True)


            st.dataframe(
                df_display[['date', 'time', 'exercise', 'sets', 'reps', 'weight', 'rpe', 'volume', 'is_pr']].rename(
                    columns={
                        'date': 'Date',
                        'time': 'Time',
                        'exercise': 'Exercise',
                        'sets': 'Sets',
                        'reps': 'Reps',
                        'weight': 'Weight (lbs)',
                        'rpe': 'RPE',
                        'volume': 'Volume',
                        'is_pr': 'PR Achieved'
                    }
                ),
                use_container_width=True,
                hide_index=True
            )
            act_left, act_right = st.columns([2, 1])
            with act_left:
                if not logger.data.empty:
                    _opts_df = logger.data.reset_index()
                    _opts_df['label'] = _opts_df.apply(lambda r: f"{r['index']}: {r['date']} {r.get('timestamp','')} — {r['exercise']} {int(r['sets'])}x{int(r['reps'])} @ {r['weight']}lbs", axis=1)
                    _labels = _opts_df['label'].tolist()
                    _selection = st.selectbox("Select an entry to delete", _labels, index=0 if _labels else None)
                    if st.button("❌ Delete Selected Entry", use_container_width=True):
                        try:
                            _idx = int(_selection.split(":", 1)[0])
                            logger.delete_by_index(_idx)
                            st.success("Entry deleted.")
                            st.rerun()
                        except Exception:
                            st.warning("Could not delete the selected entry.")
            with act_right:
                if st.button("🗑️ Clear Today’s Logs", use_container_width=True):
                    logger.clear_today()
                    st.success("Cleared all logs for today.")
                    st.rerun()
        else:
            st.info("No workouts logged yet. Start lifting!")

    # TAB 5: CYBER UPGRADES & LEVELS
    with tab5:
        st.markdown("### 🎮 Unlock Cybernetic Enhancements")
        st.markdown(f"**NeuroCredits**: `{trainer.neuro_credits}` | **Level**: `{trainer.level}`")
        st.progress(trainer.xp / trainer.xp_needed if trainer.xp_needed > 0 else 0)
        if trainer.is_adrenaline_active():
            st.success(f"🧪 Adrenaline Boost active — x{trainer.adrenaline_multiplier:.2f} rewards for {trainer.adrenaline_time_left_min()}m")

        for name, details in trainer.upgrades.items():
            col1, col2 = st.columns([3,1])
            with col1:
                status = "✅ UNLOCKED" if details['unlocked'] else f"🔒 LOCKED ({details['cost']} NeuroCredits)"
                st.markdown(f"### {name}")
                st.caption(details['desc'])
                st.markdown(f"`{status}`")
            with col2:
                if not details['unlocked']:
                    if st.button(f"Unlock ({details['cost']})", key=name):
                        trainer.unlock_upgrade(name)
                else:
                    st.button("✔️ ACTIVE", disabled=True, key=name+"_active")
            st.markdown("---")

        st.markdown("### 🥇 Battle Your Ghost")
        if len(logger.data) > 5:
            this_week = logger.data[logger.data['date'] >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")]
            last_week = logger.data[
                (logger.data['date'] < (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")) &
                (logger.data['date'] >= (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"))
            ]
            tw_vol = this_week['volume'].sum() if not this_week.empty else 0
            lw_vol = last_week['volume'].sum() if not last_week.empty else 0
            delta = tw_vol - lw_vol
            st.metric("This Week vs Last Week", f"{tw_vol:.0f}", f"{delta:+.0f}")
            if delta > 0:
                st.toast("🏋️ Victory! You crushed your Ghost this week! 🏆")
                prog = st.progress(0, text="Powering up your gains...")
                for p in range(0, 101, 10):
                    prog.progress(p, text=f"Power Level {p}%")
                    time.sleep(0.05)
                prog.empty()
                trainer.speak("🎉 Ghost defeated! +200 NeuroCredits!")
                trainer.award_credits(200)
                trainer.add_xp(500)
        else:
            st.info("Log 2 weeks of workouts to battle your ghost!")

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center; font-size:0.9em; color:#888;'>NeuroLift v2.0 — Powered by NEX-9000 AI • Where iron meets intelligence</p>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

    # Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)