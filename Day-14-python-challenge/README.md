# 🦅 Social Eagle – Python Challenge Day 14

Day 14 Task : 
 
>Stop Watch
>Start/stop/reset timer


## 🕒 SpectraLap – Immersive Stopwatch with Lap Tracking

**SpectraLap** is a sleek, futuristic stopwatch web app built with **Streamlit**, featuring lap tracking, customizable watch mockups, immersive themes, and sound cues — all wrapped in a cyberpunk-inspired UI with neon aesthetics and glass-morphism design.
> Built by **Shaid** for the Social Eagle Python Challenge (Day 14).
---
## 📸 Demo



https://github.com/user-attachments/assets/e5198a62-efcc-4ac4-94b6-df6899778eae



---

## ✨ Features

### ⏱️ Core Stopwatch Functionality
- **Start / Stop** timer with a single click
- **Reset** to zero with full state clearance
- **Lap tracking** with:
  - Lap number
  - Individual lap time
  - Cumulative time
  - Delta (difference from previous lap)

### 🎨 Immersive Visual Themes
- **6 built-in high-resolution wallpapers**:
  - Carbon Fiber
  - Brushed Metal
  - Leather Desk
  - Wood Desk
  - Marble
  - Dark Concrete
- **Custom wallpaper upload** (PNG, JPG, JPEG, WebP)
- Dynamic background blending with dark overlay for readability

### 🕶️ Watch Mockup Mode
- Render the stopwatch **inside a realistic watch image**
- Fully customizable mockup parameters:
  - Mockup width & height (300–2000 px)
  - Dial diameter (120–1500 px)
  - X & Y offset for precise positioning
- Upload your own **watch bezel/image** as a frame
- Real-time preview with drag-and-drop support

### 💾 Preset Management
- **Save**, **apply**, and **delete** mockup configurations as named presets
- Presets persist across sessions using local JSON storage (`mock_presets.json`)
- One-click recall of favorite layouts

### 🔊 Sound Cues (Optional)
- **Tick sound** every second while running (via embedded base64 audio)
- **Blip sound** on each lap recorded
- Toggle sound on/off (currently UI commented out but functional)

### 🌐 Responsive & Futuristic UI
- **Orbitron** (cyberpunk) and **Poppins** fonts
- Neon cyan, purple, and mint color scheme
- Animated **scanlines**, **glitch effects**, and **pulse animations**
- **Glass-morphism cards** with backdrop blur
- Fully responsive on mobile and desktop

### 🧠 Smart State Management
- Uses `st.session_state` for persistent UI and timer state
- Auto-rerun every 50ms when running for smooth time updates
- Handles file uploads and custom images across Streamlit reruns

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `streamlit`, `pandas` (automatically installed via requirements)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/spectralap.git
   cd spectralap
   ```

2. Install dependencies:
   ```bash
   pip install streamlit pandas
   ```

3. Ensure you have a logo file named `se.png` in the root directory (or update the path in the code).

4. Run the app:
   ```bash
   streamlit run app.py
   ```

> 💡 **Note**: The app will auto-create `mock_presets.json` to save your watch mockup presets.

---

## 📁 Project Structure
```
spectralap/
├── app.py                 # Main Streamlit application
├── se.png                 # Logo file (required)
├── mock_presets.json      # Auto-generated preset storage (optional)
└── README.md              # This file
```

---

## 🛠️ Customization

### Adding Your Logo
Replace `se.png` with your own 40px-height logo in PNG format.

### Modifying Themes
Edit the `WALLPAPERS` dictionary in `app.py` to change or add background images (must be Unsplash or public URLs).

### Disabling Sound
The sound toggle UI is currently commented out. To re-enable:
- Uncomment the sound toggle section in the main layout
- Ensure browser allows autoplay (may require user interaction)

---


## 🤝 Contributing
Pull requests welcome! Feel free to:
- Add new wallpaper options
- Improve sound system (Web Audio API)
- Add export lap data (CSV/JSON)
- Implement dark/light mode toggle

---

## 📜 License
MIT License – feel free to use, modify, and distribute.

---

<div align="center">


🎓 Keep coding, keep learning!
Made with ❤️ by Shaid using Streamlit

⭐ Star this repo if it helped you learn something new! ⭐

---
