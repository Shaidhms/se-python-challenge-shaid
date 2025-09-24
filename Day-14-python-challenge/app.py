import streamlit as st
import time
import json
from datetime import datetime
import base64
import os

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
        <center> Day 14 - Stop Watch </center>
    </h2>
    """,
    unsafe_allow_html=True
)

# # -*- coding: utf-8 -*-
# """
# SpectraLap
# Stopwatch + Lap tracking with immersive watch themes
# ===================================
# """

st.markdown("""
    <div style="text-align:center; margin-top: 1rem; margin-bottom: 2rem;">
        <h1 style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; color: #00E5FF; text-shadow: 0 0 10px #00E5FF;">
            SpectraLap
        </h1>
        <p style="font-family: 'Poppins', sans-serif; font-size: 0.75rem; color: #ccc; letter-spacing: 1px; margin-top: -10px;">
            Stopwatch + Lap tracking with immersive watch themes.
        </p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'elapsed' not in st.session_state:
    st.session_state.elapsed = 0
if 'laps' not in st.session_state:
    st.session_state.laps = []
if 'sound_enabled' not in st.session_state:
    st.session_state.sound_enabled = False
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.perf_counter()

# ---- Preset persistence (save/load to JSON so they survive refresh) ----
def _preset_file_path():
    try:
        base_dir = os.path.dirname(__file__)
    except Exception:
        base_dir = os.getcwd()
    return os.path.join(base_dir, "mock_presets.json")

def _load_presets_from_disk():
    path = _preset_file_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def _save_presets_to_disk(presets: dict):
    path = _preset_file_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(presets, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ---- Wallpaper selector (realistic watch-themed backdrops) ----
WALLPAPERS = {
    "Carbon Fiber": "https://images.unsplash.com/photo-1518640467707-6811f4a6ab73?q=80&w=1600&auto=format&fit=crop",
    "Brushed Metal": "https://images.unsplash.com/photo-1517445312885-9d5f7d7a3a2a?q=80&w=1600&auto=format&fit=crop",
    "Leather Desk": "https://images.unsplash.com/photo-1512295767273-ac109ac3acfa?q=80&w=1600&auto=format&fit=crop",
    "Wood Desk": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?q=80&w=1600&auto=format&fit=crop",
    "Marble": "https://images.unsplash.com/photo-1522184216315-dc2b7c65c8e8?q=80&w=1600&auto=format&fit=crop",
    "Dark Concrete": "https://images.unsplash.com/photo-1517705008128-361805f42e86?q=80&w=1600&auto=format&fit=crop"
}

with st.sidebar.expander("Wallpaper", expanded=True):
    st.subheader("Wallpaper")
    choice = st.selectbox("Background style", list(WALLPAPERS.keys()), index=0)
    upload = st.file_uploader(
        "Or upload your own image",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        key="wallpaper_upload"
    )

def _css_url_from_upload(uploaded_file):
    if not uploaded_file:
        return None
    try:
        uploaded_file.seek(0)
    except Exception:
        pass
    data = uploaded_file.read()
    if not data:
        # attempt to rewind and read again if empty on rerun
        try:
            uploaded_file.seek(0)
            data = uploaded_file.read()
        except Exception:
            data = b""
    mime = uploaded_file.type or "image/png"
    b64 = base64.b64encode(data).decode()
    return f"data:{mime};base64,{b64}" if data else None

WALLPAPER_CSS_URL = _css_url_from_upload(upload) or WALLPAPERS[choice]

# Persist wallpaper data URL across reruns so it doesn't disappear
if 'wallpaper_dataurl' not in st.session_state:
    st.session_state.wallpaper_dataurl = None
if _css_url_from_upload(upload):
    st.session_state.wallpaper_dataurl = _css_url_from_upload(upload)
if st.session_state.wallpaper_dataurl and (WALLPAPER_CSS_URL == WALLPAPERS[choice]):
    # If user had uploaded previously, prefer persisted upload over preset on rerun
    WALLPAPER_CSS_URL = st.session_state.wallpaper_dataurl

# Preset store for watch mockup settings
if 'mock_presets' not in st.session_state:
    st.session_state.mock_presets = _load_presets_from_disk()

# If a preset was just saved/deleted, apply its selection before rendering the selectbox
if 'pending_select_preset' in st.session_state:
    _pending = st.session_state.pop('pending_select_preset')
    # Only set if valid or special none sentinel
    if _pending == "— none —" or _pending in st.session_state.mock_presets:
        st.session_state['selected_preset'] = _pending

# If a preset application queued new mock values, apply them before rendering number_inputs
if 'pending_mock_values' in st.session_state:
    _pmv = st.session_state.pop('pending_mock_values')
    for _k in ['mock_width', 'mock_height', 'dial_size', 'offset_x', 'offset_y']:
        if _pmv and _k in _pmv:
            try:
                st.session_state[_k] = int(_pmv[_k])
            except Exception:
                st.session_state[_k] = _pmv[_k]

# ---- Watch mockup (render dial inside a real watch image) ----
st.sidebar.markdown("---")

with st.sidebar.expander("Watch Mockup", expanded=True):
    mock_enabled = st.checkbox("Render in watch mockup", value=True)

    # Ensure default values exist in session_state
    st.session_state.setdefault('mock_width', 720)
    st.session_state.setdefault('mock_height', 540)
    st.session_state.setdefault('dial_size', 360)
    st.session_state.setdefault('offset_x', 0)
    st.session_state.setdefault('offset_y', 20)

    # Number inputs bound to session_state keys so we can programmatically update them
    st.number_input(
        "Mockup width (px)", min_value=300, max_value=2000,
        value=st.session_state['mock_width'], step=10, key='mock_width')
    st.number_input(
        "Mockup height (px)", min_value=300, max_value=2000,
        value=st.session_state['mock_height'], step=10, key='mock_height')
    st.number_input(
        "Dial diameter (px)", min_value=120, max_value=1500,
        value=st.session_state['dial_size'], step=5, key='dial_size')
    st.number_input(
        "Dial X offset (px)", min_value=-2000, max_value=2000,
        value=st.session_state['offset_x'], step=1, key='offset_x')
    st.number_input(
        "Dial Y offset (px)", min_value=-2000, max_value=2000,
        value=st.session_state['offset_y'], step=1, key='offset_y')

    # Upload watch image
    watch_img_file = st.file_uploader(
        "Watch image (PNG/JPG)", type=["png", "jpg", "jpeg", "webp"], key="watch_img")

# Presets UI (collapsible)
with st.sidebar.expander("Presets", expanded=True):
    st.text_input("Preset name", key="preset_name", placeholder="e.g., Neon Street")

    # Existing presets selector
    preset_keys = list(st.session_state.mock_presets.keys())
    st.selectbox("Saved presets", ["— none —"] + preset_keys, index=0, key="selected_preset")

    # Full-width buttons stacked to avoid wrapping issues
    st.button("Save preset", key="save_preset_btn", use_container_width=True)
    st.button("Apply preset", key="apply_preset_btn", use_container_width=True)
    st.button("Delete preset", key="delete_preset_btn", use_container_width=True)

# Handle preset button actions outside the expander to keep logic unchanged
if st.session_state.get("save_preset_btn"):
    name = (st.session_state.get('preset_name') or "").strip()
    if name:
        st.session_state.mock_presets[name] = {
            'mock_width': st.session_state['mock_width'],
            'mock_height': st.session_state['mock_height'],
            'dial_size': st.session_state['dial_size'],
            'offset_x': st.session_state['offset_x'],
            'offset_y': st.session_state['offset_y'],
        }
        _save_presets_to_disk(st.session_state.mock_presets)
        # Mark for selection on next run so selectbox options include it
        st.session_state['pending_select_preset'] = name
        st.success(f"Saved preset: {name}")
        st.rerun()
    else:
        st.warning("Enter a preset name before saving.")

if st.session_state.get("apply_preset_btn"):
    name = st.session_state.get('selected_preset')
    if name and name != "— none —" and name in st.session_state.mock_presets:
        p = st.session_state.mock_presets[name]
        # Defer updates until next run to avoid modifying widget-backed keys after render
        st.session_state['pending_mock_values'] = {
            'mock_width': int(p['mock_width']),
            'mock_height': int(p['mock_height']),
            'dial_size': int(p['dial_size']),
            'offset_x': int(p['offset_x']),
            'offset_y': int(p['offset_y']),
        }
        st.rerun()

if st.session_state.get("delete_preset_btn"):
    name = st.session_state.get('selected_preset')
    if name and name in st.session_state.mock_presets:
        del st.session_state.mock_presets[name]
        _save_presets_to_disk(st.session_state.mock_presets)
        # Reset selection on next run (after options refresh)
        st.session_state['pending_select_preset'] = "— none —"
        st.rerun()

# Helper for inlined background image
def _b64_data_url(uploaded_file):
    if not uploaded_file:
        return None
    try:
        uploaded_file.seek(0)
    except Exception:
        pass
    data = uploaded_file.read()
    if not data:
        try:
            uploaded_file.seek(0)
            data = uploaded_file.read()
        except Exception:
            data = b""
    mime = uploaded_file.type or "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}" if data else None

WATCH_IMG_URL = _b64_data_url(st.session_state.get('watch_img'))
# Persist watch image data URL across reruns so it doesn't disappear
if 'watch_img_dataurl' not in st.session_state:
    st.session_state.watch_img_dataurl = None
if WATCH_IMG_URL:
    st.session_state.watch_img_dataurl = WATCH_IMG_URL
else:
    WATCH_IMG_URL = st.session_state.watch_img_dataurl

def get_elapsed():
    """Calculate elapsed time in milliseconds with precision."""
    if st.session_state.running:
        current_time = time.perf_counter()
        elapsed_delta = current_time - st.session_state.last_update
        return st.session_state.elapsed + elapsed_delta
    return st.session_state.elapsed

def start_stopwatch():
    """Start the stopwatch."""
    if not st.session_state.running:
        st.session_state.running = True
        st.session_state.start_time = time.perf_counter()
        st.session_state.last_update = st.session_state.start_time

def stop_stopwatch():
    """Stop the stopwatch."""
    if st.session_state.running:
        current_time = time.perf_counter()
        st.session_state.elapsed += current_time - st.session_state.last_update
        st.session_state.running = False

def reset_stopwatch():
    """Reset the stopwatch to zero."""
    st.session_state.running = False
    st.session_state.elapsed = 0
    st.session_state.laps = []
    st.session_state.last_update = time.perf_counter()

def add_lap():
    """Record a lap time."""
    if st.session_state.running:
        current_time = get_elapsed()
        lap_time = current_time
        if st.session_state.laps:
            lap_time = current_time - st.session_state.laps[-1]['cumulative']
        
        lap_data = {
            'number': len(st.session_state.laps) + 1,
            'lap_time': lap_time,
            'cumulative': current_time,
            'delta': lap_time if not st.session_state.laps else lap_time
        }
        st.session_state.laps.append(lap_data)

def format_time(ms):
    """Format milliseconds to HH:MM:SS.mmm."""
    total_seconds = ms / 1000
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((ms % 1000))
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def toggle_sound():
    """Toggle sound cues."""
    st.session_state.sound_enabled = not st.session_state.sound_enabled

# Custom CSS and JavaScript
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');

:root {
  --neon-cyan: #00E5FF;
  --neon-purple: #8A2BE2;
  --neon-mint: #00FF88;
  --dark-bg: #0a0a1a;
  --glass-bg: rgba(10, 10, 30, 0.6);
  --glass-border: rgba(0, 229, 255, 0.2);
}

[data-testid="stAppViewContainer"] {
 background: radial-gradient(circle at center, #0a0a2a 0%, #000011 70%);
  background-attachment: fixed;
  min-height: 100vh;
  overflow-x: hidden;
}

.main {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.clock-container {
  position: relative;
  width: 350px;
  height: 350px;
  margin: 2rem auto;
}

.clock-face {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle at center, #1a1a2e 0%, #0f0f1e 70%);
  border: 8px solid #2a2a3e;
  box-shadow: 
    0 0 30px rgba(0, 229, 255, 0.5),
    inset 0 0 20px rgba(0, 0, 0, 0.5);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.clock-face::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle at center, transparent 60%, rgba(0, 229, 255, 0.1) 100%);
  pointer-events: none;
}


.hour-marks {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.hour-mark {
  position: absolute;
  width: 4px;
  height: 15px;
  background: var(--neon-cyan);
  left: 50%;
  top: 15px;
  transform-origin: bottom center;
  transform: translateX(-50%);
  box-shadow: 0 0 5px var(--neon-cyan);
}

.hour-mark:nth-child(1) { transform: translateX(-50%) rotate(0deg); }
.hour-mark:nth-child(2) { transform: translateX(-50%) rotate(30deg); }
.hour-mark:nth-child(3) { transform: translateX(-50%) rotate(60deg); }
.hour-mark:nth-child(4) { transform: translateX(-50%) rotate(90deg); }
.hour-mark:nth-child(5) { transform: translateX(-50%) rotate(120deg); }
.hour-mark:nth-child(6) { transform: translateX(-50%) rotate(150deg); }
.hour-mark:nth-child(7) { transform: translateX(-50%) rotate(180deg); }
.hour-mark:nth-child(8) { transform: translateX(-50%) rotate(210deg); }
.hour-mark:nth-child(9) { transform: translateX(-50%) rotate(240deg); }
.hour-mark:nth-child(10) { transform: translateX(-50%) rotate(270deg); }
.hour-mark:nth-child(11) { transform: translateX(-50%) rotate(300deg); }
.hour-mark:nth-child(12) { transform: translateX(-50%) rotate(330deg); }

.digital-display {
  position: absolute;
  font-family: 'Orbitron', monospace;
  font-size: 1.8rem;
  color: var(--neon-cyan);
  text-shadow: 
    0 0 5px var(--neon-cyan),
    0 0 10px var(--neon-cyan);
  text-align: center;
  width: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 5;
  background: rgba(10, 10, 30, 0.7);
  padding: 10px;
  border-radius: 8px;
  letter-spacing: 1px;
}

.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 
    0 0 20px rgba(0, 229, 255, 0.3),
    inset 0 0 20px rgba(0, 229, 255, 0.1);
  width: 100%;
  max-width: 600px;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(138, 43, 226, 0.1), transparent);
  animation: shine 8s infinite;
  z-index: -1;
}

@keyframes shine {
  0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
  100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 2rem 0;
  flex-wrap: wrap;
}

.btn {
  background: transparent;
  border: 2px solid var(--neon-cyan);
  color: var(--neon-cyan);
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-family: 'Orbitron', monospace;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 120px;
  justify-content: center;
}

.btn:hover {
  background: rgba(0, 229, 255, 0.1);
  box-shadow: 0 0 15px var(--neon-cyan);
}

.btn:active {
  transform: scale(0.95);
  box-shadow: 0 0 5px var(--neon-cyan);
}

.btn-primary {
  border-color: var(--neon-mint);
  color: var(--neon-mint);
}

.btn-primary:hover {
  background: rgba(0, 255, 136, 0.1);
  box-shadow: 0 0 15px var(--neon-mint);
}

.btn-reset {
  border-color: var(--neon-purple);
  color: var(--neon-purple);
}

.btn-reset:hover {
  background: rgba(138, 43, 226, 0.1);
  box-shadow: 0 0 15px var(--neon-purple);
}

.lap-table {
  width: 100%;
  margin-top: 2rem;
  overflow-x: auto;
}

.lap-table table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Orbitron', monospace;
  color: var(--neon-cyan);
  background: rgba(10, 10, 30, 0.5);
  border-radius: 10px;
  overflow: hidden;
}

.lap-table th {
  background: rgba(0, 229, 255, 0.1);
  padding: 0.75rem;
  text-align: center;
  border-bottom: 1px solid var(--glass-border);
}

.lap-table td {
  padding: 0.75rem;
  text-align: center;
  border-bottom: 1px solid var(--glass-border);
}

.lap-table tr:last-child td {
  border-bottom: none;
}

.lap-table tr:hover {
  background: rgba(0, 229, 255, 0.1);
}

.scanlines {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 100;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0) 50%,
    rgba(0, 229, 255, 0.03) 50%
  );
  background-size: 100% 4px;
  animation: scan 8s linear infinite;
  opacity: 0.3;
}

@keyframes scan {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

.glitch {
  animation: glitch 0.2s linear;
}

@keyframes glitch {
  0% { transform: translate(0); }
  20% { transform: translate(-3px, 3px); }
  40% { transform: translate(-3px, -3px); }
  60% { transform: translate(3px, 3px); }
  80% { transform: translate(3px, -3px); }
  100% { transform: translate(0); }
}

.pulse {
  animation: pulse 1s infinite alternate;
}

@keyframes pulse {
  from { 
    box-shadow: 
      0 0 10px var(--neon-cyan),
      0 0 20px var(--neon-cyan),
      0 0 30px var(--neon-cyan);
  }
  to { 
    box-shadow: 
      0 0 15px var(--neon-cyan),
      0 0 30px var(--neon-cyan),
      0 0 45px var(--neon-cyan);
  }
}

.running .digital-display {
  animation: pulse 1s infinite alternate;
}

.sound-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  color: var(--neon-cyan);
  font-family: 'Orbitron', monospace;
}

.sound-toggle input {
  width: 16px;
  height: 16px;
  accent-color: var(--neon-cyan);
}

/* Sidebar UX tweaks */
section[data-testid="stSidebar"] .stButton>button { white-space: normal; line-height: 1.2; }
section[data-testid="stSidebar"] .stButton { margin-top: 0.25rem; }

/* Watch mockup container */
.watch-mock {
  position: relative;
  margin: 2rem auto;
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  filter: drop-shadow(0 20px 50px rgba(0,0,0,0.5));
  border-radius: 12px;
  overflow: hidden;
}
.watch-mock .clock-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .clock-container {
    width: 250px;
    height: 250px;
  }
  
  .digital-display {
    font-size: 1.4rem;
  }
  
  .btn {
    padding: 0.5rem 1rem;
    min-width: 100px;
    font-size: 0.9rem;
  }
}
</style>

<div class="scanlines"></div>
""", unsafe_allow_html=True)

# Apply wallpaper override (placed after base CSS so it wins)
def inject_wallpaper(image_url: str):
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.7)), url('{image_url}') center/cover no-repeat fixed !important;
    }}
    </style>
    """, unsafe_allow_html=True)

inject_wallpaper(WALLPAPER_CSS_URL)

# Inject dynamic CSS for mockup sizing/positioning
# Read current mock values from session_state
mw = int(st.session_state['mock_width'])
mh = int(st.session_state['mock_height'])
ds = int(st.session_state['dial_size'])
ox = int(st.session_state['offset_x'])
oy = int(st.session_state['offset_y'])
st.markdown(f"""
<style>
.watch-mock {{
    width: {mw}px;
    height: {mh}px;
    {f"background-image: url('{WATCH_IMG_URL}');" if WATCH_IMG_URL else ''}
}}
.watch-mock .clock-container {{
    width: {ds}px;
    height: {ds}px;
    transform: translate(calc(-50% + {ox}px), calc(-50% + {oy}px));
}}
</style>
""", unsafe_allow_html=True)


# Main app
#st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# Calculate elapsed time
elapsed_ms = get_elapsed() * 1000
time_str = format_time(elapsed_ms)

# Clock container with digital display (optionally inside watch mockup)
clock_html = f"""
<div class=\"clock-container\">
  <div class=\"clock-face\">
    <div class=\"hour-marks\">
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
      <div class=\"hour-mark\"></div>
    </div>
    <div class=\"clock-center\"></div>
    <div class=\"digital-display {'pulse' if st.session_state.running else ''}\">{time_str}</div>
  </div>
</div>
"""

if mock_enabled and WATCH_IMG_URL:
    st.markdown(f"<div class='watch-mock'>{clock_html}</div>", unsafe_allow_html=True)
else:
    st.markdown(clock_html, unsafe_allow_html=True)

# Controls
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button(
        f"{'⏸ STOP' if st.session_state.running else '▶ START'}",
        key="start_stop",
        help="Start or stop the timer",
        type="primary" if st.session_state.running else "secondary"
    ):
        if st.session_state.running:
            stop_stopwatch()
        else:
            start_stopwatch()

with col2:
    if st.button(
        "⟲ RESET",
        key="reset_btn",
        help="Reset the timer",
        type="secondary"
    ):
        reset_stopwatch()

with col3:
    if st.button(
        "⏱ LAP",
        key="lap_btn",
        help="Add a lap",
        type="secondary"
    ):
        add_lap()

# Sound toggle
#st.markdown('<div class="sound-toggle">', unsafe_allow_html=True)
#st.checkbox("Enable Sound Cues", value=st.session_state.sound_enabled, key="sound_toggle", on_change=toggle_sound)
#st.markdown('</div>', unsafe_allow_html=True)

# Laps table
if st.session_state.laps:
    st.markdown('<div class="lap-table">', unsafe_allow_html=True)
    st.subheader("Lap Times")
    
    # Create table headers
    headers = ["#", "Lap Time", "Cumulative", "Delta"]
    table_data = []
    
    for i, lap in enumerate(st.session_state.laps):
        lap_time_str = format_time(lap['lap_time'] * 1000)
        cumulative_str = format_time(lap['cumulative'] * 1000)
        
        # Calculate delta from previous lap
        delta_str = lap_time_str
        if i > 0:
            prev_lap = st.session_state.laps[i-1]
            delta = lap['cumulative'] - prev_lap['cumulative']
            delta_str = format_time(delta * 1000)
        
        table_data.append([
            lap['number'],
            lap_time_str,
            cumulative_str,
            delta_str
        ])
    
    # Display table
    import pandas as pd
    df = pd.DataFrame(table_data, columns=headers)
    st.dataframe(df, use_container_width=True, height=300)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sound cues (HTML5 audio)
if st.session_state.sound_enabled:
    st.components.v1.html("""
    <audio id="tickSound" preload="auto">
      <source src="audio/mpeg;base64,SUQzBAAAAAABEVRYWFgAAAAtAAADY29tbWVudABCaWdTb3VuZEJhbmsuY29tIC8gTGFTb25vdGhlcXVlLm9yZwBURU5DAAAAHQAAA1N3aXRjaCBQbHVzIMKpIE5DSCBTb2Z0d2FyZQBUSVQyAAAABgAAAzIyMzUAVFNTRQAAAA8AAANMYXZmNTcuODMuMTAwAAAAAAAAAAAAAAD/80DEAAAAA0gAAAAATEFNRTMuMTAwVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQsRbAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQMSkAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV" type="audio/mpeg">
    </audio>
    <audio id="blipSound" preload="auto">
      <source src="audio/mpeg;base64,SUQzBAAAAAABEVRYWFgAAAAtAAADY29tbWVudABCaWdTb3VuZEJhbmsuY29tIC8gTGFTb25vdGhlcXVlLm9yZwBURU5DAAAAHQAAA1N3aXRjaCBQbHVzIMKpIE5DSCBTb2Z0d2FyZQBUSVQyAAAABgAAAzIyMzUAVFNTRQAAAA8AAANMYXZmNTcuODMuMTAwAAAAAAAAAAAAAAD/80DEAAAAA0gAAAAATEFNRTMuMTAwVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQsRbAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQMSkAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV" type="audio/mpeg">
    </audio>
    <script>
    function playTick() {
      const audio = document.getElementById('tickSound');
      audio.currentTime = 0;
      audio.play().catch(e => console.log('Audio play error:', e));
    }
    
    function playBlip() {
      const audio = document.getElementById('blipSound');
      audio.currentTime = 0;
      audio.play().catch(e => console.log('Audio play error:', e));
    }
    
    // Play tick sound every second when running
    let lastSecond = -1;
    setInterval(() => {
      if (window.isRunning) {
        const currentSecond = Math.floor(Date.now() / 1000);
        if (currentSecond !== lastSecond) {
          playTick();
          lastSecond = currentSecond;
        }
      }
    }, 100);
    
    // Listen for lap events to play blip
    window.addEventListener('message', (event) => {
      if (event.data.type === 'lapSound') {
        playBlip();
      }
    });
    </script>
    """, height=0)
    
    # Update running state for sound
    st.components.v1.html(f"""
    <script>
    window.isRunning = {str(st.session_state.running).lower()};
    </script>
    """, height=0)

# Trigger lap sound if lap was added
if 'last_lap_count' not in st.session_state:
    st.session_state.last_lap_count = 0

if len(st.session_state.laps) > st.session_state.last_lap_count and st.session_state.sound_enabled:
    st.components.v1.html("""
    <script>
    window.parent.postMessage({type: 'lapSound'}, '*');
    </script>
    """, height=0)
    st.session_state.last_lap_count = len(st.session_state.laps)

# Auto-rerun to update time display
if st.session_state.running:
    time.sleep(0.05)  # Small delay to prevent excessive updates
    st.rerun()

                # Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)