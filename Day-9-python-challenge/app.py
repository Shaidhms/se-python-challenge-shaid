import streamlit as st
from typing import List, Dict
from streamlit.components.v1 import html
import os
import base64
import time
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("se.png")



# ---------- Page + Style ----------
st.set_page_config(page_title="RoboQuiz Nexus", page_icon="🤖", layout="centered")

# Futuristic Robotic Theme with Circuitry, Glitch, and Metallic Glass
st.markdown("""
<style>
/* Cyberpunk Robotic Background */
.stApp {
  background: 
    linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 50%, #1a0f1a 100%),
    repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(0, 255, 255, 0.03) 10px, rgba(0, 255, 255, 0.03) 20px),
    radial-gradient(circle at 30% 30%, rgba(0, 255, 200, 0.08), transparent 40%),
    radial-gradient(circle at 70% 70%, rgba(255, 0, 150, 0.08), transparent 40%);
  color: #c0ffef;
  font-family: 'Orbitron', 'Courier New', monospace;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.7);
}

/* Import Orbitron Font */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&display=swap');

/* Glitch Title Effect */
@keyframes glitch {
  0% { text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff; }
  10% { text-shadow: 2px 0 5px #ff00ff, -2px -2px 10px #00ffff; }
  20% { text-shadow: -2px 0 5px #00ff00, 2px 2px 10px #ff00ff; }
  30% { text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff; }
  100% { text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff; }
}

h1, h2, h3 {
  font-family: 'Orbitron', 'Courier New', monospace;
  letter-spacing: 1px;
  text-transform: uppercase;
  animation: glitch 3s infinite;
  position: relative;
}

/* Robotic Glass Panel */
.glass {
  background: rgba(10, 10, 20, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  padding: 24px;
  box-shadow: 
    0 0 15px rgba(0, 255, 255, 0.2),
    inset 0 0 10px rgba(0, 200, 255, 0.1);
  position: relative;
  overflow: hidden;
  margin: 16px 0;
}

.glass::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, #00ffff, transparent);
  animation: scan 2s linear infinite;
}

@keyframes scan {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}

/* Progress Bar - Reactor Core Style */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, #ff0066, #00ffff);
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.7);
}

/* Robotic Option Buttons (Replaces Radio) */
.option-card {
  background: rgba(0, 40, 60, 0.6);
  border: 2px solid rgba(0, 255, 255, 0.4);
  border-radius: 8px;
  padding: 16px;
  margin: 8px 0;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  text-align: center;
  font-weight: bold;
  font-family: 'Orbitron', monospace;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.option-card:hover {
  background: rgba(0, 80, 100, 0.8);
  border-color: #00ffff;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
}

.option-card.selected {
  background: rgba(0, 255, 255, 0.2);
  border-color: #00ffaa;
  box-shadow: 0 0 20px rgba(0, 255, 170, 0.6);
  animation: pulse 1.5s infinite;
}

.option-card.correct {
  background: rgba(0, 255, 100, 0.2);
  border-color: #00ff44;
  box-shadow: 0 0 25px rgba(0, 255, 68, 0.8);
}

.option-card.incorrect {
  background: rgba(255, 50, 50, 0.2);
  border-color: #ff3333;
  box-shadow: 0 0 25px rgba(255, 51, 51, 0.8);
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(0, 255, 170, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(0, 255, 170, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 255, 170, 0); }
}

/* Futuristic Buttons */
.stButton>button {
  background: linear-gradient(90deg, #003366, #0066ff);
  color: #ffffff;
  border: 2px solid #00ccff;
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: bold;
  font-family: 'Orbitron', monospace;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 4px 10px rgba(0, 100, 255, 0.3);
  transition: all 0.3s ease;
}

.stButton>button:hover {
  background: linear-gradient(90deg, #0066ff, #00ccff);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 200, 255, 0.6);
}

.stButton>button:disabled {
  opacity: 0.5;
  filter: grayscale(50%);
  transform: none;
  cursor: not-allowed;
}

/* Scanline Overlay (Optional Retro Robotic Effect) */
.scanlines {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%);
  background-size: 100% 4px;
  z-index: 9999;
  pointer-events: none;
  opacity: 0.3;
}

/* Hide Streamlit Branding */
footer {visibility: hidden;}
header {visibility: hidden;}
</style>

<div class="scanlines"></div>
""", unsafe_allow_html=True)

# ---------- Your quiz data ----------
QUIZ: List[Dict] = [
    {
        "id": "q1",
        "question_text": "What is RAG?",
        "options": ["LLM", "Chatgpt", "Retrieval Augmented Generation", "Re-Gen"],
        "answer": "Retrieval Augmented Generation",
        "videos": {
            "prompt": "videos/q1_prompt.mp4",
            "correct": "videos/q1_correct.mp4",
            "wrong": "videos/q1_wrong.mp4"
        }
    },
    {
        "id": "q2",
        "question_text": "A poorly designed prompt may cause?",
        "options": ["Hallucination", "Memory", "Tokenization", "Optimization"],
        "answer": "Hallucination",
        "videos": {
            "prompt": "videos/q2_prompt.mp4",
            "correct": "videos/q1_correct.mp4",   # Reuse q1 correct
            "wrong": "videos/q1_wrong.mp4"        # Reuse q1 wrong
        }
    },
    {
        "id": "q3",
        "question_text": "In LangChain, documents are split using a?",
        "options": ["Tokenizer", "Splitter", "Retriever", "Chain"],
        "answer": "Splitter",
        "videos": {
            "prompt": "videos/q3_prompt.mp4",
            "correct": "videos/q1_correct.mp4",   # Reuse q1 correct
            "wrong": "videos/q1_wrong.mp4"        # Reuse q1 wrong
        }
    },
    {
        "id": "q4",
        "question_text": "Which LLM is developed by OpenAI?",
        "options": ["Claude", "Gemini", "GPT", "Falcon"],
        "answer": "GPT",
        "videos": {
            "prompt": "videos/q4_prompt.mp4",
            "correct": "videos/q1_correct.mp4",   # Reuse q1 correct
            "wrong": "videos/q1_wrong.mp4"        # Reuse q1 wrong
        }
    },
    {
        "id": "q5",
        "question_text": "Chain-of-Thought prompting helps with?",
        "options": ["Creativity", "Reasoning", "Translation", "Storage"],
        "answer": "Reasoning",
        "videos": {
            "prompt": "videos/q5_prompt.mp4",
            "correct": "videos/q1_correct.mp4",   # Reuse q1 correct
            "wrong": "videos/q1_wrong.mp4"        # Reuse q1 wrong
        }
    },
]

TOTAL = len(QUIZ)
QUIZ_NAME = "ROBOQUIZ NEXUS"

# ---------- Session State ----------
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "stage" not in st.session_state:
    st.session_state.stage = "prompt"
if "selected" not in st.session_state:
    st.session_state.selected = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "started" not in st.session_state:
    st.session_state.started = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "play_intro" not in st.session_state:
    st.session_state.play_intro = False

def reset_for_next():
    st.session_state.stage = "prompt"
    st.session_state.selected = None

def autoplay_video(url: str, muted: bool = False, box_height: int = 640):
    src = url
    try:
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("/")):
            root = os.path.dirname(__file__)
            path = url if os.path.isabs(url) else os.path.join(root, url)
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            src = f"data:video/mp4;base64,{b64}"
    except Exception:
        pass

    html(f"""
    <style>
      .portrait-box {{
        position: relative;
        width: 100%;
        max-width: 480px;
        aspect-ratio: 9 / 16;
        background: #000;
        margin: 0 auto;
        border: 3px solid #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
      }}
      @supports not (aspect-ratio: 1) {{
        .portrait-box::before {{
          content: "";
          display: block;
          padding-top: 177.78%;
        }}
      }}
      .portrait-box > video {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        background: #000;
        display: block;
      }}
    </style>

    <div class="portrait-box" style="height:{box_height}px">
      <video autoplay {"muted" if muted else ""} playsinline controls>
        <source src="{src}" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>
    """, height=box_height)

def autoplay_audio(url: str, loop: bool = False):
    src = url
    try:
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("/")):
            root = os.path.dirname(__file__)
            path = url if os.path.isabs(url) else os.path.join(root, url)
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            src = f"data:audio/mpeg;base64,{b64}"
    except Exception:
        pass

    html(f"""
    <audio autoplay {"loop" if loop else ""}>
      <source src="{src}">
      Your browser does not support the audio element.
    </audio>
    """, height=0)

# ---------- Header + Boot Sequence ----------
if not st.session_state.started:
    # Placeholders for sequential reveal
    header_placeholder=st.empty()
    title_placeholder = st.empty()
    avatar_placeholder = st.empty()  # 👈 New: for "Hosted by Shaid's AI Avatar"
    caption_placeholder = st.empty()
    boot_panel_placeholder = st.empty()


    #show header
    header_placeholder.markdown(
    f"""
    <h2 class="main-header">
        <center>  <img src="data:image/png;base64,{logo_base64}" width="40" style="vertical-align: middle; margin-left:5px;"></center>
           <center> Social Eagle Python Challenge </center>
        <center> Day 9 - Quiz App</center>
    </h2>
    """,
    unsafe_allow_html=True
)
    time.sleep(1.0)
    # Step 1: Show Title
    title_placeholder.markdown("""
    <div style='text-align: center; margin: 40px 0 10px 0; font-family: Orbitron; text-transform: uppercase; letter-spacing: 2px;'>
        <div style='font-size: 2.5rem; color: #00ffff; text-shadow: 0 0 10px #00ffff;'>ROBOQUIZ NEXUS</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(1.0)

    # Step 2: Show "Hosted by Shaid's AI Avatar" (NEW)
    avatar_placeholder.markdown("""
    <div style='text-align: center; margin-bottom: 15px; font-family: Orbitron; letter-spacing: 1px;'>
        <div style='font-size: 1.1rem; color: #ff55ff; text-shadow: 0 0 8px #ff55ff;'>HOSTED BY SHAID’S AI AVATAR</div>
    </div>
    """, unsafe_allow_html=True)

    

    time.sleep(0.8)

    # Step 3: Show Caption
    caption_placeholder.caption("CYBERNETIC INTELLIGENCE ASSESSMENT MODULE — AWAITING SYSTEM INITIALIZATION...")
    time.sleep(1.2)

    # Step 4: Show Glass Panel with Boot Message
    boot_panel_placeholder.markdown("""
    <div class='glass' style='text-align: center; padding: 30px;'>
        <div style='font-family: Orbitron; font-size: 1.5rem; color: #00ffaa; margin-bottom: 15px;'>
            SYSTEM BOOT INITIATED
        </div>
        <div style='font-size: 0.95rem; color: #aaa; margin-top: 10px;'>
            AWAITING USER INPUT. PREPARE FOR COGNITIVE CALIBRATION.
        </div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(1.2)



# Step 4: Show Input + Button
    #st.markdown("<div class='glass' style='padding: 30px;'>", unsafe_allow_html=True)

    st.session_state.user_name = st.text_input(
        "ENTER OPERATOR DESIGNATION",
        value=st.session_state.user_name,
        placeholder="e.g., UNIT-7"
    )
    
    st.write(" ")
    st.write("PRESS **ACTIVATE MODULE** TO ENABLE AUDIO/VIDEO SUBSYSTEMS.")

    # if st.button("▶ ACTIVATE MODULE", use_container_width=True, type="primary"):
    #     st.session_state.started = True
    #   #  st.session_state.play_intro = True
    #     st.rerun()

    if st.button("▶ ACTIVATE MODULE", use_container_width=True, type="primary"):
        st.session_state.started = True
      #  st.session_state.play_intro = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

#     # Step 5: Show Input + Button
#    # st.markdown("<div class='glass' style='padding: 30px;'>", unsafe_allow_html=True)
#     st.session_state.user_name = st.text_input(
#         "ENTER OPERATOR DESIGNATION",
#         value=st.session_state.user_name,
#         placeholder="e.g., UNIT-7"
#     )
#     st.write(" ")
#     st.write("PRESS **ACTIVATE MODULE** TO ENABLE AUDIO/VIDEO SUBSYSTEMS.")

#     # if st.button("▶ ACTIVATE MODULE", use_container_width=True, type="primary"):
#     #     st.session_state.started = True
#     #     st.session_state.play_intro = True
#     #     st.rerun()

#     #new
#     if st.button("▶ ACTIVATE MODULE", use_container_width=True, type="primary"):
#         st.session_state.started = True
#         # Phase 1: Just mark for intro — don't play yet
#         st.session_state.deferred_play_intro = True  # 👈 New flag
#         st.rerun()

#     st.markdown("</div>", unsafe_allow_html=True)
#     st.stop()    

# ---------- Header (After Boot) ----------
st.markdown("""
<div style='text-align: center; margin-bottom: 10px; font-family: Orbitron; text-transform: uppercase; letter-spacing: 2px;'>
     <div style='font-size: 2rem; margin-top: 5px;'>ROBOQUIZ NEXUS</div>
    <div style='font-size: 1.1rem; color: #ff55ff; text-shadow: 0 0 8px #ff55ff;'>HOSTED BY SHAID’S AI AVATAR</div>
</div>
""", unsafe_allow_html=True)

#st.caption("CYBERNETIC INTELLIGENCE ASSESSMENT MODULE — VIDEO PLAYS → OPTIONS AUTO-REVEAL.")
if st.session_state.user_name:
    st.caption(f"IDENTITY CONFIRMED: **{st.session_state.user_name.upper()}**")


# Progress + Score (Reactor Core Style)
progress = (st.session_state.q_index) / TOTAL
st.progress(progress)
st.markdown(
    f"<div class='glass' style='margin:10px 0; display:flex; justify-content:space-between; font-family: Orbitron;'>"
    f"<div>QUERY <b>{st.session_state.q_index+1}</b> / {TOTAL}</div>"
    f"<div>COGNITIVE SCORE: <b>{st.session_state.score}</b></div>"
    f"</div>",
    unsafe_allow_html=True
)

# # One-time intro
# if st.session_state.play_intro:
#     autoplay_audio("audio/intro.mp3", loop=False)
#     st.session_state.play_intro = False

# One-time intro — deferred to avoid double rerun
if st.session_state.get("deferred_play_intro", False):
    # Wait until UI is stable, then play
    autoplay_audio("audio/intro.mp3", loop=False)
    st.session_state.deferred_play_intro = False
    st.session_state.play_intro = False  # Keep old flag clean

# Current Question
q = QUIZ[st.session_state.q_index]

with st.container():
   # st.markdown("<div class='glass'>", unsafe_allow_html=True)

    # Video Display with Avatar Attribution
    if st.session_state.stage == "prompt":
        st.subheader("PROMPT RECEIVED")
        autoplay_video(q["videos"]["prompt"], muted=False)
        st.markdown("<div style='text-align: right; font-size: 0.8rem; color: #00cccc; margin-top: -10px;'>— Shaid’s AI Avatar</div>", unsafe_allow_html=True)
    else:
        correct = (st.session_state.selected == q["answer"])
        clip = q["videos"]["correct"] if correct else q["videos"]["wrong"]
        autoplay_video(clip, muted=False)
        st.markdown("<div style='text-align: right; font-size: 0.8rem; color: #00cccc; margin-top: -10px;'>— Shaid’s AI Avatar</div>", unsafe_allow_html=True)
        if correct:
            st.success("AFFIRMATIVE. RESPONSE VALIDATED ✅")
        else:
            st.error("NEGATIVE. RECALIBRATE INPUT ❌")

    # Robotic Option Cards (Replaces Radio Buttons)
    st.markdown(f"### {q['question_text']}", unsafe_allow_html=True)
    
    for i, option in enumerate(q["options"]):
        key = f"option_{i}_{q['id']}"
        is_selected = (st.session_state.selected == option)
        is_feedback = (st.session_state.stage == "feedback")
        classes = "option-card"
        if is_selected:
            classes += " selected"
        if is_feedback:
            if option == q["answer"]:
                classes += " correct"
            elif option == st.session_state.selected:
                classes += " incorrect"

        # Disable interaction during feedback
        if is_feedback:
            st.markdown(f"<div class='{classes}'>{option}</div>", unsafe_allow_html=True)
        else:
            if st.button(option, key=key, use_container_width=True):
                st.session_state.selected = option
                if st.session_state.stage == "prompt":
                    if option == q["answer"]:
                        st.session_state.score += 1
                    st.session_state.stage = "feedback"
                    st.rerun()

    # Navigation
    c1, c2 = st.columns(2)
    with c1:
        st.button("REPLAY CLIP", on_click=lambda: None, use_container_width=True)

    with c2:
        def next_question():
            if st.session_state.q_index < TOTAL - 1:
                st.session_state.q_index += 1
                reset_for_next()
            else:
                st.session_state.stage = "finished"

        st.button(
            "NEXT QUERY",
            disabled=(st.session_state.stage != "feedback"),
            on_click=next_question,
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# Finish Screen
if st.session_state.get("stage") == "finished":
    #st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.header("COGNITIVE ASSESSMENT COMPLETE")
    st.markdown("""
    <div style='text-align: center; font-family: Orbitron; margin: 20px 0;'>
        <div style='font-size: 1.1rem; color: #ff55ff; text-shadow: 0 0 8px #ff55ff;'>
            SESSION TERMINATED BY <strong>SHAID’S AI AVATAR</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write(f"FINAL SCORE: **{st.session_state.score} / {TOTAL}**")
    if st.session_state.score == TOTAL:
        st.balloons()
        st.success("OPTIMAL PERFORMANCE. UNIT DESIGNATION: GENIUS-CLASS")
    elif st.session_state.score > TOTAL / 2:
        st.info("ADEQUATE PERFORMANCE. RECOMMEND REVISION MODULE.")
    else:
        st.warning("SUBOPTIMAL OUTPUT. INITIATE RETRAINING SEQUENCE.")
    
    if st.button("REBOOT SYSTEM", use_container_width=True):
        st.session_state.q_index = 0
        st.session_state.score = 0
        reset_for_next()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# # Tips Footer
# with st.expander("SYSTEM NOTES"):
#     st.write("""
# - AUDIO/VIDEO SUBSYSTEMS REQUIRE INITIAL USER INTERACTION (CLICK 'ACTIVATE MODULE').
# - VIDEOS MUST BE MP4/WEBM. LOCAL FILES EMBEDDED VIA BASE64.
# - OPTION CARDS SIMULATE ROBOTIC TOUCH PANELS — HOVER FOR FEEDBACK.
# - HOSTED & MODERATED BY **SHAID’S AI AVATAR** — YOUR CYBERNETIC ASSESSMENT PARTNER.
# - FOR CUSTOM SOUNDS/EFFECTS, EXTEND `autoplay_audio` WITH ADDITIONAL TRIGGERS.
# - SCANLINES AND GLITCH EFFECTS ARE PURE CSS — NO PERFORMANCE IMPACT.
# """)

    # Footer
st.markdown("""
<div class="footer">
    <p><center>\n🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
</div>
""", unsafe_allow_html=True)