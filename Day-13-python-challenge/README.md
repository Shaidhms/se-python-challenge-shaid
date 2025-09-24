# 🦅 Social Eagle – Python Challenge Day 13

Day 13 Task : 
 
Rock , Paper , scissors￼Game !

# 🤖 ROBO RPS — Streamlit Rock-Paper-Scissors Arcade

> A cinematic, neon-drenched, hyper-stylized Streamlit app with match formats, animated GIFs, live stats, and arcade flair — all in one file.  
> Built by **Shaid** for the Social Eagle Python Challenge (Day 13).

---

## 🌟 Features

✅ **Futuristic Neon UI** — Glowing buttons, animated transitions, cinematic result banners  
✅ **Player vs CPU Showdown** — Crisp animations with synchronized GIF reveals  
✅ **Match Formats** — Choose **Best of 3** or **Best of 5** — auto-declares winner at match end  
✅ **Live Scoreboard** — Tracks rounds, wins, draws, CPU score — updates in real-time  
✅ **Move History Log** — Dropdown reveals every round’s moves, result, and timestamp  
✅ **Result Animations** — Status banners pulse after each round: “YOU WIN 🎉”, “DRAW 🤝”, “CPU WINS 💀”  
✅ **Quick Controls** — One-click **START NEW MATCH** or **RESET SCORES**  
✅ **Testing Mode** — Sidebar toggle to set random seed for reproducible CPU moves  
✅ **Responsive Design** — Glows on mobile, desktop, and tablet  
✅ **Single File, Zero External Assets** — Only dependencies: `streamlit`, `requests`

---

## 🎮 Ultra-Realistic Futuristic RPS Arena

> *No quarters needed. Just pure digital adrenaline.*

---

## 📸 Demo video



https://github.com/user-attachments/assets/14f29ec1-6a88-45ea-bed3-fd1ca2e78bc5



---
## 🚀 How to Run

### 1. Clone or Create

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>/day13
```

> Or just copy `app.py` into a new folder.

### 2. (Optional) Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate for Windows
```

### 3. Install Dependencies

```bash
pip install streamlit requests
# or
pip install -r requirements.txt
```

### 4. Add Your Logo (Optional)

Place `se.png` in the same folder as `app.py`.  
> The app auto-converts it to base64. Missing? No problem — UI degrades gracefully.

### 5. Launch the App

```bash
streamlit run app.py
```

Open the URL shown in your terminal (usually `http://localhost:8501`).

---

## 🕹️ How to Play

1. **Enter Your Name** — Personalize your player tag at the top.
2. **Choose Match Format** — Best of 3 or Best of 5? The stakes are yours to set.
3. **Make Your Move** — Click **ROCK 🪨**, **PAPER 📜**, or **SCISSORS ✂️**.
4. **Watch the Duel** — GIFs animate simultaneously — then BAM — result revealed with flair.
5. **Track Progress** — Live scoreboard updates. History dropdown logs every clash.
6. **Match End** — Winner announced with cinematic banner. Buttons auto-disable.
7. **Reset or Replay** — Hit **START NEW MATCH** to go again — or **RESET SCORES** for a clean slate.

---

## 🧩 Code Structure

All logic lives in one file: `app.py`

- **Session State** — Manages scores, rounds, history, match format, player name
- **GIF Animation Engine** — Fetches + displays player/CPU move GIFs with fallback headers
- **Match Logic** — Auto-detects win conditions, ends match early if format met
- **UI Components** — Header, move buttons, scoreboard, history dropdown, reset controls
- **Testing Mode** — Sidebar seed control for deterministic CPU behavior

---

## 🖼️ GIF Configuration

Customize animations by editing the `GIF_URLS` dictionary inside `app.py`:

```python
GIF_URLS = {
    "player_rock": "https://media.giphy.com/media/...",
    "player_paper": "https://media.giphy.com/media/...",
    "player_scissors": "https://media.giphy.com/media/...",
    "cpu_rock": "https://media.giphy.com/media/...",
    "cpu_paper": "https://media.giphy.com/media/...",
    "cpu_scissors": "https://media.giphy.com/media/...",
}
```

> Replace URLs with your own. App uses `requests` with browser-like headers for reliability.

---

## 🏆 Match Logic Deep Dive

- Each move triggers CPU selection + result staging.
- Brief pause lets GIFs play → then reveals outcome.
- Round counter auto-increments.
- Match ends when:
  - Player or CPU reaches `ceil(total_rounds/2)`
  - OR final round reached → winner declared
- Ties? “DRAW” banner glows ominously.

---

## 📊 Scoreboard & History

**Live Scoreboard**  
> `ROUND: 2 / 5` | `YOU: 1` | `CPU: 0` | `DRAWS: 1`

**Move History Dropdown**  
> `Round 1 — Rock vs Paper → LOSS (14:22:07)`  
> `Round 2 — Scissors vs Scissors → DRAW (14:22:19)`  
> `Round 3 — Paper vs Rock → WIN (14:22:33)`

---

## 🧪 Developer Tools

Enable **Testing Mode** in sidebar:
- Set `random_seed` for reproducible CPU choices
- Perfect for debugging match logic or GIF timing

---

## 🚨 Troubleshooting

**Issue**: GIFs load slowly or fail  
**Fix**: Use smaller GIFs or host on faster CDN (e.g., Imgur, Giphy direct links)  
**Fallback**: App uses `streamlit.image(url)` if `requests` fails

**Issue**: No logo appears  
**Fix**: Ensure `se.png` is in folder + readable. Or comment out logo block in code.

**Issue**: Buttons stay disabled after match  
**Fix**: Click **START NEW MATCH** — it resets round counter and re-enables controls.

---

## 📦 Dependencies

```txt
streamlit>=1.33
requests>=2.31
```

> Works on older Streamlit — logic patched for backward compatibility.

---

## 💡 Ideas to Extend

- **Early Win Detection** — End match as soon as player/cpu hits required wins
- **Keyboard Shortcuts** — `R`, `P`, `S` to trigger moves
- **Sound FX** — Inject `<audio>` tags for win/loss/draw sounds
- **Asset Caching** — Locally cache GIFs for faster reloads
- **Themes** — Add “Cyberpunk”, “Neon Arena”, “Retro Arcade” CSS skins
- **Multiplayer LAN** — WebRTC or socket-based P2P mode (ambitious!)

---

## 📜 License

MIT — Use, modify, deploy freely. Perfect for portfolios, demos, or fun!

---


## ⭐ Pro Tips

- Try **Best of 5** — the tension builds with every round!
- Enable **Testing Mode** to practice against predictable CPU.
- Watch the **Move History** — learn your patterns, outsmart the machine.

---

<div align="center">

🎓 Keep coding, keep learning!  
Made with ❤️ by Shaid using Streamlit

⭐ Star this repo if it helped you learn something new! ⭐

</div>

