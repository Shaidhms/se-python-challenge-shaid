ROBO RPS — Streamlit Rock-Paper-Scissors

A futuristic Rock-Paper-Scissors built with Streamlit. Includes animated GIFs, live scoreboard, move history, and match formats (Best of 3 or Best of 5).

⸻

✨ Features
	•	Player vs CPU with crisp animations
	•	Best of 3 or Best of 5 match modes with automatic match winner announcement
	•	Scoreboard with rounds, wins, CPU score, and draws
	•	Move history dropdown with per-round details
	•	Status messages and result banners after each round
	•	Quick reset and new match controls

⸻

📂 Project Structure

day13/
├─ app.py                 # Main Streamlit app
├─ se.png                 # Logo displayed in header (place your own)
├─ requirements.txt       # Python dependencies (optional but recommended)

Minimal requirements.txt:

streamlit>=1.33
requests>=2.31


⸻

## 🔧 Setup
. What's up, baby, ma?
1.	Clone the repo
  
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>/day13
```

2.	Create a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate for Windows
```

	3.	Install dependencies


pip install -r requirements.txt
# or
pip install streamlit requests


	4.	Add your logo
	•	Put a file named se.png in the same folder as app.py.
	•	You can replace it with any PNG. The app reads it as a base64 string.
	5.	Run

streamlit run app.py



⸻

🎮 How to Play
	•	Enter your Player name at the top.
	•	Choose Match format: Best of 3 or Best of 5.
	•	Click ROCK, PAPER, or SCISSORS.
	•	The app plays the GIFs, then reveals the round result and updates the scoreboard.
	•	After the last round, the app announces the match winner and disables move buttons.
	•	Use START NEW MATCH to play again.
	•	Use RESET SCORES to clear the board and start fresh in the same format.

⸻

🖼️ GIF Configuration

The app uses a small dictionary called GIF_URLS inside app.py:

GIF_URLS = {
    "player_rock": "https://…/giphy.gif",
    "player_paper": "https://…/giphy.gif",
    "player_scissors": "https://…/giphy.gif",
    "cpu_rock": "https://…/giphy.gif",
    "cpu_paper": "https://…/giphy.gif",
    "cpu_scissors": "https://…/giphy.gif",
}

	•	Replace these with your own URLs if you want different animations.
	•	The app fetches the GIF with a browser-like header and falls back to loading by URL if needed.

⸻

🏆 Match Logic
	•	Each click triggers CPU selection and “stages” the result.
	•	The app waits briefly so the GIFs can play, then reveals the outcome.
	•	Scores are updated after the animation.
	•	Rounds increment automatically.
	•	At the end of 3 or 5 rounds, the app announces:
	•	{Player} WINS, or
	•	CPU WINS, or
	•	DRAW if scores are tied

⸻

📊 Scoreboard and History
	•	Scoreboard shows ROUND: X / N, Player score, Draws, and CPU score.
	•	Move History dropdown lists each round with the moves, result, and timestamp:

Round 3 — Paper vs Rock → WIN (12:45:08)



⸻

🧪 Developer Tools

Open the sidebar and enable Testing Mode:
	•	Set a random seed to make CPU choices reproducible during testing.

⸻

🚀 Deploy

Streamlit Community Cloud
	1.	Push this project to GitHub.
	2.	Create a new app on Streamlit Community Cloud.
	3.	Point it to day13/app.py.
	4.	Add requirements.txt if you use one.

Docker (optional sketch)

FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir streamlit requests
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]


⸻

❗ Troubleshooting
	•	GIFs feel slow
Large or remote GIFs can take time to load. Try smaller files or different hosts.
	•	No logo
Ensure se.png is present and readable. You can also comment out the logo block.
	•	Buttons disabled
After the last round in the chosen format, the match ends and buttons are disabled. Click START NEW MATCH.

⸻

📝 License

MIT. See LICENSE if included, or add one to your repo.

⸻

🙌 Credits

Built with Streamlit. GIFs credited to their respective creators. Replace the URLs if you prefer your own assets.

⸻

📸 Screenshots (optional)

Add screenshots here once you run the app:

docs/
  screenshot-1.png
  screenshot-2.png

Then reference them:

![Home](docs/screenshot-1.png)
![Round Result](docs/screenshot-2.png)


⸻

💡 Ideas to Extend
	•	First-to-2 or first-to-3 logic that ends the match early
	•	Keyboard shortcuts for moves
	•	Sounds on win or draw
	•	Local caching for custom assets

⸻

Happy playing!
