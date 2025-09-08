import streamlit as st

# Page configuration
st.set_page_config(page_title="Python Challenge Day 1", page_icon="🦅", layout="centered")

# Initialize dark mode state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ----- Sidebar settings (optional second control) -----
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="sidebar_toggle"):
        st.session_state.dark_mode = True
    else:
        st.session_state.dark_mode = False

# ----- Theme CSS -----
def get_css(is_dark: bool) -> str:
    if is_dark:
        return """
        <style>
          .stApp{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);color:#fff;}
          .main-header{text-align:center;color:#64ffda;font-size:3rem;font-weight:800;margin:0.75rem 0 1rem;text-shadow:2px 2px 4px rgba(0,0,0,.3);}
          .subtitle{text-align:center;color:#b0bec5;font-size:1.05rem;margin-bottom:1.25rem;font-style:italic;}
          .toolbar{display:flex;justify-content:flex-end;gap:.5rem;margin:.25rem 0 1rem;}
          .toolbar .stButton>button{background:#0ea5e9;color:#fff;border:1px solid #0ea5e9;border-radius:999px;padding:.45rem .9rem;font-weight:700;}
          .toolbar .stButton>button:hover{filter:brightness(1.05);}
          .form-container{background:linear-gradient(135deg,#2d3748 0%,#4a5568 100%);padding:1.5rem;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.35);border:1px solid #4a5568;}
          .form-container h3{color:#64ffda!important;text-align:center;margin-top:.25rem;}
          .form-container p{color:#e2e8f0!important;font-weight:600;margin-bottom:.5rem;}
          .stTextInput input{background:#111827!important;color:#e5e7eb!important;border:1px solid #374151!important;border-radius:10px!important;}
          .stSlider>div[data-baseweb="slider"] div{color:#e5e7eb!important;}
          .stButton button{background:#0ea5e9;color:#fff;border-radius:10px;border:1px solid #0ea5e9;}
          .greeting-card{background:linear-gradient(45deg,#667eea,#764ba2);padding:1.5rem;border-radius:14px;text-align:center;color:#fff;font-size:1.15rem;font-weight:700;margin-top:1.25rem;box-shadow:0 8px 24px rgba(102,126,234,.28);}
          .fun-facts{background:#2d3748;padding:1rem 1.25rem;border-radius:10px;border-left:5px solid #64ffda;margin-top:.9rem;color:#e2e8f0;box-shadow:0 4px 14px rgba(0,0,0,.28);border:1px solid #4a5568;}
          .fun-facts h4{color:#64ffda!important;margin-bottom:.6rem;}
          .fun-facts li{color:#cbd5e0!important;margin-bottom:.4rem;line-height:1.55;}
          .footer{text-align:center;color:#93a3af;font-size:.9rem;}
        </style>
        """
    else:
        return """
        <style>
          .stApp{background:linear-gradient(135deg,#eef2f7 0%,#ccd6e3 100%);color:#111827;}
          .main-header{text-align:center;color:#0f766e;font-size:3rem;font-weight:800;margin:.75rem 0 1rem;text-shadow:1px 1px 2px rgba(0,0,0,.06);}
          .subtitle{text-align:center;color:#374151;font-size:1.05rem;margin-bottom:1.25rem;font-style:italic;}
          .toolbar{display:flex;justify-content:flex-end;gap:.5rem;margin:.25rem 0 1rem;}
          .toolbar .stButton>button{background:#111827;color:#fff;border:1px solid #111827;border-radius:999px;padding:.45rem .9rem;font-weight:700;}
          .toolbar .stButton>button:hover{filter:brightness(1.05);}
          .form-container{background:#ffffff;padding:1.5rem;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.08);border:1px solid #e5e7eb;}
          .form-container h3{color:#111827!important;text-align:center;margin-top:.25rem;}
          .form-container p{color:#1f2937!important;font-weight:600;margin-bottom:.5rem;}
          .stTextInput input{background:#f9fafb!important;color:#111827!important;border:1px solid #d1d5db!important;border-radius:10px!important;}
          .stTextInput label,.stSlider label{color:#111827!important;}
          .stSlider>div[data-baseweb="slider"] div{color:#111827!important;}
          .stButton button{background:#111827;color:#fff;border-radius:10px;border:1px solid #111827;}
          .greeting-card{background:linear-gradient(45deg,#10b981,#22c55e);padding:1.5rem;border-radius:14px;text-align:center;color:#fff;font-size:1.15rem;font-weight:700;margin-top:1.25rem;box-shadow:0 8px 24px rgba(16,185,129,.22);}
          .fun-facts{background:#ffffff;padding:1rem 1.25rem;border-radius:10px;border-left:5px solid #0ea5e9;margin-top:.9rem;color:#111827;box-shadow:0 4px 14px rgba(0,0,0,.06);border:1px solid #e5e7eb;}
          .fun-facts h4{color:#0ea5e9!important;margin-bottom:.6rem;}
          .fun-facts li{color:#1f2937!important;margin-bottom:.4rem;line-height:1.55;}
          .footer{text-align:center;color:#4b5563;font-size:.9rem;}
        </style>
        """

st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ----- Header + top toolbar with toggle button -----
st.markdown('<h1 class="main-header">Social Eagle 🦅 Python Challenge Day 1 </h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Welcome to your first Python challenge! Let\'s get to know you better.</p>', unsafe_allow_html=True)

# Toolbar row (right-aligned) with eagle emoji toggle button
toolbar_col = st.container()
with toolbar_col:
    st.markdown('<div class="toolbar">', unsafe_allow_html=True)
    # Use 🦅 plus sun/moon
    label = "🦅☀️ Light Mode" if st.session_state.dark_mode else "🦅🌙 Dark Mode"
    if st.button(label, key="header_theme_btn"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Form -----
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    #st.markdown('<div class="form-container">', unsafe_allow_html=True)
    with st.form("greeting_form", clear_on_submit=False):
        st.markdown('<h3>👋 Tell us about yourself</h3>', unsafe_allow_html=True)
        raw_name = st.text_input(
            "🏷️ What's your name?",
            placeholder="Enter your awesome name here...",
            help="Don't worry, we won't spam you! 😄",
            label_visibility="visible",
        )
        name = raw_name.strip()
        st.markdown('<p>🎂 How old are you?</p>', unsafe_allow_html=True)
        age = st.slider("", 1, 100, 25, help="Slide to select your age", label_visibility="collapsed")
        submitted = st.form_submit_button("✨ Generate My Greeting ✨", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ----- Response -----
if submitted and name:
    if age < 13:
        age_message, emoji = "You're so young and full of potential! 🌟", "🧒"
    elif age < 20:
        age_message, emoji = "Teenage years - the perfect time to learn coding! 💪", "🧑‍💻"
    elif age < 30:
        age_message, emoji = "Great age to master new skills! 🎯", "👨‍💼"
    elif age < 60:
        age_message, emoji = "Wisdom and experience - a powerful combination! 🧠", "👨‍🏫"
    else:
        age_message, emoji = "Age is just a number - keep learning! 🏆", "👴"

    st.markdown(
        f"""
        <div class="greeting-card">
            <h2>🎉 Hello {name}! {emoji}</h2>
            <p>You are {age} years old.</p>
            <p>{age_message}</p>
            <p>Welcome to the Python Challenge! 🦅✨</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="fun-facts">
            <h4>🎈 Fun Facts About You:</h4>
            <ul>
                <li>🎂 You've lived for approximately <strong>{age * 365:,}</strong> days!</li>
                <li>⏰ That's about <strong>{age * 365 * 24:,}</strong> hours of life experience!</li>
                <li>🌟 Your name <strong>"{name}"</strong> has <strong>{len(name)}</strong> letters</li>
                <li>🚀 You're ready to tackle Python challenges!</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.balloons()
elif submitted and not name:
    st.error("🤔 Oops! Please enter your name so we can create a personalized greeting for you!")

# ----- Footer -----
st.markdown("---")
st.markdown(
    '<p class="footer">🎓 Keep coding, keep learning! Made with ❤️ by Shaid using Streamlit '
    f'{"🌙" if st.session_state.dark_mode else "☀️"}'
    "</p>",
    unsafe_allow_html=True,
)