import streamlit as st
import random
from typing import Optional, List, Tuple

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
        <center> Day 12 - Tic-Tac-Toe </center>
    </h2>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [""] * 9
if 'turn' not in st.session_state:
    st.session_state.turn = "X"
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'winning_line' not in st.session_state:
    st.session_state.winning_line = None
if 'mode' not in st.session_state:
    st.session_state.mode = "PVP"
if 'scores' not in st.session_state:
    st.session_state.scores = {"X": 0, "O": 0}
if 'active_theme' not in st.session_state:
    st.session_state.active_theme = "quantum"
if 'player_names' not in st.session_state:
    st.session_state.player_names = {"X": "Player X", "O": "Player O"}
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'games_played': 0,
        'x_wins': 0,
        'o_wins': 0,
        'draws': 0,
        'current_streak': 0,
        'best_streak': 0,
        'last_winner': None
    }
if 'cpu_difficulty' not in st.session_state:
    st.session_state.cpu_difficulty = "Easy"

# Define themes with CSS + icon pairs for X and O
THEMES = {
    "quantum": {
        "name": "Quantum Grid",
        "icon": "⚛️",
        "x_icon": "⚛️",
        "o_icon": "🌀",
        "css": """
        :root {
            --neo-cyan: #00F0FF;
            --neo-mag: #FF00E6;
            --neo-purple: #8A2BE2;
            --glass: rgba(255,255,255,0.06);
            --text: #EAF6FF;
            --bg: #0B0F1A;
        }
        """
    },
    "redline": {
        "name": "Cyberpunk Redline",
        "icon": "🚨",
        "x_icon": "🚨",
        "o_icon": "🔥",
        "css": """
        :root {
            --neo-cyan: #FF3700;
            --neo-mag: #FFA500;
            --neo-purple: #FF4500;
            --glass: rgba(255,60,40,0.1);
            --text: #FFF0E0;
            --bg: #100000;
        }
        .tcell button:hover { box-shadow: 0 0 18px var(--neo-cyan); }
        .pulse-win { animation: pulseRed 1.2s infinite; }
        @keyframes pulseRed {
            0% { box-shadow: 0 0 0px var(--neo-mag); }
            50% { box-shadow: 0 0 32px var(--neo-mag); }
            100% { box-shadow: 0 0 0px var(--neo-mag); }
        }
        """
    },
    "matrix": {
        "name": "Glitch Matrix",
        "icon": "💾",
        "x_icon": "💾",
        "o_icon": "▓",
        "css": """
        :root {
            --neo-cyan: #00FF41;
            --neo-mag: #00C841;
            --neo-purple: #008F39;
            --glass: rgba(0, 255, 65, 0.05);
            --text: #CCFFDD;
            --bg: #000800;
        }
        .tcell button {
            font-family: 'Courier New', monospace;
            letter-spacing: 0.1em;
            font-size: 2rem;
        }
        @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }
        .pulse-win {
            animation: glitch 0.3s infinite, pulse 1.2s infinite;
            background: var(--neo-cyan) !important;
        }
        """
    },
    "cosmic": {
        "name": "Cosmic Void",
        "icon": "🌌",
        "x_icon": "🌠",
        "o_icon": "🌙",
        "css": """
        :root {
            --neo-cyan: #9D4EDD;
            --neo-mag: #5A189A;
            --neo-purple: #3C096C;
            --glass: rgba(128, 0, 255, 0.08);
            --text: #E0AAFF;
            --bg: #0D001A;
        }
        body, .stApp {
            background: radial-gradient(circle at center, var(--neo-cyan) 0%, var(--bg) 100%);
            background-attachment: fixed;
        }
        .tcell button:hover { box-shadow: 0 0 24px var(--neo-cyan); }
        .neo-glass {
            background: rgba(80, 20, 120, 0.1);
        }
        """
    },
    "classic": {
        "name": "Classic Mode",
        "icon": "♟️",
        "x_icon": "X",
        "o_icon": "O",
        "css": """
        :root {
            --neo-cyan: #555555;
            --neo-mag: #888888;
            --neo-purple: #333333;
            --glass: rgba(255,255,255,0.1);
            --text: #FFFFFF;
            --bg: #222222;
        }
        .tcell button {
            font-family: 'Georgia', serif;
            font-weight: bold;
            font-size: 2.8rem;
            letter-spacing: 0.05em;
        }
        .tcell button:hover {
            box-shadow: 0 0 12px rgba(255,255,255,0.5);
        }
        .pulse-win {
            background: rgba(255,255,255,0.2) !important;
            color: #FFD700 !important;
            box-shadow: 0 0 16px #FFD700;
        }
        body, .stApp {
            background: linear-gradient(135deg, #222, #333);
        }
        """
    }
}

# Inject dynamic CSS
dynamic_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=Poppins:wght@400;600&display=swap');

{THEMES[st.session_state.active_theme]['css']}

body, .stApp {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Poppins', system-ui, sans-serif;
    transition: background 0.5s ease;
}}

h1, h2, h3 {{
    font-family: 'Orbitron', sans-serif;
    letter-spacing: .03em;
}}

.neo-glass {{
    background: var(--glass);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 18px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.neo-glass:hover {{
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(0, 240, 255, 0.15);
}}

.price-chip {{
    color: var(--bg);
    background: linear-gradient(90deg, var(--neo-cyan), var(--neo-mag));
    padding: .2rem .6rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.9rem;
    display: inline-block;
    margin-top: 0.5rem;
}}

.tcell button {{
    width: 100%;
    aspect-ratio: 1/1;
    font-weight: 900;
    font-size: 2.4rem;
    border-radius: 20px !important;
    background: var(--glass);
    border: 2px solid rgba(255,255,255,0.1);
    color: var(--text);
    transition: all 0.2s ease;
    font-family: 'Orbitron', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.tcell button:hover {{
    box-shadow: 0 0 18px var(--neo-cyan);
    transform: scale(1.05);
}}

.tcell button:active {{
    box-shadow: 0 0 24px var(--neo-purple);
    transform: scale(0.98);
}}

.pulse-win {{
    animation: pulse 1.2s infinite;
    background: var(--neo-mag) !important;
    color: var(--bg) !important;
    box-shadow: 0 0 24px var(--neo-mag);
}}

@keyframes pulse {{
    0% {{ box-shadow: 0 0 0px var(--neo-mag); }}
    50% {{ box-shadow: 0 0 24px var(--neo-mag); }}
    100% {{ box-shadow: 0 0 0px var(--neo-mag); }}
}}

.stButton>button {{
    border-radius: 12px !important;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 0.05em;
    border: none;
    background: linear-gradient(90deg, var(--neo-cyan), var(--neo-purple));
    color: var(--bg);
}}

.stButton>button:hover {{
    box-shadow: 0 0 16px var(--neo-cyan);
}}

.badge {{
    padding: 0.5rem 1rem;
    border-radius: 12px;
    font-weight: 700;
    display: inline-block;
    margin: 1rem 0;
    font-family: 'Orbitron', sans-serif;
    background: linear-gradient(90deg, var(--neo-cyan), var(--neo-mag));
    color: var(--bg);
    animation: fadeIn 0.5s ease;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: scale(0.9); }}
    to {{ opacity: 1; transform: scale(1); }}
}}

.grid-container {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    max-width: 400px;
    margin: 0 auto;
}}

.menu-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem auto;
    max-width: 1200px;
    padding: 0 1rem;
}}

.selected-theme {{
    animation: bounce 0.5s;
    border: 2px solid var(--neo-cyan);
}}
@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{transform: translateY(0);}}
    40% {{transform: translateY(-8px);}}
    60% {{transform: translateY(-4px);}}
}}

.stat-card {{
    background: rgba(255,255,255,0.05);
    padding: 1rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    border-left: 4px solid var(--neo-cyan);
}}

.streak-glow {{
    color: gold;
    text-shadow: 0 0 8px gold;
}}
</style>
"""

st.markdown(dynamic_css, unsafe_allow_html=True)

# Winning combinations
WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

def check_winner(board: List[str]) -> Tuple[Optional[str], Optional[Tuple[int, int, int]]]:
    for combo in WINNING_COMBINATIONS:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], combo
    return None, None

def is_board_full(board: List[str]) -> bool:
    return all(cell != "" for cell in board)

def find_winning_move(board: List[str], player: str) -> Optional[int]:
    """Returns index of winning move for player, or None."""
    for i in range(9):
        if board[i] == "":
            board[i] = player
            if check_winner(board)[0] == player:
                board[i] = ""
                return i
            board[i] = ""
    return None

def find_blocking_move(board: List[str], opponent: str) -> Optional[int]:
    """Returns index to block opponent's winning move."""
    return find_winning_move(board, opponent)

def cpu_move() -> Optional[int]:
    """CPU move based on difficulty level."""
    empty_cells = [i for i, cell in enumerate(st.session_state.board) if cell == ""]
    if not empty_cells:
        return None

    difficulty = st.session_state.cpu_difficulty
    board = st.session_state.board

    if difficulty == "Hard":
        # 1. Win if possible
        move = find_winning_move(board, "O")
        if move is not None:
            return move
        # 2. Block opponent
        move = find_blocking_move(board, "X")
        if move is not None:
            return move
        # 3. Take center
        if 4 in empty_cells:
            return 4
        # 4. Take corners
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if i in empty_cells]
        if available_corners:
            return random.choice(available_corners)
        # 5. Take any
        return random.choice(empty_cells)

    elif difficulty == "Medium":
        # 1. Block opponent
        move = find_blocking_move(board, "X")
        if move is not None:
            return move
        # 2. Take center
        if 4 in empty_cells:
            return 4
        # 3. Random
        return random.choice(empty_cells)

    else:  # Easy
        return random.choice(empty_cells)

def make_move(index: int):
    if st.session_state.winner or st.session_state.board[index] != "":
        return
    st.session_state.board[index] = st.session_state.turn
    winner, winning_line = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.winning_line = winning_line
        st.session_state.scores[winner] += 1
        
        # Update stats
        st.session_state.stats['games_played'] += 1
        if winner == "X":
            st.session_state.stats['x_wins'] += 1
        else:
            st.session_state.stats['o_wins'] += 1
            
        # Update streak
        if st.session_state.stats['last_winner'] == winner:
            st.session_state.stats['current_streak'] += 1
        else:
            st.session_state.stats['current_streak'] = 1
        st.session_state.stats['last_winner'] = winner
        if st.session_state.stats['current_streak'] > st.session_state.stats['best_streak']:
            st.session_state.stats['best_streak'] = st.session_state.stats['current_streak']
            
    elif is_board_full(st.session_state.board):
        st.session_state.winner = "DRAW"
        st.session_state.stats['games_played'] += 1
        st.session_state.stats['draws'] += 1
        st.session_state.stats['current_streak'] = 0
        st.session_state.stats['last_winner'] = None
    else:
        st.session_state.turn = "O" if st.session_state.turn == "X" else "X"
        if st.session_state.mode == "CPU" and st.session_state.turn == "O":
            cpu_index = cpu_move()
            if cpu_index is not None:
                st.session_state.board[cpu_index] = "O"
                winner, winning_line = check_winner(st.session_state.board)
                if winner:
                    st.session_state.winner = winner
                    st.session_state.winning_line = winning_line
                    st.session_state.scores[winner] += 1
                    
                    st.session_state.stats['games_played'] += 1
                    st.session_state.stats['o_wins'] += 1
                    
                    if st.session_state.stats['last_winner'] == winner:
                        st.session_state.stats['current_streak'] += 1
                    else:
                        st.session_state.stats['current_streak'] = 1
                    st.session_state.stats['last_winner'] = winner
                    if st.session_state.stats['current_streak'] > st.session_state.stats['best_streak']:
                        st.session_state.stats['best_streak'] = st.session_state.stats['current_streak']
                        
                elif is_board_full(st.session_state.board):
                    st.session_state.winner = "DRAW"
                    st.session_state.stats['games_played'] += 1
                    st.session_state.stats['draws'] += 1
                    st.session_state.stats['current_streak'] = 0
                    st.session_state.stats['last_winner'] = None
                else:
                    st.session_state.turn = "X"

def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.turn = "X"
    st.session_state.winner = None
    st.session_state.winning_line = None

def render_menu():
    # st.title("⚡ NEON ARCADE ⚡")
    # st.markdown("### CHOOSE YOUR POWER-UP THEME")

    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 3rem; letter-spacing: 0.05em; animation: fadeIn 0.8s ease;">⚡ NEON ARCADE ⚡</h1>
        <h3 style="opacity: 0.9; font-weight: 500;">CHOOSE YOUR POWER-UP THEME</h3>
    </div>
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

    menu_items = [
        {"id": "quantum", "price": "19.99", "desc": "Sci-fi particles and quantum glow"},
        {"id": "redline", "price": "14.99", "desc": "Crimson sirens and fire trails"},
        {"id": "matrix", "price": "2.99", "desc": "Glitchy terminals and hacker vibes"},
        {"id": "cosmic", "price": "7.99", "desc": "Stardust trails and lunar halos"},
        {"id": "classic", "price": "FREE", "desc": "Pure nostalgia — original X and O"}
    ]

    st.markdown('<div class="menu-grid">', unsafe_allow_html=True)
    for item in menu_items:
        theme = THEMES[item["id"]]
        is_active = st.session_state.active_theme == item["id"]
        border_class = " selected-theme" if is_active else ""
        
        st.markdown(f"""
        <div class="neo-glass{border_class}">
            <h3>{theme['icon']} {theme['name']}</h3>
            <p>{item['desc']}</p>
            <p><strong>X</strong> = {theme['x_icon']} &nbsp; <strong>O</strong> = {theme['o_icon']}</p>
            <div class="price-chip">{item['price']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"✨ ACTIVATE {theme['name'].upper()}", key=f"btn_{item['id']}", use_container_width=True):
            st.session_state.active_theme = item["id"]
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### Ready to play?")
    if st.button("🎮 LAUNCH GAME", key="launch", use_container_width=True):
        st.session_state.view = "play"
        st.rerun()

def render_stats():
    st.title("📊 PLAYER STATS")
    
    s = st.session_state.stats
    total = s['games_played']
    x_pct = (s['x_wins'] / total * 100) if total > 0 else 0
    o_pct = (s['o_wins'] / total * 100) if total > 0 else 0
    
    st.markdown(f"""
    <div class="stat-card">
        <h3>🎮 Total Games: {total}</h3>
        <p>❌ {st.session_state.player_names['X']}: {s['x_wins']} ({x_pct:.1f}%)</p>
        <p>⭕ {st.session_state.player_names['O']}: {s['o_wins']} ({o_pct:.1f}%)</p>
        <p>🤝 Draws: {s['draws']}</p>
    </div>
    <div class="stat-card">
        <h3>🔥 Streaks</h3>
        <p>Current: <span class="{'streak-glow' if s['current_streak'] >= 3 else ''}">{s['current_streak']}</span></p>
        <p>Best: <span class="streak-glow">{s['best_streak']}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ BACK TO GAME", use_container_width=True):
        st.session_state.view = "play"
        st.rerun()

def render_board():
    st.title("⚡ TIC-TAC-TOE ⚡")
    
    # Player name inputs
    with st.expander("👤 Player Names", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_x_name = st.text_input("Player X", value=st.session_state.player_names["X"], key="x_name")
        with col2:
            new_o_name = st.text_input("Player O", value=st.session_state.player_names["O"], key="o_name")
        if st.button("💾 Save Names"):
            st.session_state.player_names["X"] = new_x_name or "Player X"
            st.session_state.player_names["O"] = new_o_name or "Player O"
            st.rerun()
    
    # Game mode and difficulty
    col1, col2, col3 = st.columns(3)
    with col1:
        new_mode = st.radio("Mode", ["Two Players", "vs Computer"], 
                           index=0 if st.session_state.mode == "PVP" else 1,
                           horizontal=False)
        st.session_state.mode = "PVP" if new_mode == "Two Players" else "CPU"
    
    with col2:
        if st.session_state.mode == "CPU":
            st.session_state.cpu_difficulty = st.selectbox(
                "Difficulty",
                ["Easy", "Medium", "Hard"],
                index=["Easy", "Medium", "Hard"].index(st.session_state.cpu_difficulty)
            )
    
    with col3:
        if st.button("📊 Stats", use_container_width=True):
            st.session_state.view = "stats"
            st.rerun()
    
    # Scoreboard with player names
    theme = THEMES[st.session_state.active_theme]
    st.markdown(f"**SCORE**  {theme['x_icon']} {st.session_state.player_names['X']}: {st.session_state.scores['X']} | {theme['o_icon']} {st.session_state.player_names['O']}: {st.session_state.scores['O']}")

    # Current turn with player name
    if not st.session_state.winner:
        current_player = st.session_state.player_names[st.session_state.turn]
        current_icon = theme['x_icon'] if st.session_state.turn == "X" else theme['o_icon']
        st.markdown(f"### Current Turn: **{current_icon} {current_player}**")

    # Winner badge
    if st.session_state.winner:
        if st.session_state.winner == "DRAW":
            st.markdown('<div class="badge">⚡ IT\'S A DRAW! ⚡</div>', unsafe_allow_html=True)
        else:
            winner_icon = theme['x_icon'] if st.session_state.winner == "X" else theme['o_icon']
            winner_name = st.session_state.player_names[st.session_state.winner]
            st.markdown(f'<div class="badge">🎉 {winner_icon} {winner_name} WINS! 🎉</div>', unsafe_allow_html=True)

    # Game grid
    grid = st.container()
    with grid:
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                index = i * 3 + j
                cell_value = st.session_state.board[index]
                
                # Map internal "X"/"O" to theme icons for display
                display_icon = ""
                if cell_value == "X":
                    display_icon = theme['x_icon']
                elif cell_value == "O":
                    display_icon = theme['o_icon']
                
                row, col = i + 1, j + 1
                is_winning_cell = st.session_state.winning_line and index in st.session_state.winning_line
                button_class = "tcell"
                if is_winning_cell:
                    button_class += " pulse-win"
                
                tooltip = f"Occupied by {cell_value}" if cell_value else f"Place {st.session_state.turn} at row {row}, col {col}"

                with cols[j]:
                    if st.button(
                        display_icon or " ",
                        key=f"cell_{index}",
                        help=tooltip,
                        use_container_width=True
                    ):
                        if not st.session_state.winner:
                            make_move(index)
                            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.button("🔄 RESET GAME", on_click=reset_game, use_container_width=True)
    if st.button("⬅️ BACK TO MENU", use_container_width=True):
        st.session_state.view = "menu"
        st.rerun()

def _simulate_game(moves: List[int]) -> str:
    board = [""] * 9
    turn = "X"
    for move in moves:
        if board[move] != "":
            continue
        board[move] = turn
        w, _ = check_winner(board)
        if w:
            return w
        if all(cell != "" for cell in board):
            return "DRAW"
        turn = "O" if turn == "X" else "X"
    return "IN_PROGRESS"

def main():
    if 'view' not in st.session_state:
        st.session_state.view = "menu"
    
    if st.session_state.view == "menu":
        render_menu()
    elif st.session_state.view == "stats":
        render_stats()
    else:
        render_board()

if __name__ == "__main__":
    main()

            # Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)