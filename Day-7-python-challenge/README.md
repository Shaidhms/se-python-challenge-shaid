Here you go — the entire README written out in Markdown format so you can directly use it in your repo:

# 🦅 Social Eagle – Python Challenge Day 8

Day 8 Task :  

Gym Workout Logger 🏋️

> Log exercises (sets, reps, weight).

> Store history in a table.

> Show weekly progress graph.



---

## ⚡ NeuroLift Gesture Log — Python Challenge Day 8

> **Welcome to Day 8!** This is a cyber-styled, multi-tab **Streamlit** app that lets you **log workouts by camera gestures or voice**, tracks progress with **Plotly** charts, and syncs data to **Firebase Realtime Database**. It also has **gamification** (XP, levels, NeuroCredits, upgrades) and a fun **“Motivate Me”** YouTube Shorts boost.
Vision-powered workout logging with gestures, voice, AI suggestions, and cloud sync.
---

## ✨ Features

### 🖐️ **Vision & Gesture Logging**
- **Two-finger ✌️ = Log** a quick set (uses your last template or most recent set as defaults).
- **Open palm 🖐️ = Undo** the most recent entry (deletes last row and saves).
- Live on-screen HUD shows what the model “sees” (fingers, gaps, ratios).
- Optional **sensitivity slider** (strict → permissive) for real-world lighting.

### 🎙️ **Voice Command Logging**
- Click **Start Listening**, say things like:
  - “Bench Press 3 sets 8 reps 135 pounds”
  - “Log squat 5 by 5 at 100”
  - “Bench press 3 sets” (reps/weight default from previous context)
- Parser supports number words (“one”, “two”, … “twenty”), flexible patterns, and safe fallbacks.

### 🤖 **AI Suggestions + Kinetic Sync**
- Predicts your **next weight** per exercise with simple linear regression.
- **Kinetic Sync (750 NeuroCredits)**: Auto-adjusts suggestions using your recent RPE:
  - Avg RPE ≥ 9 → −5 lb
  - Avg RPE ≥ 8 → −2.5 lb
  - Avg RPE ≤ 6 → +2.5 lb
  - Avg RPE ≤ 5 → +5 lb
- Displays rationale inline and rounds to the nearest 2.5 lb.

### 🧪 **Adrenaline Boost (Timed)**
- **Adrenaline Injector (1000 NeuroCredits)**: 60-minute window with **+5% XP & credits**.
- Sidebar badge shows remaining time and active multiplier.
- Boost automatically applied to **all** XP/credit awards during the window.

### 🏆 **Gamification**
- **XP & Levels**: Earn XP from volume; level-up updates progress targets.
- **NeuroCredits**: Earn credits from volume and achievements.
- **Badges**: Level badges + space for future achievements.
- **Battle Your Ghost**: Compares this week vs last week and rewards wins.

### ☁️ **Cloud Sync + Local Fallback**
- **Firebase Realtime Database** sync for all logs (`users/default_user/workouts`).
- If Firebase isn’t configured, app runs in **local JSON** mode.
- “Cloud Sync: ACTIVE” label when connected.

### 📊 **Visual Analytics**
- **Weekly Volume** line chart (Plotly).
- **Personal Records** bar chart per exercise.
- Clean, cyber UI with custom CSS and metrics.

### 🎥 **Motivation Booster**
- **Motivate Me** button: plays a random **YouTube Short** (autoplay with sound).
- **Close Video** appears only when a video is visible.

### 💾 **History & Controls**
- Pretty dataframe view with date/time formatting and PR markers.
- **Delete single entry** via dropdown.
- **Clear Today’s Logs** button.
- Toasts and sounds (optional) instead of spammy pop-ups.

---

## 🖥️ Screen Shot

_Add your screenshot(s) here._

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** (3.11 works)
- **pip** package manager
- **macOS** users: enable **camera** and **microphone** permissions for your terminal/IDE

### Installation

1) **Clone the repository**
```bash
git clone https://github.com/Shaidhms/se-python-challenge-shaid.git
cd se-python-challenge-shaid/day\ 8

	2.	Create & activate a virtual environment (recommended)

python -m venv venv
source venv/bin/activate       # macOS/Linux
# or on Windows:
# venv\Scripts\activate

	3.	Install dependencies

pip install -r requirements.txt

	4.	Run the app

streamlit run neuro-lift-app.py

	5.	Open your browser

	•	Local: http://localhost:8501

⸻

🎯 How to Use
	1.	Configure Firebase (optional but recommended)
	•	In neuro-lift-app.py, replace the firebaseConfig dict with your project keys:
	•	apiKey, authDomain, databaseURL, projectId, storageBucket, messagingSenderId, appId, measurementId
	•	If you skip this, the app runs in local JSON mode.
	2.	Log a Set (Manual)
	•	Go to Log Workout tab.
	•	Pick exercise, sets, reps, weight, RPE.
	•	Click LOG SET — ACTIVATE NEURAL SYNC.
	•	Check the toast + History tab.
	3.	Log by Voice
	•	Go to Voice/Gesture tab → Start Listening.
	•	Speak: “Log Bench Press 3 sets 8 reps 135 pounds”
	•	You’ll see “You said: …” and a toast if it logs.
	4.	Log by Gesture
	•	In Voice/Gesture, set Gesture sensitivity if needed.
	•	Click Start Camera Gesture Detection.
	•	✌️ Two fingers = Log, 🖐️ Open palm = Undo.
	•	You’ll see HUD info and a success toast.
	5.	Motivation
	•	Sidebar → Motivate Me to autoplay a random YouTube Short.
	•	Close Video to hide it.
	6.	Progress & History
	•	Progress tab for weekly volume & PRs.
	•	History tab to review, delete single entries, or Clear Today’s Logs.
	7.	Upgrades & Levels
	•	Cyber Upgrades tab:
	•	Unlock Kinetic Sync and Adrenaline Injector with NeuroCredits.
	•	Watch adrenaline badge and XP bar update live.

⸻

🧠 What’s Inside (Code Overview)
	•	RoboTrainer
	•	Tracks quotes, upgrades, NeuroCredits, XP/Level, badges.
	•	unlock_upgrade(name) starts Adrenaline timer and toggles Kinetic Sync.
	•	award_credits/add_xp support a “quiet” mode (no extra pop-ups).
	•	level_up() shows a sidebar success + toast (no image card).
	•	WorkoutLogger
	•	Loads/saves data from Firebase or local JSON.
	•	log_workout(), delete_by_index(), clear_today() mutate and persist.
	•	get_weekly_progress() and get_prs() power the charts.
	•	predict_next_weight() (per exercise) drives the suggestion.
	•	Gesture Detection (detect_gesture)
	•	Captures frames, thresholding to hand silhouette.
	•	Finds contours, convex hull, and convexity defects (valleys).
	•	Estimates fingers ≈ gaps + 1, with fallbacks and sensitivity.
	•	Mapping: 2 fingers → LOG, 4–5 fingers (open palm) → UNDO.
	•	Voice
	•	recognize_speech() uses SpeechRecognition (Google recognizer).
	•	parse_voice_command() supports multiple natural patterns + defaults.
	•	UI/UX
	•	Five tabs: Log Workout, Voice/Gesture, Progress, History, Cyber Upgrades.
	•	Sidebar: status, Quick Actions, Motivate Me, upgrades guide, Cloud Sync.
	•	Custom CSS for a cyber vibe; Plotly charts for visuals.

⸻

🧪 Troubleshooting & Tips
	•	macOS Camera Authorization
	•	System Settings → Privacy & Security → Camera → allow your terminal/IDE.
	•	If you never get a prompt, try launching once from a simple script on the main thread to trigger it.
	•	Microphone for Voice
	•	Install PortAudio + PyAudio (macOS):

brew install portaudio
pip install pyaudio


	•	Autoplay with Sound
	•	Browsers may require a user click (your Motivate Me button qualifies).
	•	If muted, click the player once to activate audio.
	•	Firebase 400 / Invalid JSON
	•	We write a JSON-safe list (allow_nan=False, stringified timestamps).
	•	If you edited the DB manually, clear invalid data or reset the workouts node.

⸻

🏆 Achievements Unlocked
	•	✅ Vision-based gesture logging in Streamlit
	•	✅ Robust voice command parsing with fallbacks
	•	✅ AI-assisted weight suggestions + fatigue-aware tuning
	•	✅ Gamified XP/levels, credits, timed boosts
	•	✅ Firebase cloud sync + local fallback
	•	✅ Clean multi-tab UI with charts and history controls

⸻

📝 Requirements

Add these to requirements.txt (already used by the app):

streamlit
pandas
plotly
numpy
opencv-python
SpeechRecognition
pyttsx3
pygame            # optional (sounds)
pyrebase4         # if using Firebase via pyrebase
requests          # pyrebase dependency
scikit-learn      # AI weight suggestion

macOS voice optional:

pyaudio           # requires 'brew install portaudio'

Note: If you installed pyrebase previously, prefer pyrebase4, or keep the one your code imports. Make sure your firebaseConfig values are valid.

⸻

🤝 Contributing

Have ideas to supercharge NeuroLift Gesture Log? PRs welcome!
	1.	Fork the repo
	2.	Create a feature branch (git checkout -b feature/gesture-tuner)
	3.	Implement your changes with basic tests
	4.	Commit (git commit -m "Add gesture sensitivity slider")
	5.	Push (git push origin feature/gesture-tuner)
	6.	Open a Pull Request

Ideas
	•	Fine-tuned gesture model (MediaPipe Hands)
	•	Multi-user auth with Firebase Auth
	•	Exercise templates and superset flows
	•	Auto-PR detection and per-exercise analytics
	•	Export to CSV/Google Sheets

⸻

📄 License

This project is licensed under the MIT License.

⸻


<div align="center">


  

<h2>Social Eagle Python Challenge</h2>
<h3>NeuroLift Gesture Log</h3>


🎓 Keep coding, keep learning!
Made with ❤️ by Shaid using Streamlit

⭐ Star this repo if it helped you learn something new! ⭐

</div>
```
