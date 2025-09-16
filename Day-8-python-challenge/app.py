import streamlit as st
import time
import streamlit.components.v1 as components
from PIL import Image
import random
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
        <center> Day 8 - Currency Converter</center>
    </h2>
    """,
    unsafe_allow_html=True
)

# --- CONFIG ---
st.set_page_config(
    page_title="🪙 NEON NEXUS — Currency Converter Challenge",
    page_icon="💱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



# --- SESSION STATE ---
if "conversion_done" not in st.session_state:
    st.session_state.conversion_done = False
    st.session_state.result_msg = ""
    st.session_state.full_result_msg = ""
    st.session_state.coins_falling = False
    st.session_state.teller_message = "👋 Welcome, Trader. Select currencies and amount."
    st.session_state.last_typed_message = None
    st.session_state.ready_to_rerun = False  # 👈 ADD THIS

# --- STATIC RATES ---
RATES = {
    "INR": {"USD": 1/83.5, "EUR": 1/90.2},
    "USD": {"INR": 83.5, "EUR": 0.925},
    "EUR": {"INR": 90.2, "USD": 1.08}
}

# --- TYPEWRITER EFFECT ---
def typewriter_effect(container, text, delay=0.03):
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f'<div class="speech-bubble">💬 {displayed_text}▌</div>', unsafe_allow_html=True)
        time.sleep(delay)
    container.markdown(f'<div class="speech-bubble">💬 {displayed_text}</div>', unsafe_allow_html=True)
    st.session_state.last_typed_message = text  # ✅ Remember what we just typed

# --- SPEAK HELPER — RANDOM VOICE ---
def speak_text(text, target_amount=None, target_currency=None):
    if target_amount is not None and target_currency is not None:
        whole_number = int(round(target_amount))

        phrases = [
            f"Alright, you’ve got about {whole_number} {target_currency} now. Nice move, Trader.",
            f"Just turned your money into {whole_number} {target_currency}. Ready to spend or save?",
            f"Neon transfer complete — you now hold {whole_number} {target_currency}. The market smiles on you.",
            f"Transaction confirmed. {whole_number} {target_currency} are now yours. What’s next, Trader?",
            f"Consider it done. You’re walking away with {whole_number} {target_currency}. Smooth as liquid light.",
            f"Currency swapped. You’re holding {whole_number} {target_currency}. The Nexus approves.",
            f"Easy. {whole_number} {target_currency} — transferred, secured, and glowing in your account.",
            f"Done and dusted. {whole_number} {target_currency} are now at your command. Go make waves."
        ]
        speak_phrase = random.choice(phrases)
    else:
        speak_phrase = text

    safe_phrase = speak_phrase.replace("'", "\\'").replace('"', '\\"')

    voice_list = [
        # "Microsoft Zira Desktop - English (United States)",
        # "Alex",
        # "Google US English",
        "Google UK English Female",
        # "Microsoft Hazel Desktop - English (Great Britain)"
    ]

    selected_voice_name = random.choice(voice_list)

    js_code = f"""
    <script>
    function speakWithNaturalVoice() {{
        const utterance = new SpeechSynthesisUtterance("{safe_phrase}");
        utterance.rate = 0.88;
        utterance.pitch = 1.05;

        let voices = speechSynthesis.getVoices();
        let selectedVoice = null;
        selectedVoice = voices.find(v => v.name === "{selected_voice_name}");

        if (!selectedVoice) {{
            selectedVoice = voices.find(v => v.lang.includes('en')) || null;
        }}

        utterance.voice = selectedVoice;
        speechSynthesis.speak(utterance);
    }}

    if (speechSynthesis.getVoices().length === 0) {{
        speechSynthesis.addEventListener('voiceschanged', speakWithNaturalVoice);
    }} else {{
        speakWithNaturalVoice();
    }}
    </script>
    """
    components.html(js_code, height=0, width=0)

# --- HEADER ---
st.markdown('<div class="neon-header">⚡ NEON NEXUS EXCHANGER ⚡</div>', unsafe_allow_html=True)


# --- TELLER AI — TYPE ONLY IF MESSAGE CHANGED ---      
col1, col2 = st.columns([5.5,3])
with col1:
    try:
        teller_img = Image.open("images/teller_hologram.png")
        st.image(teller_img, width=3000)
    except:
        st.image("https://via.placeholder.com/120x200/0f0f23/00f7ff?text=AI+TELLER", width=2000)

with col2:
    teller_container = st.empty()

    # ✅ ONLY TYPE IF MESSAGE IS NEW OR CHANGED
    if (st.session_state.teller_message != st.session_state.last_typed_message):
        typewriter_effect(teller_container, st.session_state.teller_message)

st.markdown("<br>", unsafe_allow_html=True)

# --- INPUT PANEL ---
col_from, col_to = st.columns(2)

with col_from:
    currency_from = st.selectbox(
        "💱 FROM",
        ["INR", "USD", "EUR"],
        index=0,
        key="from_curr"
    )

available_to = [c for c in ["INR", "USD", "EUR"] if c != currency_from]

with col_to:
    currency_to = st.selectbox(
        "💱 TO",
        available_to,
        index=0,
        key="to_curr"
    )

amount = st.text_input(
    "💰 Enter Amount",
    placeholder="e.g., 1000",
    label_visibility="collapsed"
)

# ➤ 1:1 Rate
if currency_from != currency_to:
    rate = RATES[currency_from][currency_to]
    st.session_state.result_msg = f"1 {currency_from} = {rate:.4f} {currency_to}"
else:
    st.session_state.result_msg = f"1 {currency_from} = 1 {currency_to}"

#st.info(f"💱 **Live Rate**: {st.session_state.result_msg}")

# --- EXCHANGER CACHE BAR ---
st.markdown('<div class="exchanger-label">⚡ EXCHANGER CACHE</div>', unsafe_allow_html=True)
cache_bar = st.progress(0)
coin_zone = st.empty()

if st.session_state.coins_falling:
    coin_zone.markdown('<div class="coin-zone">🪙 COINS FALLING — HOLD FOR SYNC...</div>', unsafe_allow_html=True)
else:
    if st.session_state.conversion_done:
        coin_zone.markdown(f'<div class="coin-zone success">✅ {st.session_state.full_result_msg}</div>', unsafe_allow_html=True)
    else:
        coin_zone.markdown('<div class="coin-zone">🪙 DROP ZONE — AWAITING COINS</div>', unsafe_allow_html=True)

# --- CONVERT BUTTON ---
if st.button("💱 EXCHANGE NOW", key="convert_btn", use_container_width=True):
    try:
        amt = float(amount)
        if amt <= 0:
            raise ValueError
    except:
        error_msg = "⚠️ Invalid amount. Reboot transaction?"
        st.session_state.teller_message = error_msg
        speak_text("Invalid input. Reboot transaction?")
        st.rerun()

    rate = RATES[currency_from][currency_to] if currency_from != currency_to else 1.0
    result = amt * rate
    st.session_state.full_result_msg = f"{amt} {currency_from} → {result:.2f} {currency_to}"

    # ➤ ONLY set processing message + start animation
    st.session_state.teller_message = "⚡ Processing... Syncing cache."
    st.session_state.coins_falling = True
    speak_text("Processing transaction. Syncing cache.")
    st.rerun()

# --- ANIMATE + SET FINAL MESSAGE ---
# --- ANIMATE + SET FINAL MESSAGE ---
if st.session_state.coins_falling:
    # Animate progress bar
    for i in range(0, 101, 10):
        cache_bar.progress(i)
        time.sleep(0.1)

    # Finalize progress
    cache_bar.progress(100)
    st.session_state.coins_falling = False
    st.session_state.conversion_done = True

    # ➤ Set final Teller message
    full_message = f"✅ {st.session_state.full_result_msg}. Cache sync complete."
    st.session_state.teller_message = full_message

    # ➤ Speak the friendly summary (whole number)
    result_parts = st.session_state.full_result_msg.split(" → ")
    if len(result_parts) == 2:
        target_str = result_parts[1]
        try:
            num_part, curr_part = target_str.split(" ", 1)
            target_amount = float(num_part)
            target_currency = curr_part.strip()
            speak_text("", target_amount=target_amount, target_currency=target_currency)
        except Exception as e:
            st.warning(f"Voice error: {e}")
            speak_text("Conversion complete.")
    else:
        speak_text("Conversion complete.")

    # ➤ ✅ Let UI settle, then trigger re-render to type final message
    time.sleep(0.2)
    st.rerun()

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)

    # Footer
st.markdown("""
<div class="footer">
    <p><center>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</center>
   
</div>
""", unsafe_allow_html=True)
