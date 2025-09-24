import streamlit as st
import random
from pathlib import Path
import requests
from io import BytesIO
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
        <center> Day 13 - Rock-Paper-Scissors </center>
    </h2>
    """,
    unsafe_allow_html=True
)

# Page config
st.set_page_config(
    page_title="Robo RPS",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for futuristic theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Orbitron', monospace;
    }
    
    .main {
        background-color: #0a0a0a;
        color: #f0f0f0;
    }
    
    .stApp {
        background-color: #0a0a0a;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(26, 26, 26, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 20px rgba(0, 255, 255, 0.1);
    }
    
    /* Neon buttons */
    .neon-btn {
        background: rgba(26, 26, 26, 0.7);
        border: 1px solid #00ffff;
        color: #00ffff;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'Orbitron', monospace;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
        margin: 5px;
    }
    
    .neon-btn:hover {
        background: rgba(0, 255, 255, 0.1);
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        transform: translateY(-2px);
    }
    
    .neon-btn:active {
        transform: translateY(1px);
    }
    
    /* Result banner animation */
    @keyframes pulse {
        0% { box-shadow: 0 0 5px #00ffff; }
        50% { box-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff; }
        100% { box-shadow: 0 0 5px #00ffff; }
    }
    
    .result-banner {
        background: rgba(26, 26, 26, 0.9);
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 15px 0;
        animation: pulse 2s infinite;
    }
    
    .win { color: #00ffff; }
    .lose { color: #ff00ff; }
    .draw { color: #ffff00; }
    
    /* Score display */
    .score-container {
        display: flex;
        justify-content: space-around;
        padding: 10px;
        font-size: 18px;
        border-top: 1px solid rgba(0, 255, 255, 0.3);
    }
    
    /* Grid background */
    .grid-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            linear-gradient(rgba(10, 10, 10, 0.9), rgba(10, 10, 10, 0.9)),
            repeating-linear-gradient(0deg, transparent, transparent 1px, rgba(0, 255, 255, 0.05) 1px, rgba(0, 255, 255, 0.05) 2px),
            repeating-linear-gradient(90deg, transparent, transparent 1px, rgba(0, 255, 255, 0.05) 1px, rgba(0, 255, 255, 0.05) 2px);
        z-index: -1;
    }
    
    /* Status message styling */
    .status-message {
        font-style: italic;
        color: #aaa;
        text-align: center;
        margin-top: 10px;
    }
    
    /* GIF container */
    .gif-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    .gif-placeholder {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        background: rgba(30, 30, 30, 0.5);
        border: 1px dashed #00ffff;
        border-radius: 8px;
        color: #00ffff;
        font-size: 14px;
        text-align: center;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Create grid background
st.markdown('<div class="grid-bg"></div>', unsafe_allow_html=True)

# Initialize session state
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'cpu_score' not in st.session_state:
    st.session_state.cpu_score = 0
if 'draws' not in st.session_state:
    st.session_state.draws = 0
if 'player_choice' not in st.session_state:
    st.session_state.player_choice = None
if 'cpu_choice' not in st.session_state:
    st.session_state.cpu_choice = None
if 'result' not in st.session_state:
    st.session_state.result = None
if 'status_message' not in st.session_state:
    st.session_state.status_message = "System ready. Select your move."
if 'pending_result' not in st.session_state:
    st.session_state.pending_result = None
if 'reveal_at' not in st.session_state:
    st.session_state.reveal_at = None
if 'player_name' not in st.session_state:
    st.session_state.player_name = "You"
if 'history' not in st.session_state:
    st.session_state.history = []

# Match session variables
if 'total_rounds' not in st.session_state:
    st.session_state.total_rounds = 3  # default: Best of 3
if 'rounds_played' not in st.session_state:
    st.session_state.rounds_played = 0
if 'match_over' not in st.session_state:
    st.session_state.match_over = False
if 'match_winner' not in st.session_state:
    st.session_state.match_winner = None

# Game constants
MOVES = ["rock", "paper", "scissors"]

# Define GIF URLs (replace with your actual URLs)
GIF_URLS = {
    "player_rock": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZmY4YzF2cjE4c2lld2EycXVoNWMwam9iNzhtdTZ2cnZybG1mZTFleSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/8YcJb8tW47SxYUZUQy/giphy.gif",
    "player_paper": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2k0eDIwMHA0YmVkOHIydTZxOTI3MTk1am43c21zY29udWg5NGkwYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9bJ2OJyi9quJAT81HC/giphy.gif",
    "player_scissors": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZmY4YzF2cjE4c2lld2EycXVoNWMwam9iNzhtdTZ2cnZybG1mZTFleSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/RD3QScf0fgktocr353/giphy.gif",
    "cpu_rock": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGFvem91ejdzYXRtZnV1a3RsdjRkOTM0Y3Q0OHY4MGl1MmRuMzZwcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dAc4wOoFRNKNfgF9Zh/giphy.gif",
    "cpu_paper": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ajZwdmNyOXl2MHl3M211Z3UwNXNxdWplaGs4eWhhcG90dWFxa3Q1cSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/XeY4vs0zXUh99pJo1g/giphy.gif",
    "cpu_scissors": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ajZwdmNyOXl2MHl3M211Z3UwNXNxdWplaGs4eWhhcG90dWFxa3Q1cSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/iFUrGtG2udD4yGAVyX/giphy.gif",
}

# Function to get robot quips
def get_robot_quip(result, player_move, cpu_move, player_name: str | None = None):
    if player_name is None:
        player_name = st.session_state.get("player_name", "Player")
    quips = {
        "win": [
            f"SYSTEM: {player_name}'s {player_move} crushes CPU's {cpu_move}. Victory achieved.",
            f"ANALYSIS: {player_name} outmaneuvered CPU. {player_move.capitalize()} trumps {cpu_move}.",
            f"LOG: {player_name} wins. {player_move.capitalize()} defeats {cpu_move}."
        ],
        "lose": [
            f"SYSTEM: CPU's {cpu_move} defeats {player_name}'s {player_move}. Strategic failure.",
            f"ANALYSIS: CPU executed superior strategy. {cpu_move.capitalize()} overcomes {player_move}.",
            f"LOG: CPU wins. {cpu_move.capitalize()} trumps {player_move}."
        ],
        "draw": [
            f"SYSTEM: Both selected {player_move}. No winner this round.",
            f"ANALYSIS: Synchronized moves detected. {player_move.capitalize()} vs {cpu_move}.",
            f"LOG: Draw. Both chose {player_move}."
        ]
    }
    return random.choice(quips[result])

# Function to decide winner
def decide_winner(player, cpu):
    if player == cpu:
        return "draw"
    elif (player == "rock" and cpu == "scissors") or \
         (player == "paper" and cpu == "rock") or \
         (player == "scissors" and cpu == "paper"):
        return "win"
    else:
        return "lose"

# Function to load GIF from URL with error handling
@st.cache_data(show_spinner=False, ttl=60)
def load_gif_from_url(url):
    """Fetch GIF bytes with a browser-like header; if fetching fails, return the URL so Streamlit can load it directly in the client."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    }
    try:
        resp = requests.get(url, timeout=12, headers=headers, allow_redirects=True)
        ctype = resp.headers.get("Content-Type", "")
        if resp.status_code == 200 and (ctype.startswith("image/") or ctype == "application/octet-stream"):
            return resp.content
        # Non-image response: let the browser fetch it directly
        return url
    except Exception:
        # Fallback to URL so the front-end can still try to load it
        return url

# Helper to reset a match
def reset_match(keep_mode: bool = True):
    """Reset scores and round counters for a new match."""
    st.session_state.player_score = 0
    st.session_state.cpu_score = 0
    st.session_state.draws = 0
    st.session_state.player_choice = None
    st.session_state.cpu_choice = None
    st.session_state.result = None
    st.session_state.pending_result = None
    st.session_state.reveal_at = None
    st.session_state.history = []
    st.session_state.rounds_played = 0
    st.session_state.match_over = False
    st.session_state.match_winner = None
    if not keep_mode:
        st.session_state.total_rounds = 3
    st.session_state.status_message = "System reset. Select your move."

# Header
st.markdown("<h1 style='text-align: center; color: #00ffff; text-shadow: 0 0 10px #00ffff;'>ROBO RPS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ff00ff;'>ROCK • PAPER • SCISSORS</h3>", unsafe_allow_html=True)
 # Player name input
st.text_input("Player name", key="player_name", placeholder="Enter your name")

# Match format selector
mode = st.radio(
    "Match format",
    ["Best of 3", "Best of 5"],
    index=0 if st.session_state.total_rounds == 3 else 1,
    horizontal=True,
)
desired_rounds = 3 if mode == "Best of 3" else 5
if desired_rounds != st.session_state.total_rounds:
    st.session_state.total_rounds = desired_rounds
    reset_match(keep_mode=True)
    st.success(f"Match format set to {mode}. New match started.")

# Main game area
col1, col2 = st.columns(2)

with col1:
    #st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #00ffff;'>{st.session_state.player_name.upper()}</h3>", unsafe_allow_html=True)
    
    # Player move display
    if st.session_state.player_choice:
        gif_url = GIF_URLS.get(f"player_{st.session_state.player_choice}")
        if gif_url:
            gif_data = load_gif_from_url(gif_url)
            if gif_data:
                st.image(gif_data, width=150, caption=f"{st.session_state.player_name}: {st.session_state.player_choice.capitalize()}")
            else:
                st.markdown(f'<div class="gif-placeholder">ERROR LOADING PLAYER {st.session_state.player_choice.upper()}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="gif-placeholder">NO URL FOR PLAYER {st.session_state.player_choice.upper()}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="gif-placeholder">SELECT YOUR MOVE</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    #st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #ff00ff;'>CPU</h3>", unsafe_allow_html=True)
    
    # CPU move display
    if st.session_state.cpu_choice:
        gif_url = GIF_URLS.get(f"cpu_{st.session_state.cpu_choice}")
        if gif_url:
            gif_data = load_gif_from_url(gif_url)
            if gif_data:
                st.image(gif_data, width=150, caption=f"CPU: {st.session_state.cpu_choice.capitalize()}")
            else:
                st.markdown(f'<div class="gif-placeholder">ERROR LOADING CPU {st.session_state.cpu_choice.upper()}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="gif-placeholder">NO URL FOR CPU {st.session_state.cpu_choice.upper()}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="gif-placeholder">CPU THINKING...</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# Move selection buttons (single location)
st.markdown("<h4 style='text-align: center; color: #ffff00;'>SELECT YOUR MOVE</h4>", unsafe_allow_html=True)

if not st.session_state.match_over:
    button_col1, button_col2, button_col3 = st.columns(3)

    with button_col1:
        if st.button("🪨 ROCK", key="rock", use_container_width=True):
            cpu_choice = random.choice(MOVES)
            st.session_state.player_choice = "rock"
            st.session_state.cpu_choice = cpu_choice
            result = decide_winner("rock", cpu_choice)
            st.session_state.pending_result = result
            st.session_state.result = None
            st.session_state.reveal_at = time.time() + 1.5
            st.session_state.status_message = "Animating... calculating outcome"

    with button_col2:
        if st.button("📄 PAPER", key="paper", use_container_width=True):
            cpu_choice = random.choice(MOVES)
            st.session_state.player_choice = "paper"
            st.session_state.cpu_choice = cpu_choice
            result = decide_winner("paper", cpu_choice)
            st.session_state.pending_result = result
            st.session_state.result = None
            st.session_state.reveal_at = time.time() + 1.5
            st.session_state.status_message = "Animating... calculating outcome"

    with button_col3:
        if st.button("✂️ SCISSORS", key="scissors", use_container_width=True):
            cpu_choice = random.choice(MOVES)
            st.session_state.player_choice = "scissors"
            st.session_state.cpu_choice = cpu_choice
            result = decide_winner("scissors", cpu_choice)
            st.session_state.pending_result = result
            st.session_state.result = None
            st.session_state.reveal_at = time.time() + 1.5
            st.session_state.status_message = "Animating... calculating outcome"
else:
    st.info("🏁 Match over. Start a new match to play again.")

# Reveal result after GIF animation delay
now = time.time()
if st.session_state.reveal_at and now >= st.session_state.reveal_at and st.session_state.pending_result:
    final_result = st.session_state.pending_result
    st.session_state.result = final_result
    st.session_state.pending_result = None
    st.session_state.reveal_at = None

    # Update scores now (after GIFs played)
    if final_result == "win":
        st.session_state.player_score += 1
    elif final_result == "lose":
        st.session_state.cpu_score += 1
    else:
        st.session_state.draws += 1

    # Proper quip using current choices
    st.session_state.status_message = get_robot_quip(
        final_result,
        st.session_state.player_choice,
        st.session_state.cpu_choice,
        st.session_state.player_name
    )

    # Append to history
    st.session_state.history.append({
        "round": len(st.session_state.history) + 1,
        "time": time.strftime("%H:%M:%S"),
        "player": st.session_state.player_name,
        "player_move": st.session_state.player_choice,
        "cpu_move": st.session_state.cpu_choice,
        "result": final_result,
    })

    # Increment rounds played and check for match end
    st.session_state.rounds_played += 1
    if st.session_state.rounds_played >= st.session_state.total_rounds:
        # Decide match winner by scores (player vs CPU). Draws counted but can cause tie.
        if st.session_state.player_score > st.session_state.cpu_score:
            st.session_state.match_winner = st.session_state.player_name
        elif st.session_state.cpu_score > st.session_state.player_score:
            st.session_state.match_winner = "CPU"
        else:
            st.session_state.match_winner = "DRAW"

        st.session_state.match_over = True
        # Build final announcement
        if st.session_state.match_winner == "DRAW":
            final_banner = f"MATCH OVER — DRAW ({st.session_state.player_score}-{st.session_state.cpu_score}, {st.session_state.draws} draws)"
        else:
            final_banner = f"MATCH OVER — {st.session_state.match_winner} WINS ({st.session_state.player_score}-{st.session_state.cpu_score}, {st.session_state.draws} draws)"
        # Show an eye-catching status
        st.session_state.status_message = final_banner

# Result display
if st.session_state.result:
    result_class = st.session_state.result
    result_text = {"win": "VICTORY", "lose": "DEFEAT", "draw": "DRAW"}[st.session_state.result]
    
    st.markdown(f"""
    <div class="result-banner {result_class}">
        {result_text}
    </div>
    """, unsafe_allow_html=True)

# Match over banner
if st.session_state.match_over:
    st.markdown(f"""
    <div class="result-banner win">
        {st.session_state.status_message}
    </div>
    """, unsafe_allow_html=True)

# Status message
st.markdown(f'<p class="status-message">{st.session_state.status_message}</p>', unsafe_allow_html=True)

# While waiting for reveal time, trigger a short auto-rerun to update UI when time elapses
if not st.session_state.match_over and st.session_state.reveal_at and time.time() < st.session_state.reveal_at:
    time.sleep(0.2)
    st.rerun()

# Reset / New Match controls
col_reset, col_new = st.columns(2)
with col_reset:
    if st.button("🔄 RESET SCORES", key="reset"):
        # Keep current mode; clear scores and rounds
        reset_match(keep_mode=True)
with col_new:
    if st.button("🏁 START NEW MATCH", key="new_match"):
        reset_match(keep_mode=True)

# Scoreboard

#st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #00ffff;'>SCOREBOARD</h4>", unsafe_allow_html=True)
st.markdown(f"""
<div class="score-container">
    <div>ROUND: {st.session_state.rounds_played} / {st.session_state.total_rounds}</div>
    <div>{st.session_state.player_name.upper()}: {st.session_state.player_score}</div>
    <div>DRAW: {st.session_state.draws}</div>
    <div>CPU: {st.session_state.cpu_score}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# History dropdown below the scoreboard
if st.session_state.history:
    labels = [
        f"Round {h['round']} — {h['player_move'].capitalize()} vs {h['cpu_move'].capitalize()} → {h['result'].upper()} ({h['time']})"
        for h in st.session_state.history
    ]
    _sel = st.selectbox("Move history", labels, index=len(labels)-1)
else:
    st.selectbox("Move history", ["No moves yet"], index=0, disabled=True)

# Testing hook in sidebar
with st.sidebar:
    st.header("🔧 DEVELOPER")
    if st.checkbox("Enable Testing Mode"):
        seed = st.number_input("Random Seed", value=42, step=1)
        if st.button("Set Seed"):
            random.seed(seed)
            st.success(f"Seed set to {seed}")
    
    st.markdown("---")
    st.markdown("### URL CONFIGURATION")
    st.markdown("Update GIF_URLS in the code with your actual GIF URLs")
    st.code("""
GIF_URLS = {
    "player_rock": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZmY4YzF2cjE4c2lld2EycXVoNWMwam9iNzhtdTZ2cnZybG1mZTFleSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/8YcJb8tW47SxYUZUQy/giphy.gif",
    "player_paper": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2k0eDIwMHA0YmVkOHIydTZxOTI3MTk1am43c21zY29udWg5NGkwYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9bJ2OJyi9quJAT81HC/giphy.gif", 
    "player_scissors": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZmY4YzF2cjE4c2lld2EycXVoNWMwam9iNzhtdTZ2cnZybG1mZTFleSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/RD3QScf0fgktocr353/giphy.gif",
    "cpu_rock": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGFvem91ejdzYXRtZnV1a3RsdjRkOTM0Y3Q0OHY4MGl1MmRuMzZwcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dAc4wOoFRNKNfgF9Zh/giphy.gif",
    "cpu_paper": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ajZwdmNyOXl2MHl3M211Z3UwNXNxdWplaGs4eWhhcG90dWFxa3Q1cSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/XeY4vs0zXUh99pJo1g/giphy.gif",
    "cpu_scissors": "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ajZwdmNyOXl2MHl3M211Z3UwNXNxdWplaGs4eWhhcG90dWFxa3Q1cSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/iFUrGtG2udD4yGAVyX/giphy.gif",
}
    """)

            # Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)