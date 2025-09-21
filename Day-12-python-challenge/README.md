# 🦅 Social Eagle – Python Challenge Day 11

Day 12 Task : 
 
Tic-Tac-Toe ❌⭕

> 3x3 grid using buttons.

> Two-player mode (or vs computer with random moves).

> Highlight winning line.

> Option to reset the board.

# 🎮 Ultra-Realistic Futuristic Tic-Tac-Toe Arcade

> A cinematic, neon-drenched, hyper-stylized Streamlit app with themes, AI difficulty, player stats, and arcade flair — all in one file.
> Built by **Shaid** for the Social Eagle Python Challenge (Day 12).
<br>

## 🌟 Features

✅ **Futuristic Neon UI** — Glassmorphism, glowing buttons, pulse animations  
✅ **5 Themed Power-Ups** — Each transforms the board, colors, and X/O icons:
- **Quantum Grid** ⚛️🌀 — Sci-fi particles
- **Cyberpunk Redline** 🚨🔥 — Crimson sirens
- **Glitch Matrix** 💾▓ — Hacker terminal
- **Cosmic Void** 🌠🌙 — Starfield cosmos
- **Classic Mode** ❌⭕ — Pure nostalgia

✅ **Player Personalization** — Name your X and O players  
✅ **CPU Opponent with 3 Difficulty Levels**:
- **Easy**: Random moves
- **Medium**: Blocks your wins
- **Hard**: Tries to win → blocks you → center/corner strategy

✅ **Stats Tracker** — Tracks:
- Total games played
- Wins per player
- Draw count
- Current & best win streaks (with gold glow!)

✅ **Win Detection & Animation** — Glowing pulse effect on winning line  
✅ **Responsive Design** — Works on mobile & desktop  
✅ **Single File, Zero External Assets** — Only dependency: `streamlit`

---
## Demo Video



https://github.com/user-attachments/assets/90959c16-28c9-41be-8d4b-92fbea3850de


---
## 🚀 How to Run

### 1. Clone or Create

Save the code as `app.py`.

### 2. Install Streamlit

```bash
pip install streamlit
```

### 3. Launch the App

```bash
streamlit run app.py
```

Open the URL shown in your terminal (usually `http://localhost:8501`).

---

## 🕹️ How to Play

1. **Start on Menu** — Pick a theme, activate it.
2. **Launch Game** — Set player names (optional).
3. **Choose Mode**:
   - **Two Players**: Local hotseat
   - **vs Computer**: Pick Easy/Medium/Hard
4. **Play** — Click cells to place your mark.
5. **Win** — Watch the winning line glow!
6. **Reset** — Start fresh anytime.
7. **View Stats** — Track your mastery.
8. **Back to Menu** — Switch themes or take a break.

---

## 🧩 Code Structure

All features are contained in one file: `app.py`

- **Session State** — Manages board, scores, themes, stats, player names
- **CSS Injection** — Dynamic styling based on active theme
- **Game Logic** — Win detection, CPU AI, move validation
- **UI Components** — Menu, board, stats panel, settings

---

## 🛠️ Customization & Extensibility

You can easily:

- Add new themes (copy/paste + tweak CSS & icons)
- Add sound effects (inject `<audio>` tags)
- Add achievements or easter eggs
- Export stats to file or share via URL

---

## 📸 Screenshots (Conceptual)

> *Add your own screenshots here after deployment!*

- **Menu Screen**: Glowing theme cards with prices
- **Game Screen**: Neon grid with animated win effects
- **Stats Panel**: Clean cards showing win rates and streaks

---

## 🧪 Testing

Includes internal `_simulate_game()` function for validation:

```python
# Example: Simulate X winning top row
outcome = _simulate_game([0, 3, 1, 4, 2])  # returns "X"
```

---

## 📦 Dependencies

Only one:

```txt
streamlit>=1.27.0
```

> Works on older Streamlit too — logic patched for backward compatibility.

---

## 🌈 Theme Showcase

| Theme         | X     | O     | Vibe                  |
|---------------|-------|-------|------------------------|
| Quantum       | ⚛️    | 🌀    | Sci-fi particles       |
| Redline       | 🚨    | 🔥    | Cyberpunk danger       |
| Matrix        | 💾    | ▓     | Hacker terminal        |
| Cosmic        | 🌠    | 🌙    | Deep space mystery     |
| Classic       | X     | O     | Timeless simplicity    |

---

## 📜 License

MIT — Use, modify, and deploy freely. Perfect for portfolios, demos, or fun!

---

## 💡 Pro Tips

- Try **Hard mode** — the AI will surprise you!
- Activate **Matrix theme** for full hacker immersion.
- Chase the **gold streak glow** — can you hit 5 wins in a row?

---

## 🚨 Troubleshooting

**Issue**: Buttons break after win on old Streamlit  
**Fix**: Upgrade Streamlit → `pip install --upgrade streamlit`  
**Fallback**: Code already patched to work on older versions!

---

## 🙌 Credits

Built with ❤️ using Streamlit.  
Designed for arcade lovers, theme chasers, and tic-tac-toe masters.

---



Let the neon games begin! 🎮🔮
