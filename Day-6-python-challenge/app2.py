# app.py
import streamlit as st
import pandas as pd
import sqlite3
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_extras.stylable_container import stylable_container
from streamlit_option_menu import option_menu
import time
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
        <center> Day 5 - Unit Converter</center>
    </h2>
    """,
    unsafe_allow_html=True
)


# Try to import plyer for system notifications
try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False

# === DATABASE SETUP ===
DB_NAME = "hydration_tracker.db"
CONFIG_FILE = "config.json"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        amount REAL,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    conn.close()
    return df

def add_log(amount, target_date=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().isoformat()
    c.execute("INSERT INTO logs (date, amount, timestamp) VALUES (?, ?, ?)",
              (target_date, amount, now))
    conn.commit()
    conn.close()

def get_daily_total(target_date=None):
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM logs WHERE date = ?", (target_date,))
    result = c.fetchone()[0]
    conn.close()
    return result or 0.0

def get_weekly_logs(start_date):
    """Get logs for a 7-day period starting from start_date"""
    end_date = start_date + timedelta(days=6)
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT date, SUM(amount) as total FROM logs WHERE date BETWEEN ? AND ? GROUP BY date ORDER BY date",
        conn,
        params=(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    )
    conn.close()
    
    # Create all dates in the range
    all_dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    df_all = pd.DataFrame({"date": all_dates})
    df = df_all.merge(df, on="date", how="left").fillna(0)
    return df

def export_logs():
    df = get_logs()
    filename = f"hydration_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    return filename

def delete_log(log_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM logs WHERE id = ?", (log_id,))
    conn.commit()
    conn.close()

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"goal": 3.0, "personality": "Friendly Bot", "reminder_interval": 300}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# === ROBOTIC ASSISTANT LOGIC ===
PERSONALITIES = {
    "Friendly Bot": {
        "greeting": "Greetings, operator. Today's hydration cycle has commenced.",
        "progress": "Affirmative. Progress recalibrated to {percent}%. Hydration systems charging.",
        "goal": "Objective complete. Hydration secure. Systems stable.",
        "reminder": "You are at {percent}% of your daily goal. Add ~{needed:.2f} L to reach it!",
        "export": "Logs exported successfully. File saved as: {filename}",
        "log_success": "Intake of {amount}L logged successfully for {date}. Current total: {total:.2f}L",
        "notification": "💧 Time to take a sip of water! Stay hydrated, operator."
    },
    "Strict Drill Sergeant": {
        "greeting": "LISTEN UP! TODAY'S HYDRATION TARGET: {goal} L. CURRENT STATUS: {current:.2f} L.",
        "progress": "ACCEPTABLE. PROGRESS: {percent}%. KEEP DRINKING!",
        "goal": "MISSION ACCOMPLISHED. HYDRATION TARGET MET. DISMISSED.",
        "reminder": "YOU ARE AT {percent}% OF YOUR DAILY GOAL. ADD {needed:.2f} L IMMEDIATELY!",
        "export": "LOGS EXPORTED. FILE: {filename}. REPORT TO HQ.",
        "log_success": "RECORDED: {amount}L for {date}. TOTAL NOW: {total:.2f}L. NEXT!",
        "notification": "💧 ATTENTION! HYDRATION REMINDER! DRINK NOW!"
    },
    "Zen Monk": {
        "greeting": "Peace be with you. Today's fluid journey begins now.",
        "progress": "Balance restored. Hydration level: {percent}%. Breathe deeply.",
        "goal": "Harmony achieved. The vessel is full. Inner calm flows.",
        "reminder": "Your path is {percent}% complete. Pour {needed:.2f} L more for balance.",
        "export": "Your logs have been preserved. File name: {filename}. Walk in peace.",
        "log_success": "Mindfully recorded {amount}L for {date}. Your total flows at {total:.2f}L",
        "notification": "💧 Mindful reminder: Take a gentle sip of water. Flow like water, be like water."
    },
    "Cyberpunk AI": {
        "greeting": "[SYSTEM BOOT] Hydration Protocol v2.3 initialized. Target: {goal} L.",
        "progress": "[UPDATE] Fluid intake recalculated. Efficiency: {percent}%. Continue.",
        "goal": "[SUCCESS] Hydration matrix complete. All systems nominal.",
        "reminder": "[WARNING] Hydration deficit detected. {needed:.2f} L required for optimal function.",
        "export": "[EXPORT COMPLETE] Logs archived. Filename: {filename}. Encrypting...",
        "log_success": "[LOGGED] {amount}L for {date}. System total: {total:.2f}L. Efficiency maintained.",
        "notification": "[ALERT] Hydration protocol active. Recommended fluid intake. Proceed immediately."
    }
}

def get_bot_message(key, **kwargs):
    personality = st.session_state.get("personality", "Friendly Bot")
    template = PERSONALITIES[personality].get(key, "")
    return template.format(**kwargs)

def show_notification():
    """Show notification with 20-second duration"""
    notification_msg = get_bot_message("notification")
    
    # Try system notification first with 20 seconds timeout
    if NOTIFICATIONS_AVAILABLE:
        try:
            notification.notify(
                title="💧 Hydration Reminder",
                message=notification_msg,
                timeout=20  # 20 seconds duration
            )
            return True
        except Exception as e:
            print(f"System notification failed: {e}")
            pass
    
    # Generate unique ID for this notification
    notif_id = f"hydration-notification-{int(time.time() * 1000)}"
    
    # Store notification in session state
    st.session_state.current_notification = {
        'id': notif_id,
        'message': notification_msg,
        'timestamp': time.time()
    }

def display_notification():
    """Display the current notification if it exists"""
    if 'current_notification' in st.session_state and st.session_state.current_notification:
        notif = st.session_state.current_notification
        notif_id = notif['id']
        notification_msg = notif['message']
        
        st.markdown(f"""
        <div id="{notif_id}" style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(145deg, #1a1a2e, #16213e);
            border: 2px solid #00f7ff;
            border-radius: 12px;
            padding: 20px;
            color: #00f7ff;
            font-family: 'Orbitron', sans-serif;
            z-index: 9999;
            box-shadow: 0 0 30px #00f7ff;
            max-width: 350px;
            animation: pulse 2s infinite;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; font-size: 18px;">💧 HYDRATION REMINDER</h3>
                <button onclick="document.getElementById('{notif_id}').style.display='none'" 
                        style="background: transparent; border: 1px solid #ff00ff; color: #ff00ff; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; font-weight: bold;">
                    ✕
                </button>
            </div>
            <p style="margin: 10px 0 0 0; font-size: 14px;">{notification_msg}</p>
        </div>
        <script>
            // Auto-hide after 20 seconds
            setTimeout(function() {{
                var notif = document.getElementById('{notif_id}');
                if (notif) {{
                    notif.style.opacity = '0';
                    setTimeout(function() {{
                        notif.style.display = 'none';
                    }}, 500);
                }}
            }}, 20000);
        </script>
        """, unsafe_allow_html=True)

# === CUSTOM CSS ===
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Exo+2:wght@300;600&display=swap');

    :root {
        --neon-aqua: #00f7ff;
        --neon-green: #39ff14;
        --cyber-pink: #ff00ff;
        --dark-bg: #0d0d1a;
        --panel-bg: rgba(13, 13, 26, 0.7);
    }

    body {
        background-color: var(--dark-bg);
        color: #ffffff;
        font-family: 'Exo 2', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: var(--neon-aqua);
        text-shadow: 0 0 10px var(--neon-aqua);
    }

    .stButton>button {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        color: var(--neon-green);
        border: 1px solid var(--neon-green);
        border-radius: 8px;
        font-family: 'Orbitron', sans-serif;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        box-shadow: 0 0 15px var(--neon-green);
        transform: scale(1.05);
    }

    .stButton>button:disabled {
        background: #2a2a3a;
        color: #666;
        border: 1px solid #444;
        cursor: not-allowed;
    }

    .glass-panel {
        background: rgba(13, 13, 26, 0.6);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(0, 247, 255, 0.3);
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .hud-ring {
        position: relative;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: conic-gradient(var(--neon-aqua) {percent}%, #1a1a2e 0%);
        margin: 20px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px var(--neon-aqua);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 20px var(--neon-aqua); }
        50% { box-shadow: 0 0 30px var(--neon-aqua), 0 0 40px var(--neon-green); }
        100% { box-shadow: 0 0 20px var(--neon-aqua); }
    }

    .hud-center {
        width: 160px;
        height: 160px;
        background-color: var(--dark-bg);
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'Orbitron', sans-serif;
        color: var(--neon-green);
    }

    .chat-bubble {
        background: rgba(13, 13, 26, 0.8);
        border-left: 4px solid var(--cyber-pink);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-family: 'Exo 2', sans-serif;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
    }

    .chat-input {
        background: rgba(26, 26, 46, 0.7);
        border: 1px solid var(--neon-aqua);
        border-radius: 8px;
        padding: 10px;
        color: white;
    }

    .chat-input:focus {
        outline: none;
        box-shadow: 0 0 10px var(--neon-aqua);
    }

    .success-message {
        color: var(--neon-green);
        font-weight: bold;
        text-shadow: 0 0 8px var(--neon-green);
    }
    
    .date-navigation {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin: 20px 0;
    }
    
    .date-btn {
        background: rgba(26, 26, 46, 0.7);
        border: 1px solid var(--neon-aqua);
        color: var(--neon-aqua);
        border-radius: 8px;
        padding: 8px 15px;
        cursor: pointer;
        font-family: 'Orbitron', sans-serif;
    }
    
    .date-btn:hover {
        background: rgba(0, 247, 255, 0.2);
    }
    
    .date-display {
        font-family: 'Orbitron', sans-serif;
        font-size: 20px;
        color: var(--neon-green);
        text-shadow: 0 0 8px var(--neon-green);
        min-width: 300px;
        text-align: center;
    }
    
    .today-btn {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        color: var(--neon-green);
        border: 1px solid var(--neon-green);
        border-radius: 8px;
        font-family: 'Orbitron', sans-serif;
        padding: 8px 15px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .today-btn:hover {
        box-shadow: 0 0 15px var(--neon-green);
        transform: scale(1.05);
    }
    
    .week-navigation {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin: 10px 0;
    }
    
    .week-display {
        font-family: 'Orbitron', sans-serif;
        font-size: 16px;
        color: var(--neon-aqua);
        text-shadow: 0 0 5px var(--neon-aqua);
        min-width: 250px;
        text-align: center;
    }
    
    .clear-chat-btn {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        color: var(--cyber-pink);
        border: 1px solid var(--cyber-pink);
        border-radius: 8px;
        font-family: 'Orbitron', sans-serif;
        padding: 5px 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 12px;
        margin-left: 10px;
    }
    
    .clear-chat-btn:hover {
        box-shadow: 0 0 15px var(--cyber-pink);
        transform: scale(1.05);
    }
    
    .chat-form-container {
        display: flex;
        gap: 10px;
        align-items: flex-end;
    }
    
    .chat-input-container {
        flex-grow: 1;
    }
    
    .status-indicator {
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
    }
    
    .status-active {
        background: rgba(57, 255, 20, 0.1);
        border: 1px solid var(--neon-green);
        color: var(--neon-green);
    }
    
    .status-inactive {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid #ff0000;
        color: #ff0000;
    }
    
    /* Auto-refresh styling */
    .auto-refresh-info {
        background: rgba(26, 26, 46, 0.7);
        border: 1px solid var(--neon-aqua);
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
        font-family: 'Exo 2', sans-serif;
        font-size: 12px;
        text-align: center;
    }
    
    .enable-btn {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        color: var(--neon-green);
        border: 1px solid var(--neon-green);
        border-radius: 8px;
        font-family: 'Orbitron', sans-serif;
        padding: 8px 15px;
        cursor: pointer;
        width: 100%;
        margin: 5px 0;
    }
    
    .disable-btn {
        background: linear-gradient(145deg, #2a1a1e, #21161e);
        color: #ff4d4d;
        border: 1px solid #ff4d4d;
        border-radius: 8px;
        font-family: 'Orbitron', sans-serif;
        padding: 8px 15px;
        cursor: pointer;
        width: 100%;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# === DATE NAVIGATION ===
def date_navigation():
    col1, col2, col3, col4 = st.columns([1,3,1,3.5])
    
    with col1:
        if st.button("◀ Previous"):
            st.session_state.current_date -= timedelta(days=1)
    
    with col2:
        st.markdown(f"<div class='date-display'>{st.session_state.current_date.strftime('%A, %B %d, %Y')}</div>", unsafe_allow_html=True)
  
    with col3:
         # Grey out next button for future dates
        is_future = st.session_state.current_date >= datetime.now().date()
        if st.button("Next ▶", disabled=is_future):
            if not is_future:
                st.session_state.current_date += timedelta(days=1)        
    with col4:
        if st.button("Today"):
            st.session_state.current_date = datetime.now().date()

# === WEEK NAVIGATION ===
def week_navigation():
    col1, col2, col3 = st.columns([1,2,1])
    
    with col1:
        if st.button("◀ Prev Week"):
            st.session_state.week_start_date -= timedelta(days=7)
    
    with col2:
        week_end_date = st.session_state.week_start_date + timedelta(days=6)
        st.markdown(f"<div class='week-display'>{st.session_state.week_start_date.strftime('%b %d')} - {week_end_date.strftime('%b %d, %Y')}</div>", unsafe_allow_html=True)
    
    with col3:
        # Only allow next week if it doesn't go beyond current week
        current_week_start = datetime.now().date() - timedelta(days=datetime.now().weekday())
        is_future = st.session_state.week_start_date >= current_week_start
        if st.button("Next Week ▶", disabled=is_future):
            if not is_future:
                st.session_state.week_start_date += timedelta(days=7)

# === CLEAR BOT CHAT ===
def clear_bot_chat():
    """Clear all bot messages and add a fresh greeting"""
    st.session_state.bot_messages = [
        get_bot_message("greeting", goal=st.session_state.goal, current=get_daily_total())
    ]

# === PARSE LOG COMMAND ===
def parse_log_command(text):
    """Parse commands like 'log 0.5L' or 'add 1.2 liters'"""
    text = text.lower().strip()
    
    # Patterns to match
    import re
    
    # Pattern 1: "log 0.5L" or "log 1.2 liters"
    log_pattern = r'(?:log|add|record)\s+(\d*\.?\d+)\s*(?:l|liters?|litres?)'
    match = re.search(log_pattern, text)
    
    if match:
        try:
            amount = float(match.group(1))
            return amount
        except ValueError:
            return None
    
    # Pattern 2: "0.5L" or "1.2 liters"
    amount_pattern = r'(\d*\.?\d+)\s*(?:l|liters?|litres?)'
    match = re.search(amount_pattern, text)
    
    if match:
        try:
            amount = float(match.group(1))
            return amount
        except ValueError:
            return None
    
    return None

# === MAIN APP ===
def main():
    st.set_page_config(page_title="Water Intake Tracker 💧🤖", layout="wide")
    inject_custom_css()
    init_db()
    
    # Initialize session state
    if "current_date" not in st.session_state:
        st.session_state.current_date = datetime.now().date()
    if "week_start_date" not in st.session_state:
        # Set to the start of the current week (Monday)
        st.session_state.week_start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
    if "goal" not in st.session_state:
        st.session_state.goal = 3.0
    if "personality" not in st.session_state:
        st.session_state.personality = "Friendly Bot"
    if "bot_messages" not in st.session_state:
        st.session_state.bot_messages = [get_bot_message("greeting", goal=st.session_state.goal, current=get_daily_total())]
    if "needs_rerun" not in st.session_state:
        st.session_state.needs_rerun = False
    if "reminder_interval" not in st.session_state:
        st.session_state.reminder_interval = 300  # Default 5 minutes (300 seconds)
    if "last_reminder" not in st.session_state:
        st.session_state.last_reminder = datetime.now()
    if "reminder_active" not in st.session_state:
        st.session_state.reminder_active = False
    if "show_test_notification" not in st.session_state:
        st.session_state.show_test_notification = False
    if "auto_refresh_count" not in st.session_state:
        st.session_state.auto_refresh_count = 0
    if "current_notification" not in st.session_state:
        st.session_state.current_notification = None

    # Load config
    config = load_config()
    if "goal" not in st.session_state:
        st.session_state.goal = config.get("goal", 3.0)
    if "personality" not in st.session_state:
        st.session_state.personality = config.get("personality", "Friendly Bot")
    if "reminder_interval" not in st.session_state:
        st.session_state.reminder_interval = config.get("reminder_interval", 300)
    if "bot_messages" not in st.session_state:
        st.session_state.bot_messages = [get_bot_message("greeting", goal=st.session_state.goal, current=get_daily_total())]

    # Check for reminder - this will run on every page load
    if st.session_state.reminder_active:
        time_since_last = (datetime.now() - st.session_state.last_reminder).seconds
        if time_since_last >= st.session_state.reminder_interval:
            show_notification()
            st.session_state.last_reminder = datetime.now()
            st.session_state.needs_rerun = True

    # Show test notification if requested
    if st.session_state.show_test_notification:
        show_notification()
        st.session_state.show_test_notification = False
        st.session_state.needs_rerun = True

    # Handle rerun
    if st.session_state.needs_rerun:
        st.session_state.needs_rerun = False
        st.rerun()

    # Display any pending notification
    display_notification()

    # Clear notification from session state after displaying
    if 'current_notification' in st.session_state and st.session_state.current_notification:
        st.session_state.current_notification = None

    # Sidebar
    with st.sidebar:
        st.title("🔧 Control Panel")
        
        goal = st.slider("Daily Goal (L)", 0.5, 10.0, st.session_state.goal, 0.1, key="goal_slider")
        if goal != st.session_state.goal:
            st.session_state.goal = goal
            save_config({
                "goal": goal, 
                "personality": st.session_state.personality,
                "reminder_interval": st.session_state.reminder_interval
            })
            
        personality = st.selectbox("Bot Personality", list(PERSONALITIES.keys()), index=list(PERSONALITIES.keys()).index(st.session_state.personality))
        if personality != st.session_state.personality:
            st.session_state.personality = personality
            save_config({
                "goal": st.session_state.goal, 
                "personality": personality,
                "reminder_interval": st.session_state.reminder_interval
            })
            st.session_state.bot_messages.append(get_bot_message("greeting", goal=goal, current=get_daily_total()))
            
        # Reminder settings
        st.subheader("🔔 Reminder Settings")
        reminder_options = {
            "Every 5 minutes": 300,
            "Every 10 minutes": 600,
            "Every 15 minutes": 900,
            "Every 30 minutes": 1800,
            "Every hour": 3600,
            "Disabled": 0
        }
        
        selected_interval = st.selectbox(
            "Reminder Frequency",
            list(reminder_options.keys()),
            index=list(reminder_options.values()).index(st.session_state.reminder_interval) if st.session_state.reminder_interval in reminder_options.values() else 0
        )
        
        new_interval = reminder_options[selected_interval]
        if new_interval != st.session_state.reminder_interval:
            st.session_state.reminder_interval = new_interval
            if new_interval > 0:
                st.session_state.last_reminder = datetime.now()
            save_config({
                "goal": st.session_state.goal, 
                "personality": st.session_state.personality,
                "reminder_interval": new_interval
            })
            
        # Status indicator and control buttons
        if st.session_state.reminder_interval > 0:
            status = "🟢 Active" if st.session_state.reminder_active else "🔴 Inactive"
            status_class = "status-active" if st.session_state.reminder_active else "status-inactive"
            st.markdown(f'<div class="status-indicator {status_class}">Status: {status}</div>', unsafe_allow_html=True)
            
            # Enable/Disable buttons
            if not st.session_state.reminder_active:
                if st.button("Enable Reminders", key="enable_reminders", use_container_width=True):
                    st.session_state.reminder_active = True
                    st.session_state.last_reminder = datetime.now()
                    st.rerun()
            else:
                if st.button("Disable Reminders", key="disable_reminders", use_container_width=True):
                    st.session_state.reminder_active = False
                    st.rerun()
            
            # Test notification button
            if st.button("Test Notification", use_container_width=True):
                st.session_state.show_test_notification = True
                st.rerun()
                
            # Auto-refresh info
            st.markdown('<div class="auto-refresh-info">🔄 App auto-checks for reminders on each interaction</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-inactive">Status: 🔴 Disabled</div>', unsafe_allow_html=True)
            
        if st.button("Export Logs"):
            filename = export_logs()
            st.session_state.bot_messages.append(get_bot_message("export", filename=filename))
            
        st.markdown('</div>', unsafe_allow_html=True)

    # Main Content
    st.markdown("<h1 style='text-align: center;'>💧 Water Intake Tracker 💧🤖</h1>", unsafe_allow_html=True)    
    
    # Date Navigation
    date_navigation()
    
    # Progress HUD for selected date
    current = get_daily_total(st.session_state.current_date.strftime("%Y-%m-%d"))
    percent = min(100, int((current / st.session_state.goal) * 100))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="glass-panel">
            <h2>Today's Hydration</h2>
            <div class="hud-ring" style="background: conic-gradient(var(--neon-aqua) {percent}%, #1a1a2e 0%);">
                <div class="hud-center">
                    <div style="font-size: 24px;">{percent}%</div>
                    <div style="font-size: 16px; color: #aaa;">{current:.2f} / {st.session_state.goal} L</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Add for selected date
        st.subheader("💧 Quick Log")
        cols = st.columns([1,1,1,1,1])
        amounts = [0.1, 0.25, 0.5, 0.75, 1.0]
        for i, amt in enumerate(amounts):
            if cols[i].button(f"+{amt}L"):
                add_log(amt, st.session_state.current_date.strftime("%Y-%m-%d"))
                st.session_state.needs_rerun = True
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Manual Entry for selected date (moved below quick log)
        st.subheader("➕ Manual Entry")
        with st.form("manual_entry"):
            amount = st.number_input("Amount (L)", min_value=0.0, step=0.1, value=0.25, key="manual_amount")
            submitted = st.form_submit_button("Log Intake")
            if submitted:
                add_log(amount, st.session_state.current_date.strftime("%Y-%m-%d"))
                st.session_state.needs_rerun = True
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Weekly Chart with Navigation (moved below manual entry)
        st.subheader("📅 Weekly Overview")
        
        # Week Navigation
        week_navigation()
        
        # Get weekly data
        weekly_df = get_weekly_logs(st.session_state.week_start_date)
        fig = px.bar(
            weekly_df,
            x="date",
            y="total",
            labels={"total": "Liters", "date": "Date"},
            color_discrete_sequence=["#00f7ff"]
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # History Table
        st.subheader("📜 Intake History")
        logs_df = get_logs()
        if not logs_df.empty:
            # Filter logs for current date
            current_date_str = st.session_state.current_date.strftime("%Y-%m-%d")
            date_logs = logs_df[logs_df['date'] == current_date_str].copy()
            if not date_logs.empty:
                # Format timestamp to include date and time
                date_logs['formatted_timestamp'] = pd.to_datetime(date_logs['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Display table with delete buttons
                for idx, row in date_logs.iterrows():
                    col1, col2, col3 = st.columns([3,1,1])
                    with col1:
                        st.write(f"🕒 {row['formatted_timestamp']}")
                    with col2:
                        st.write(f"💧 {row['amount']} L")
                    with col3:
                        if st.button("❌", key=f"delete_{row['id']}"):
                            delete_log(row['id'])
                            st.session_state.needs_rerun = True
                            st.rerun()
            else:
                st.info("No intake records for this date.")
        else:
            st.info("No intake records yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat Pod
    st.subheader("🤖 Hydration Bot")
    
    # Display messages (show last 10 messages)
    for msg in st.session_state.bot_messages[-10:]:
        st.markdown(f'<div class="chat-bubble">{msg}</div>', unsafe_allow_html=True)
    
    # User input with clear button next to send
    with st.form("chat_form", clear_on_submit=True):
        st.markdown('<div class="chat-form-container">', unsafe_allow_html=True)
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        user_input = st.text_input("", placeholder="Ask me anything or say 'log 0.5L'...", key="chat_input", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1,10])
        with col1:
            submitted = st.form_submit_button("Send")
        with col2:
            if st.form_submit_button("Clear 💬"):
                clear_bot_chat()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submitted and user_input:
            user_input = user_input.lower()
            current = get_daily_total(st.session_state.current_date.strftime("%Y-%m-%d"))
            percent = min(100, int((current / st.session_state.goal) * 100))
            needed = max(0, st.session_state.goal - current)
            
            # Check if this is a log command
            amount_to_log = parse_log_command(user_input)
            if amount_to_log is not None:
                # Log the amount
                add_log(amount_to_log, st.session_state.current_date.strftime("%Y-%m-%d"))
                new_total = get_daily_total(st.session_state.current_date.strftime("%Y-%m-%d"))
                response = get_bot_message("log_success", 
                                         amount=amount_to_log, 
                                         date=st.session_state.current_date.strftime("%Y-%m-%d"),
                                         total=new_total)
                st.session_state.needs_rerun = True
            elif "how much" in user_input or "need" in user_input:
                response = get_bot_message("reminder", percent=percent, needed=needed)
            elif "week" in user_input or "report" in user_input:
                response = f"📊 Weekly Report: {weekly_df['total'].sum():.2f}L consumed over the last 7 days."
            elif "export" in user_input:
                filename = export_logs()
                response = get_bot_message("export", filename=filename)
            elif "clear" in user_input or "reset" in user_input:
                clear_bot_chat()
                response = "Chat history cleared. Starting fresh conversation."
            elif "reminder" in user_input or "notify" in user_input:
                if "disable" in user_input or "off" in user_input:
                    st.session_state.reminder_active = False
                    response = "💧 Reminder notifications have been disabled."
                elif "enable" in user_input or "on" in user_input:
                    st.session_state.reminder_active = True
                    st.session_state.last_reminder = datetime.now()
                    response = "💧 Reminder notifications have been enabled."
                elif "test" in user_input:
                    st.session_state.show_test_notification = True
                    response = "💧 Test notification triggered!"
                else:
                    response = "💧 You can control reminders by saying 'enable reminders', 'disable reminders', or 'test notification'. You can also adjust frequency in the sidebar."
            else:
                response = "💧 I'm a hydration bot. You can ask me about your water intake, goals, or reports. Or tell me to log water like 'log 0.5L'!"
                
            st.session_state.bot_messages.append(f"👤 You: {user_input}")
            st.session_state.bot_messages.append(f"🤖 Bot: {response}")
            if amount_to_log is not None or st.session_state.show_test_notification:
                st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
     

if __name__ == "__main__":
    main()

 
# Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)  