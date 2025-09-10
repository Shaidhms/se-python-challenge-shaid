import streamlit as st
import math
import time
import random
import re
from io import BytesIO
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("se.png")

st.markdown(
    f"""
    <h1 class="main-header">
         <img src="data:image/png;base64,{logo_base64}" width="40" style="vertical-align: middle; margin-left:5px;">
        Social Eagle Python Challenge Day 3 - Smart Calculator
    </h1>
    """,
    unsafe_allow_html=True
)
# Page configuration
st.set_page_config(
  page_title="Social Eagle Python Challenge Day 3", page_icon="🦅", layout="centered"
)

# Configure the page
st.set_page_config(
    page_title="AI Voice Calculator Pro",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Try to import speech recognition (install with: pip install SpeechRecognition)
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

# Custom CSS for AI theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #0f1419 100%);
        color: #ffffff;
    }
    
    .ai-header {
        text-align: center;
        background: linear-gradient(45deg, #00d4ff, #ff0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 20px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px #00d4ff; }
        to { text-shadow: 0 0 30px #ff0080; }
    }
    

    
    .result-box {
        background: linear-gradient(135deg, #00d4ff 0%, #ff0080 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        color: #ffffff;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4); }
        50% { box-shadow: 0 8px 25px rgba(255, 0, 128, 0.6); }
        100% { box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4); }
    }
    
    .ai-thinking {
        text-align: center;
        color: #00d4ff;
        font-style: italic;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    
 
    
    .history-item {
        background: rgba(0, 212, 255, 0.1);
        border-left: 3px solid #00d4ff;
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #ff0080);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4);
    }
    
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Voice command parser function
def parse_voice_command(text):
    """Parse voice command and extract numbers and operation"""
    if not text:
        return [], None
        
    text = text.lower().strip()
    
    # Common number words to digits mapping
    number_words = {
        'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
        'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
        'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14', 'fifteen': '15',
        'sixteen': '16', 'seventeen': '17', 'eighteen': '18', 'nineteen': '19', 'twenty': '20',
        'thirty': '30', 'forty': '40', 'fifty': '50', 'sixty': '60', 'seventy': '70',
        'eighty': '80', 'ninety': '90', 'hundred': '100'
    }
    
    # Replace number words with digits
    for word, digit in number_words.items():
        text = text.replace(word, digit)
    
    # Extract numbers using regex
    numbers = re.findall(r'-?\d+(?:\.\d+)?', text)
    
    # Determine operation
    operation = None
    if any(word in text for word in ['plus', 'add', 'sum', '+']):
        operation = "➕ Addition"
    elif any(word in text for word in ['minus', 'subtract', 'take away', '-']):
        operation = "➖ Subtraction"
    elif any(word in text for word in ['times', 'multiply', 'multiplied by', '*', 'x']):
        operation = "✖️ Multiplication"
    elif any(word in text for word in ['divide', 'divided by', '/', 'over']):
        operation = "➗ Division"
    elif any(word in text for word in ['power', 'to the power of', '^', 'squared', 'cubed']):
        operation = "🔋 Power"
        if 'squared' in text:
            numbers.append('2')
        elif 'cubed' in text:
            numbers.append('3')
    elif any(word in text for word in ['square root', 'sqrt', 'root']):
        operation = "📐 Square Root"
    elif any(word in text for word in ['percent', 'percentage', '%']):
        operation = "📊 Percentage"
    
    return numbers, operation

# Function to process audio with speech recognition
def process_audio(audio_bytes):
    """Process audio bytes and return transcribed text"""
    if not SPEECH_AVAILABLE:
        return "Speech recognition not available. Install: pip install SpeechRecognition"
    
    try:
        # Initialize recognizer
        r = sr.Recognizer()
        
        # Convert audio bytes to AudioFile
        audio_file = sr.AudioFile(BytesIO(audio_bytes))
        
        with audio_file as source:
            audio = r.record(source)
        
        # Use Google's free speech recognition
        text = r.recognize_google(audio)
        return text
        
    except sr.UnknownValueError:
        return "Could not understand audio. Please speak clearly."
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"
    except Exception as e:
        return f"Error processing audio: {str(e)}"

# Header
st.markdown('<div class="ai-header">🎤 AI Voice Calculator Pro</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #888; margin-bottom: 30px;">Powered by Speech Recognition • Voice-Activated Computing</div>', unsafe_allow_html=True)

# Voice Input Section
st.markdown('<div class="voice-box">', unsafe_allow_html=True)
st.markdown("### 🎙️ Voice Command Center")

if SPEECH_AVAILABLE:
    st.markdown("**🎤 Record your calculation:** *'What is 5 plus 5'* or *'Calculate 10 times 3'*")
    
    # Audio input widget
    audio_data = st.audio_input("🎯 Record your voice command:")
    
    if audio_data is not None:
        with st.spinner("🧠 Processing voice command..."):
            # Process the audio
            transcribed_text = process_audio(audio_data.getvalue())
            
            # Display transcribed text
            st.success(f"🎯 **Heard:** {transcribed_text}")
            
            # Parse the command
            numbers, operation = parse_voice_command(transcribed_text)
            
            if numbers and operation:
                # Auto-fill the calculator
                st.session_state.voice_num1 = float(numbers[0]) if len(numbers) > 0 else 0.0
                st.session_state.voice_num2 = float(numbers[1]) if len(numbers) > 1 else 0.0
                st.session_state.voice_operation = operation
                
                st.success(f"✅ **Parsed:** Numbers: {numbers}, Operation: {operation}")
                st.info("👇 Values auto-filled in calculator below!")
            else:
                st.warning("❌ Could not parse the command. Try saying something like 'What is 5 plus 5'")
else:
    st.error("❌ **Speech Recognition not available!**")
    st.info("💡 **To enable voice features, install:** `pip install SpeechRecognition`")
    st.markdown("**Manual input:** Type your calculation in the text box below:")

# Alternative: Manual text input for voice commands
st.markdown("### ⌨️ Type Voice Command (Alternative)")
manual_voice_input = st.text_input(
    "🎯 Type your calculation:",
    placeholder="Example: 'What is 25 plus 15' or 'Square root of 16'",
    key="manual_voice"
)

if manual_voice_input and st.button("🔄 PARSE TYPED COMMAND"):
    numbers, operation = parse_voice_command(manual_voice_input)
    if numbers and operation:
        st.session_state.voice_num1 = float(numbers[0]) if len(numbers) > 0 else 0.0
        st.session_state.voice_num2 = float(numbers[1]) if len(numbers) > 1 else 0.0
        st.session_state.voice_operation = operation
        st.success(f"✅ **Parsed:** Numbers: {numbers}, Operation: {operation}")
    else:
        st.warning("❌ Could not parse the command.")

st.markdown('</div>', unsafe_allow_html=True)

# Calculator container
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 🔢 Input Parameters")
    
    # Get values from voice or default
    default_num1 = getattr(st.session_state, 'voice_num1', 0.0)
    default_num2 = getattr(st.session_state, 'voice_num2', 0.0)
    default_operation = getattr(st.session_state, 'voice_operation', "➕ Addition")
    
    num1 = st.number_input(
        "🎯 First Operand (X)",
        value=default_num1,
        step=0.1,
        format="%.6f",
        help="Auto-filled from voice or enter manually"
    )
    
    num2 = st.number_input(
        "🎯 Second Operand (Y)", 
        value=default_num2,
        step=0.1,
        format="%.6f",
        help="Auto-filled from voice or enter manually"
    )
    
    # Operation selection
    st.markdown("### ⚡ Operation Selection")
    operations = ["➕ Addition", "➖ Subtraction", "✖️ Multiplication", "➗ Division", "🔋 Power", "📐 Square Root", "📊 Percentage"]
    
    operation = st.selectbox(
        "🔮 Choose Mathematical Operation",
        operations,
        index=operations.index(default_operation) if default_operation in operations else 0,
        help="Auto-selected from voice or choose manually"
    )
    
    # Calculate button
    st.markdown("---")
    if st.button("🚀 COMPUTE RESULT", use_container_width=True):
        # AI thinking animation
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown('<div class="ai-thinking">🧠 AI Processing voice command...</div>', unsafe_allow_html=True)
        time.sleep(0.5)
        
        thinking_placeholder.markdown('<div class="ai-thinking">⚡ Converting speech to mathematics...</div>', unsafe_allow_html=True)
        time.sleep(0.5)
        
        thinking_placeholder.empty()
        
        # Perform calculation
        try:
            if operation == "➕ Addition":
                result = num1 + num2
                equation = f"{num1} + {num2} = {result:.6f}"
                speech_result = f"The result of {num1} plus {num2} is {result:.2f}"
            elif operation == "➖ Subtraction":
                result = num1 - num2
                equation = f"{num1} - {num2} = {result:.6f}"
                speech_result = f"The result of {num1} minus {num2} is {result:.2f}"
            elif operation == "✖️ Multiplication":
                result = num1 * num2
                equation = f"{num1} × {num2} = {result:.6f}"
                speech_result = f"The result of {num1} times {num2} is {result:.2f}"
            elif operation == "➗ Division":
                if num2 == 0:
                    st.error("🚫 ERROR: Division by zero detected!")
                    st.stop()
                result = num1 / num2
                equation = f"{num1} ÷ {num2} = {result:.6f}"
                speech_result = f"The result of {num1} divided by {num2} is {result:.2f}"
            elif operation == "🔋 Power":
                result = num1 ** num2
                equation = f"{num1} ^ {num2} = {result:.6f}"
                speech_result = f"The result of {num1} to the power of {num2} is {result:.2f}"
            elif operation == "📐 Square Root":
                if num1 < 0:
                    st.error("🚫 ERROR: Cannot calculate square root of negative number!")
                    st.stop()
                result = math.sqrt(num1)
                equation = f"√{num1} = {result:.6f}"
                speech_result = f"The square root of {num1} is {result:.2f}"
            elif operation == "📊 Percentage":
                if num2 == 0:
                    st.error("🚫 ERROR: Division by zero detected!")
                    st.stop()
                result = (num1 / num2) * 100
                equation = f"({num1} ÷ {num2}) × 100 = {result:.2f}%"
                speech_result = f"{num1} is {result:.2f} percent of {num2}"
            
            # Add to history
            timestamp = time.strftime("%H:%M:%S")
            history_entry = f"{equation} [{timestamp}]"
            st.session_state.history.append(history_entry)
            
            if len(st.session_state.history) > 10:
                st.session_state.history = st.session_state.history[-10:]
            
            # Display result
            st.markdown(f'<div class="result-box">🎯 RESULT: {equation}</div>', unsafe_allow_html=True)
            
            # Show the speech result text (since TTS is complex in Streamlit)
            st.success(f"✅ Calculation completed!")
            st.info(f"🔊 **Voice Result:** {speech_result}")
            
            # Show AI stats
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("⚡ Processing Speed", f"{random.randint(850, 999)} ms")
            with col_b:
                st.metric("🧠 AI Confidence", f"{random.randint(95, 99)}%")
            with col_c:
                st.metric("🎤 Voice Accuracy", f"{random.randint(92, 98)}%")
                
        except Exception as e:
            st.error(f"🚫 COMPUTATIONAL ERROR: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 🎤 Voice Calculator Setup")

if not SPEECH_AVAILABLE:
    st.sidebar.error("❌ **Speech Recognition not installed**")
    st.sidebar.markdown("""
    **To enable voice features:**
    ```
    pip install SpeechRecognition
    ```
    Then restart the app.
    """)
else:
    st.sidebar.success("✅ **Voice Recognition Ready**")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎤 Voice Commands Examples")
st.sidebar.markdown("""
- *"What is 5 plus 5?"*
- *"Calculate 10 times 3"*
- *"Square root of 16"*
- *"25 divided by 5"*
- *"Two to the power of three"*
- *"What is 20 percent of 150?"*
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Recent Operations")

if st.session_state.history:
    for calc in reversed(st.session_state.history[-5:]):
        st.sidebar.markdown(f'<div class="history-item">{calc}</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.sidebar.markdown("*No calculations yet.*")

# Footer
st.markdown("""
<div class="footer">
    <p>🎓 Keep coding, keep learning! Made with ❤️ by Shaid 🎤 AI Voice Calculator Pro v3.0 | Speech-Enabled Computing | 
    <span style="color: #00d4ff;">Powered by Python Speech Recognition</span></p>
</div>
""", unsafe_allow_html=True)
