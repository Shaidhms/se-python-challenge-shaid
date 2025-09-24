# 🦅 Social Eagle – Python Challenge Day 15

Day 15 Task : 
 
> Problem Statement: Snake Game in Streamlit

> Build a classic Snake Game where the player controls a snake to eat food and grow in size, while avoiding collisions with the walls or itself.
> Requirements:
> - Create a grid-based game board.
> - The snake moves automatically in the chosen direction (Up/Down/Left/Right).
> - Player can change direction using buttons or keyboard input.
> - Food appears randomly on the grid.
> - Each time the snake eats food, its length increases and the score updates.
> - The game ends if the snake collides with the wall or itself.
> - Display the current score and a "Restart" option.

> Goal:
> Practice real-time updates, session state management, and dynamic rendering in Streamlit.

# 🐍 Python Pixel

A **futuristic, visually stunning Snake game** built entirely with **Streamlit**, featuring neon aesthetics, smooth keyboard controls, special power-ups, and a sleek UI — all running in your browser!
> Built by **Shaid** for the Social Eagle Python Challenge (Day 15).
---

## 🌟 Features

### 🎮 Core Gameplay
- Classic **Snake mechanics** with smooth directional controls.
- **Auto-collision detection** with walls and self.
- **Score tracking** with persistent **high score** across sessions.
- **Game history** panel showing your last 5 game scores.

### 💎 Special Power-Up: The Neon Diamond
- **Randomly spawns** (10% chance after eating food).
- Grants **+5 points** and **instantly grows the snake by 5 segments**.
- **Expires after 8 seconds** if not collected — shown with a live countdown timer.

### 🎨 Futuristic Visual Design
- **Neon gradient UI** with glowing text and animated borders.
- **Animated snake head** with directional eyes and blinking mouth.
- **Pulsing food** with dynamic glow effects.
- **Glowing diamond** with layered outlines for a radiant look.
- Optional **grid toggle** for cleaner or more structured visuals.

### ⌨️ Responsive Controls
- **Keyboard support**: Arrow keys or **WASD** for movement.
- **Spacebar** to pause/resume gameplay.
- **On-screen buttons** in the sidebar for touch/mobile support.
- **Robust key capture** using JavaScript to prevent page scrolling and ensure reliable input.

### 🧠 Smart Session Management
- Game state fully preserved using **Streamlit Session State**.
- **No duplicate history entries** — scores recorded only once per game.
- **Configurable speed** (1–15) via slider for beginner to expert difficulty.

### 🖥️ Layout & UX
- **Wide layout** optimized for game visibility.
- **Sidebar "Venom Panel"** with futuristic-styled controls.
- **Score HUD** with animated glowing chips.
- **Responsive design** that works on desktop and tablet.

---

## 🛠️ Requirements

- Python 3.8+
- Required packages:
  ```bash
  streamlit
  pillow
  streamlit-js-eval
  ```

Install with:
```bash
pip install streamlit pillow streamlit-js-eval
```

> 💡 Also ensure you have the `se.png` logo file in the same directory as the script.

---

## ▶️ How to Run

1. Save the code as `snake_game.py`
2. Place your `se.png` logo in the same folder
3. Run in terminal:
   ```bash
   streamlit run app.py
   ```
4. Play using **arrow keys**, **WASD**, or on-screen buttons!

---

## 🎯 Controls

| Action        | Key / Button                     |
|---------------|----------------------------------|
| Move Up       | ↑ / W / "⬆️ UP" button           |
| Move Down     | ↓ / S / "⬇️ DOWN" button         |
| Move Left     | ← / A / "⬅️ LEFT" button         |
| Move Right    | → / D / "➡️ RIGHT" button        |
| Pause/Resume  | Spacebar / "⏸️ PAUSE" button     |
| Start Game    | "▶️ START" button                |
| Restart       | "🔄 RESTART" button               |

> 📝 **Note**: The game starts paused by default. Press **START** or any direction key to begin!

---

## 📸 Preview


https://github.com/user-attachments/assets/9e6db255-3180-4e79-b99f-ebde4941e8cb



---

## 🧪 Tips for Best Experience

- Use **Chrome or Edge** for optimal JavaScript key handling.
- Avoid clicking outside the app window during gameplay to maintain focus.
- Increase **speed** gradually as you improve!

---

## 📜 License

MIT — Use, modify, and deploy freely. Perfect for portfolios, demos, or fun!

---

<div align="center">


🎓 Keep coding, keep learning!
Made with ❤️ by Shaid using Streamlit

⭐ Star this repo if it helped you learn something new! ⭐
