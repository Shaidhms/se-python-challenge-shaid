import streamlit as st
import time
import random
from PIL import Image, ImageDraw

import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval


import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("se.png")

# CSS style block
st.markdown("""
<style>
.main-header {
    text-align: center;
    background: linear-gradient(90deg, #00f0ff, #00ff9d, #7c00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.2rem;   /* adjust if you want bigger/smaller */
    letter-spacing: 2px;
    text-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
    margin-bottom: 15px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# Apply your header content inside that class
st.markdown(
    f"""
    <div class="main-header">
        <img src="data:image/png;base64,{logo_base64}" width="40" 
             style="vertical-align: middle; margin-right:8px;">
        Social Eagle Python Challenge<br>
        Day 15 - Snake Game
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Configuration
# ----------------------------
st.set_page_config(page_title="Neon Snake v2.0", layout="wide")

GRID_SIZE = 20
CELL_SIZE = 25
BOARD_SIZE = GRID_SIZE * CELL_SIZE

# Colors
BG_COLOR = (10, 10, 35)        # Dark blue background
GRID_COLOR = (50, 50, 100)     # Grid lines
SNAKE_HEAD = (100, 255, 100)   # Bright green head
SNAKE_BODY = (50, 200, 50)     # Green body
FOOD_COLOR = (255, 50, 50)     # Red food
DIAMOND_COLOR = (200, 100, 255)  # Purple diamond
DIAMOND_GLOW = (230, 180, 255)

# ----------------------------
# Futuristic UI Styling
# ----------------------------
st.markdown("""
<style>
/* Futuristic Title */
h1 {
    text-align: center;
    background: linear-gradient(90deg, #00f0ff, #00ff9d, #7c00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.8rem;
    letter-spacing: 2px;
    text-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
    margin-bottom: 10px;
}

/* Score HUD */
.score-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 15px 0 25px 0;
    flex-wrap: wrap;
}

.score-chip {
    background: linear-gradient(145deg, #0f1b3a, #0a1228);
    border: 2px solid #00f0ff;
    border-radius: 16px;
    padding: 16px 24px;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
    text-align: center;
    min-width: 160px;
    animation: pulse-border 3s infinite;
}

@keyframes pulse-border {
    0% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.3); }
    50% { box-shadow: 0 0 25px rgba(0, 240, 255, 0.6); }
    100% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.3); }
}

.score-label {
    font-size: 0.9rem;
    color: #a0f0ff;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    font-weight: 600;
}

.score-value {
    font-size: 2.2rem;
    font-family: 'Courier New', monospace;
    color: #00ff9d;
    text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
    font-weight: bold;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1a 0%, #050810 100%);
    border-right: 1px solid #00f0ff;
    box-shadow: 5px 0 25px rgba(0, 240, 255, 0.15);
}

.sidebar-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #00f0ff;
    text-align: center;
    margin: 10px 0 20px 0;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.7);
    letter-spacing: 1px;
}

/* Sidebar Buttons */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(145deg, #0c162a, #070e1a);
    color: #a0f0ff;
    border: 1px solid #00b0cc;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #00f0ff;
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
    transform: translateY(-1px);
}

/* Slider */
[data-testid="stSidebar"] .stSlider > div > div > div {
    background: #00f0ff !important;
}

/* Diamond Timer */
.diamond-timer {
    background: linear-gradient(145deg, #1a0a2a, #0f071a);
    border: 1px solid #d900ff;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    margin: 15px 0;
    color: #f0a0ff;
    box-shadow: 0 0 15px rgba(217, 0, 255, 0.3);
}

/* History Panel */
.history-panel {
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid #00f0ff;
}

.history-title {
    color: #00f0ff;
    font-size: 1.1rem;
    margin-bottom: 10px;
    text-align: center;
}

.history-item {
    color: #a0f0ff;
    font-family: 'Courier New', monospace;
    font-size: 1.0rem;
    padding: 4px 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Initialize Session State
# ----------------------------
if 'snake' not in st.session_state:
    st.session_state.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
if 'direction' not in st.session_state:
    st.session_state.direction = "RIGHT"
if 'food' not in st.session_state:
    st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'running' not in st.session_state:
    st.session_state.running = False
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'speed' not in st.session_state:
    st.session_state.speed = 8
if 'last_key' not in st.session_state:
    st.session_state.last_key = None
# Ensure game-over history is recorded only once
if 'history_recorded' not in st.session_state:
    st.session_state.history_recorded = False

# Grid visibility toggle state
if 'show_grid' not in st.session_state:
    st.session_state.show_grid = True

# Diamond-specific state
if 'diamond' not in st.session_state:
    st.session_state.diamond = None
if 'diamond_timer' not in st.session_state:
    st.session_state.diamond_timer = 0
if 'diamond_active' not in st.session_state:
    st.session_state.diamond_active = False

# ----------------------------
# Helper Functions
# ----------------------------

def reset_game():
    # Start a fresh game without re-recording history here
    st.session_state.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    st.session_state.score = 0
    st.session_state.running = False
    st.session_state.game_over = False
    st.session_state.last_update = time.time()
    st.session_state.diamond = None
    st.session_state.diamond_timer = 0
    st.session_state.diamond_active = False
    st.session_state.last_key = None
    st.session_state.history_recorded = False

def change_direction(new_dir):
    opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    if new_dir != opposites.get(st.session_state.direction):
        st.session_state.direction = new_dir
        if not st.session_state.running:
            st.session_state.running = True

def move_snake():
    head_x, head_y = st.session_state.snake[0]
    dx, dy = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}[st.session_state.direction]
    new_head = (head_x + dx, head_y + dy)

    if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
        st.session_state.running = False
        st.session_state.game_over = True
        return

    if st.session_state.diamond_active and new_head == st.session_state.diamond:
        st.session_state.score += 5
        tail = st.session_state.snake[-1]
        for _ in range(5):
            st.session_state.snake.append(tail)
        st.session_state.diamond = None
        st.session_state.diamond_active = False
        st.session_state.snake.insert(0, new_head)
        return

    if new_head in st.session_state.snake:
        st.session_state.running = False
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head)

    if new_head == st.session_state.food:
        st.session_state.score += 1
        while True:
            new_food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if new_food not in st.session_state.snake:
                st.session_state.food = new_food
                break

        if random.random() < 0.10:
            for _ in range(50):
                diamond_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
                if (diamond_pos not in st.session_state.snake and 
                    diamond_pos != st.session_state.food and
                    diamond_pos != st.session_state.diamond):
                    st.session_state.diamond = diamond_pos
                    st.session_state.diamond_timer = time.time() + 8
                    st.session_state.diamond_active = True
                    break
    else:
        st.session_state.snake.pop()

def draw_board():
    img = Image.new("RGB", (BOARD_SIZE, BOARD_SIZE), BG_COLOR)
    draw = ImageDraw.Draw(img)

    if st.session_state.get('show_grid', True):
        for i in range(GRID_SIZE + 1):
            x = i * CELL_SIZE
            y = i * CELL_SIZE
            draw.line([(x, 0), (x, BOARD_SIZE)], fill=GRID_COLOR, width=1)
            draw.line([(0, y), (BOARD_SIZE, y)], fill=GRID_COLOR, width=1)

    fx, fy = st.session_state.food
    padding = CELL_SIZE // 6
    draw.ellipse([
        fx * CELL_SIZE + padding,
        fy * CELL_SIZE + padding,
        (fx + 1) * CELL_SIZE - padding,
        (fy + 1) * CELL_SIZE - padding
    ], fill=FOOD_COLOR)

    pulse = (time.time() * 2) % 1
    glow_intensity = int(100 + 155 * (0.5 + 0.5 * (pulse - 0.5) * 2))
    for offset in [3, 2, 1]:
        current_glow = int(glow_intensity * (4 - offset) * 0.3)
        if current_glow > 0:
            draw.ellipse([
                fx * CELL_SIZE + padding - offset * 2,
                fy * CELL_SIZE + padding - offset * 2,
                (fx + 1) * CELL_SIZE - padding + offset * 2,
                (fy + 1) * CELL_SIZE - padding + offset * 2
            ], outline=(current_glow, max(0, current_glow // 5), max(0, current_glow // 5)), width=1)

    if st.session_state.diamond_active and st.session_state.diamond:
        dx, dy = st.session_state.diamond
        cx = dx * CELL_SIZE + CELL_SIZE // 2
        cy = dy * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 3
        diamond_points = [
            (cx, cy - radius),
            (cx + radius, cy),
            (cx, cy + radius),
            (cx - radius, cy)
        ]
        draw.polygon(diamond_points, fill=DIAMOND_COLOR)
        for offset in [1, 2]:
            draw.polygon([
                (cx, cy - radius - offset),
                (cx + radius + offset, cy),
                (cx, cy + radius + offset),
                (cx - radius - offset, cy)
            ], outline=DIAMOND_GLOW, width=1)

    for i, (x, y) in enumerate(st.session_state.snake):
        if i == 0:
            head_x1 = x * CELL_SIZE
            head_y1 = y * CELL_SIZE
            head_x2 = (x + 1) * CELL_SIZE
            head_y2 = (y + 1) * CELL_SIZE

            glow_color = (200, 255, 200)
            for offset in [2, 1]:
                draw.rectangle([
                    head_x1 - offset, head_y1 - offset,
                    head_x2 + offset, head_y2 + offset
                ], outline=glow_color, width=1)

            draw.rectangle([head_x1, head_y1, head_x2, head_y2], fill=SNAKE_HEAD)

            eye_size = max(2, CELL_SIZE // 8)
            if st.session_state.direction == "RIGHT":
                left_eye = (x * CELL_SIZE + CELL_SIZE - eye_size - 2, y * CELL_SIZE + eye_size + 2)
                right_eye = (x * CELL_SIZE + CELL_SIZE - eye_size - 2, y * CELL_SIZE + CELL_SIZE - 2 * eye_size - 2)
            elif st.session_state.direction == "LEFT":
                left_eye = (x * CELL_SIZE + 2, y * CELL_SIZE + eye_size + 2)
                right_eye = (x * CELL_SIZE + 2, y * CELL_SIZE + CELL_SIZE - 2 * eye_size - 2)
            elif st.session_state.direction == "UP":
                left_eye = (x * CELL_SIZE + eye_size + 2, y * CELL_SIZE + 2)
                right_eye = (x * CELL_SIZE + CELL_SIZE - 2 * eye_size - 2, y * CELL_SIZE + 2)
            elif st.session_state.direction == "DOWN":
                left_eye = (x * CELL_SIZE + eye_size + 2, y * CELL_SIZE + CELL_SIZE - eye_size - 2)
                right_eye = (x * CELL_SIZE + CELL_SIZE - 2 * eye_size - 2, y * CELL_SIZE + CELL_SIZE - eye_size - 2)

            draw.ellipse([left_eye[0], left_eye[1], left_eye[0] + eye_size, left_eye[1] + eye_size], fill=(0, 0, 0))
            draw.ellipse([right_eye[0], right_eye[1], right_eye[0] + eye_size, right_eye[1] + eye_size], fill=(0, 0, 0))

            frame = int(time.time() * 4) % 8
            mouth_open = frame < 4
            if mouth_open:
                mouth_color = (255, 100, 100)
                if st.session_state.direction == "RIGHT":
                    mouth_rect = [head_x2 - 2, head_y1 + CELL_SIZE//3, head_x2, head_y2 - CELL_SIZE//3]
                elif st.session_state.direction == "LEFT":
                    mouth_rect = [head_x1, head_y1 + CELL_SIZE//3, head_x1 + 2, head_y2 - CELL_SIZE//3]
                elif st.session_state.direction == "UP":
                    mouth_rect = [head_x1 + CELL_SIZE//3, head_y1, head_x2 - CELL_SIZE//3, head_y1 + 2]
                elif st.session_state.direction == "DOWN":
                    mouth_rect = [head_x1 + CELL_SIZE//3, head_y2 - 2, head_x2 - CELL_SIZE//3, head_y2]
                draw.rectangle(mouth_rect, fill=mouth_color)

        else:
            draw.rectangle([
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE
            ], fill=SNAKE_BODY)

    return img

# ----------------------------
# SIDEBAR: Futuristic Controls
# ----------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">VENOM PANEL</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬆️ UP", key="up"):
            change_direction("UP")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ LEFT", key="left"):
            change_direction("LEFT")
    with col2:
        if st.button("➡️ RIGHT", key="right"):
            change_direction("RIGHT")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬇️ DOWN", key="down"):
            change_direction("DOWN")
    
    st.markdown("---")
    if st.button("▶️ START", use_container_width=True):
        st.session_state.running = True
        st.session_state.game_over = False
    if st.button("⏸️ PAUSE", use_container_width=True):
        st.session_state.running = False
    if st.button("🔄 RESTART", use_container_width=True):
        reset_game()
    
    st.slider("SPEED", 1, 15, value=st.session_state.speed, key="speed")
    st.toggle("Show grid", value=st.session_state.show_grid, key="show_grid")

# ----------------------------
# MAIN AREA — Futuristic UI
# ----------------------------

st.title("🐍 Pixel Python")

# Score & High Score HUD
st.markdown(f"""
<div class="score-container">
    <div class="score-chip">
        <div class="score-label">Current Score</div>
        <div class="score-value">{st.session_state.score:03d}</div>
    </div>
    <div class="score-chip">
        <div class="score-label">High Score</div>
        <div class="score-value">{st.session_state.high_score:03d}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Diamond timer (if active)
if st.session_state.diamond_active:
    remaining = max(0, int(st.session_state.diamond_timer - time.time()))
    st.markdown(f'<div class="diamond-timer">💎 DIAMOND ACTIVE! Expires in: <strong>{remaining}s</strong></div>', unsafe_allow_html=True)

# Ensure main iframe has focus and grab keys even after sidebar clicks
components.html(
    """
<div id=\"keyfocus\" tabindex=\"0\" style=\"outline:none;width:0;height:0;opacity:0;position:fixed;left:-9999px;top:-9999px;\"></div>
<script>
(function(){
  // Focus an invisible element so the main iframe regains focus after sidebar interactions
  const el = document.getElementById('keyfocus');
  if (el) {
    try { el.focus({preventScroll:true}); } catch (e) {}
    setTimeout(function(){ try { el.focus({preventScroll:true}); } catch (e) {} }, 0);
  }
  function handle(e){
    const k = e.key;
    const allow = ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d','W','A','S','D',' '];
    if (allow.includes(k)) {
      window._snakeLastKey = (k.length === 1 ? k.toLowerCase() : k);
      try { e.preventDefault(); } catch(_) {}
      try { e.stopPropagation(); } catch(_) {}
      try { e.stopImmediatePropagation(); } catch(_) {}
    }
  }
  if (!window._snakeKeyListenerAdded2) {
    window._snakeKeyListenerAdded2 = true;
    // Listen on both window and document in capture phase
    window.addEventListener('keydown', handle, {capture:true, passive:false});
    document.addEventListener('keydown', handle, {capture:true, passive:false});
  }
})();
</script>
""",
    height=0,
)

# ----------------------------------------------------
# Keyboard Input via streamlit_js_eval (robust, one-shot capture)
#  - Adds a single document-level listener (capture phase, passive:false)
#  - Stores last key in window._snakeLastKey and returns + clears it each run
#  - Prevents page scroll on arrows/space (Mac friendly)
# ----------------------------------------------------
key_press = streamlit_js_eval(
    js_expressions="""
    (function() {
        // Install only once
        if (!window._snakeKeyListenerAdded) {
            window._snakeKeyListenerAdded = true;
            document.addEventListener(
                'keydown',
                function(e) {
                    const k = e.key;
                    const allow = ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d','W','A','S','D',' '];
                    if (allow.includes(k)) {
                        // Normalize to lowercase for WASD and keep Arrow* as-is
                        window._snakeLastKey = (k.length === 1 ? k.toLowerCase() : k);
                        try { e.preventDefault(); } catch (_) {}
                    }
                },
                { capture: true, passive: false }
            );
        }
        // Read and clear the buffered key so Python sees it once per rerun
        const v = window._snakeLastKey || null;
        window._snakeLastKey = null;
        return v;
    })()
    """,
    key="snake_keys_v2",
    want_value=True,
)

if key_press:
    if key_press == 'ArrowUp' or key_press == 'w':
        change_direction('UP')
    elif key_press == 'ArrowDown' or key_press == 's':
        change_direction('DOWN')
    elif key_press == 'ArrowLeft' or key_press == 'a':
        change_direction('LEFT')
    elif key_press == 'ArrowRight' or key_press == 'd':
        change_direction('RIGHT')
    elif key_press == ' ':  # Space toggles pause
        st.session_state.running = not st.session_state.running

# Game board
board = draw_board()
st.image(board, width='stretch')

# Game over
if st.session_state.game_over:
    # Record history only once per game over
    if not st.session_state.get('history_recorded', False):
        if st.session_state.score > 0:
            st.session_state.game_history.insert(0, st.session_state.score)
            st.session_state.game_history = st.session_state.game_history[:5]
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
        st.session_state.history_recorded = True
    st.error(f"💀 GAME OVER! Final Score: {st.session_state.score}")
    # Do not auto-reset here; user can press RESTART

# Game history panel
if st.session_state.game_history:
    history_html = "".join([f"<div class='history-item'>Game {i+1}: {score}</div>" for i, score in enumerate(st.session_state.game_history[:5])])
    st.markdown(f"""
    <div class="history-panel">
        <div class="history-title">🏆 RECENT GAMES</div>
        {history_html}
    </div>
    """, unsafe_allow_html=True)

# Game loop
if st.session_state.running and not st.session_state.game_over:
    now = time.time()
    time_to_move = 1.0 / st.session_state.speed
    if now - st.session_state.last_update >= time_to_move:
        move_snake()
        st.session_state.last_update = now
        st.rerun()
    else:
        time_to_sleep = time_to_move - (now - st.session_state.last_update)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
            st.rerun()
        else:
            st.rerun()

            # Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)            