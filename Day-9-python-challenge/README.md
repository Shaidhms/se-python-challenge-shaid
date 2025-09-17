# 🦅 Social Eagle – Python Challenge Day 9

Day 9 Task :  

Quiz Game App ❓

> Features:

> Multiple-choice questions (hardcoded in list/dict).

> User selects answers via radio buttons.

> Keep score using st.session_state.

> Show final score at the end.
# 🤖 RoboQuiz Nexus — Hosted by Shaid’s AI Avatar

> *“CYBERNETIC INTELLIGENCE ASSESSMENT MODULE — VIDEO PLAYS → OPTIONS AUTO-REVEAL.”*

A cinematic, futuristic, robotic-themed quiz application built with **Streamlit**, where users interact with **Shaid’s AI Avatar** through video prompts and immersive UI. Perfect for AI/LLM education, team onboarding, or sci-fi themed learning.

🎬 **Watch. Listen. Respond.**  
✅ Video-prompted questions  
✅ Auto-reveal options after video ends  
✅ Persistent video playback  
✅ Futuristic robotic UI with glitch/neon effects  
✅ Hosted & moderated by Shaid’s AI Avatar  
✅ Fully responsive and locally embeddable

---

## 🚀 Preview

![RoboQuiz Nexus Preview](https://via.placeholder.com/800x500/0a0f1a/00ffff?text=RoboQuiz+Nexus+Preview)  
*(Replace with actual screenshot or GIF when deployed)*

---

## ✨ Features

- **Cinematic Boot Sequence** — Title → AI Avatar → Caption → System Boot → Input
- **Video-First UX** — Questions are asked via video. Options auto-appear after video ends.
- **Persistent Video** — Prompt video stays visible during answer selection and feedback.
- **Robotic UI** — Glitch effects, scanlines, neon glow, Orbitron font, cyberpunk glass panels.
- **AI Hosted** — Every interaction is attributed to **Shaid’s AI Avatar** for immersion.
- **Reusable Feedback** — Correct/Wrong videos reused across questions to minimize assets.
- **Session State Managed** — Smooth navigation, score tracking, and replay support.
- **No Double Refresh** — Optimized activation flow to prevent UI flicker.

---

## 📦 Installation

### Prerequisites

- Python 3.9+
- `pip` or `conda`

### Steps

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/roboquiz-nexus.git
cd roboquiz-nexus
```

2. **Set up virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install streamlit
```

4. **Prepare media files**

Create folders and add your videos/audio:

```
📁 videos/
   ├── q1_prompt.mp4
   ├── q2_prompt.mp4
   ├── q3_prompt.mp4
   ├── q4_prompt.mp4
   ├── q5_prompt.mp4
   ├── q1_correct.mp4
   └── q1_wrong.mp4

📁 audio/
   └── intro.mp3
```

> 💡 You can replace these with HTTPS URLs in `QUIZ` data if hosting externally.

5. **Run the app**

```bash
streamlit run app.py
```

6. **Open in browser** → `http://localhost:8501`

---

## 🧩 Quiz Structure

Defined in `app.py` → `QUIZ` list. Each question includes:

```python
{
    "id": "q1",
    "question_text": "What is RAG?",
    "options": [...],
    "answer": "...",
    "videos": {
        "prompt": "videos/q1_prompt.mp4",
        "correct": "videos/q1_correct.mp4",
        "wrong": "videos/q1_wrong.mp4"
    },
    "duration": 6  # in seconds — used for auto-reveal timing
}
```

Add or modify questions as needed.

---

## 🎨 Customization

### Fonts & Colors

- Font: `Orbitron` (imported via Google Fonts)
- Primary Glow: `#00ffff` (cyan)
- Secondary: `#ff55ff` (magenta), `#00ffaa` (teal)
- Background: Cyberpunk dark with circuit overlays

Edit in `<style>` block in `app.py`.

### Media

Replace `videos/` and `audio/` files. Ensure:
- Videos are MP4 (H.264) for browser compatibility.
- Keep prompt videos short (5–10 sec) for best UX.
- Update `duration` field to match video length.

---

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **Styling**: CSS + HTML (via `st.markdown` and `st.components.v1.html`)
- **Media Embedding**: Base64 inline for local files
- **State Management**: `st.session_state`
- **No External JS** — Pure Python + Streamlit

---

## 🧪 Known Limitations

- Video end detection uses `time.sleep(duration)` — not event-driven (due to Streamlit constraints).
- Audio autoplay requires user interaction first (browser policy).
- For production, consider hosting videos on CDN and using HTTPS URLs.

---

## 📸 Screenshots

| Boot Sequence | Question Screen | Feedback Screen |
|---------------|-----------------|-----------------|
| ![Boot](https://via.placeholder.com/300x500/0a0f1a/00ffaa?text=System+Boot) | ![Question](https://via.placeholder.com/300x500/0a0f1a/00ffff?text=Video+%2B+Options) | ![Feedback](https://via.placeholder.com/300x500/0a0f1a/ff55ff?text=Correct%2FWrong) |

*(Add real screenshots in `/screenshots` folder and link here)*

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙌 Acknowledgements

- **Shaid’s AI Avatar** — The charismatic host of this cognitive assessment module.
- [Streamlit](https://streamlit.io) — For making interactive AI apps a breeze.
- [Google Fonts - Orbitron](https://fonts.google.com/specimen/Orbitron) — For that futuristic terminal vibe.
- Cyberpunk aesthetic inspirations — Blade Runner, Ghost in the Shell, Neon Genesis Evangelion.

---

## 💬 Feedback / Support

Built something cool with this? Found a bug? Want Shaid’s AI Avatar to say something specific?

→ Open an [Issue](https://github.com/yourusername/roboquiz-nexus/issues) or tag @shaid on Twitter/X.


---

### 🗃️ Repository Structure

```
roboquiz-nexus/
├── app.py                  # Main Streamlit app
├── videos/                 # Video prompts and feedback
├── audio/                  # Intro and sound effects
├── screenshots/            # (Optional) UI previews
├── README.md               # You are here
└── LICENSE                 # MIT License
```

---

-----

## 📄 License

This project is licensed under the MIT License.



<div align="center">


🎓 Keep coding, keep learning!
Made with ❤️ by Shaid using Streamlit

⭐ Star this repo if it helped you learn something new! ⭐

</div>
