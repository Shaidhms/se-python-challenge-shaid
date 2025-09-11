import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
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
        Social Eagle Python Challenge Day 4 - BMI Health Calculator
    </h1>
    """,
    unsafe_allow_html=True
)
# Configure page
st.set_page_config(
    page_title="BMI Health Motivator",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling with health-focused theme
st.markdown("""
<style>
    .main {
        padding: 1rem;
        max-height: 100vh;
        overflow-y: auto;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .language-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .bmi-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .bmi-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .input-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        color: white;
        height: 100%;
    }
    
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    
    .tips-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    
    .motivation-card {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        margin-top: 2rem;
        text-align: center;
        color: white;
    }
    
    .bmi-value {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .category-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        margin: 0.5rem 0;
        width: 100%;
        text-align: center;
    }
    
    .underweight {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
    }
    
    .normal {
        background: linear-gradient(135deg, #00b894, #00a085);
        color: white;
    }
    
    .overweight {
        background: linear-gradient(135deg, #fdcb6e, #e17055);
        color: white;
    }
    
    .tip-item {
        background: #f8f9fa;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        border-left: 4px solid #28a745;
        color: #2c3e50;
        font-weight: 500;
    }
    
    .section-header {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .section-header-white {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .motivation-element {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .motivation-quote {
        font-size: 1.1rem;
        font-weight: bold;
        color: white;
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        margin: 1rem 0;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .tips-main-text {
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
        color: #2c3e50;
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #28a745;
    }
    
    .video-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def calculate_bmi(weight, height_cm):
    """Calculate BMI from weight (kg) and height (cm)"""
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Get BMI category and corresponding color"""
    if bmi < 18.5:
        return "Underweight", "underweight", "#74b9ff"
    elif 18.5 <= bmi < 25:
        return "Normal", "normal", "#00b894"
    else:
        return "Overweight", "overweight", "#e17055"

def get_translations(language):
    """Get all text translations based on language"""
    translations = {
        "english": {
            "title": "💪 BMI Health Motivator",
            "subtitle": "Calculate your BMI and get motivated to achieve your health goals! 🎯",
            "your_details": "📊 Your Details",
            "height": "Height (cm)",
            "weight": "Weight (kg)",
            "calculate": "🔍 Calculate",
            "your_bmi": "📈 Your BMI",
            "bmi_formula": "BMI Formula:",
            "bmi_scale": "📊 BMI Scale",
            "action_plan": "Action Plan",
            "bmi_categories": "📚 BMI Categories",
            "categories": ['Underweight', 'Normal', 'Overweight'],
            "bmi_range": "BMI Range",
            "motivation_hub": "Health Motivation Hub",
            "transform_text": "Transform your {category} status into optimal health! 💪",
            "daily_motivation": "💬 Daily Motivation",
            "health_goals": "🎯 Your Health Goals",
            "motivation_video": "🎥 Get Motivated!",
            "get_new_motivation": "🚀 Get New Motivation!",
            "health_journey": "🌟 Your Health Journey Starts Today! 🌟",
            "bmi_status": "BMI: {bmi} | Status: {category} | Goal: Optimal Health!",
            "disclaimer": "⚠️ Consult healthcare professionals for personalized medical advice and supervision.",
            "footer_message": "💪 Remember: Every healthy choice you make today builds a stronger tomorrow!"
        },
        "tamil": {
            "title": "💪 BMI உடல்நல ஊக்குவிப்பு",
            "subtitle": "உங்கள் BMI கணக்கிட்டு உடல்நல இலக்குகளை அடைய உத்வேகம் பெறுங்கள்! 🎯",
            "your_details": "📊 உங்கள் விவரங்கள்",
            "height": "உயரம் (செ.மீ)",
            "weight": "எடை (கி.கி)",
            "calculate": "🔍 கணக்கிடுங்கள்",
            "your_bmi": "📈 உங்கள் BMI",
            "bmi_formula": "BMI சூத்திரம்:",
            "bmi_scale": "📊 BMI அளவுகோல்",
            "action_plan": "செயல் திட்டம்",
            "bmi_categories": "📚 BMI வகைகள்",
            "categories": ['குறைந்த எடை', 'சாதாரண', 'அதிக எடை'],
            "bmi_range": "BMI வரம்பு",
            "motivation_hub": "உடல்நல ஊக்க மையம்",
            "transform_text": "உங்கள் {category} நிலையை சிறந்த ஆரோக்கியமாக மாற்றுங்கள்! 💪",
            "daily_motivation": "💬 தினசரி உத்வேகம்",
            "health_goals": "🎯 உங்கள் ஆரோக்கிய இலக்குகள்",
            "motivation_video": "🎥 உத்வேகம் பெறுங்கள்!",
            "get_new_motivation": "🚀 புதிய உத்வேகம் பெறுங்கள்!",
            "health_journey": "🌟 உங்கள் ஆரோக்கிய பயணம் இன்றே தொடங்குகிறது! 🌟",
            "bmi_status": "BMI: {bmi} | நிலை: {category} | இலக்கு: சிறந்த ஆரோக்கியம்!",
            "disclaimer": "⚠️ தனிப்பட்ட மருத்துவ ஆலோசனை மற்றும் மேற்பார்வைக்காக மருத்துவ நிபுணர்களை அணுகவும்.",
            "footer_message": "💪 நினைவில் கொள்ளுங்கள்: இன்று நீங்கள் எடுக்கும் ஒவ்வொரு ஆரோக்கியமான தேர்வும் வலிமையான நாளைய உங்களை உருவாக்குகிறது!"
        }
    }
    return translations.get(language, translations["english"])

def get_health_suggestions(category, language):
    """Get health suggestions based on BMI category and language"""
    suggestions = {
        "english": {
            "Underweight": {
                "emoji": "💪",
                "main": "Focus on healthy weight gain through nutrition and strength training",
                "tips": [
                    "🥑 Include healthy fats like avocados, nuts, and olive oil",
                    "🥛 Add protein-rich foods to every meal (eggs, fish, legumes)",
                    "🏋️‍♀️ Start resistance training to build muscle mass",
                    "👨‍⚕️ Consult a nutritionist for personalized meal plans"
                ]
            },
            "Normal": {
                "emoji": "🌟",
                "main": "Maintain your healthy lifestyle with consistent habits",
                "tips": [
                    "🥗 Continue eating a variety of nutritious foods",
                    "🚶‍♂️ Maintain regular physical activity (150 min/week)",
                    "💧 Stay hydrated with 8-10 glasses of water daily",
                    "😴 Prioritize quality sleep (7-9 hours per night)"
                ]
            },
            "Overweight": {
                "emoji": "🔥",
                "main": "Focus on sustainable weight loss through lifestyle changes",
                "tips": [
                    "🍽️ Practice portion control and mindful eating",
                    "🏃‍♀️ Gradually increase physical activity and cardio",
                    "🚫 Limit processed foods, sugary drinks, and snacks",
                    "📱 Track your food intake and exercise progress"
                ]
            }
        },
        "tamil": {
            "குறைந்த எடை": {
                "emoji": "💪",
                "main": "ஊட்டச்சத்து மற்றும் வலிமை பயிற்சி மூலம் ஆரோக்கியமான எடை அதிகரிப்பில் கவனம் செலுத்துங்கள்",
                "tips": [
                    "🥑 ஆரோக்கியமான கொழுப்புகளான வெண்ணெய் பழம், கொட்டைகள், ஆலிவ் எண்ணெய் சேர்க்கவும்",
                    "🥛 ஒவ்வொரு உணவிலும் புரத சத்து நிறைந்த உணவுகளை சேர்க்கவும் (முட்டை, மீன், பருப்பு வகைகள்)",
                    "🏋️‍♀️ தசை வலிமை அதிகரிக்க எதிர்ப்பு பயிற்சி தொடங்குங்கள்",
                    "👨‍⚕️ தனிப்பட்ட உணவு திட்டத்திற்காக ஊட்டச்சத்து நிபுணரை அணுகவும்"
                ]
            },
            "சாதாரண": {
                "emoji": "🌟",
                "main": "நிலையான பழக்கவழக்கங்களுடன் உங்கள் ஆரோக்கியமான வாழ்க்கை முறையை பராமரிக்கவும்",
                "tips": [
                    "🥗 பல்வேறு ஊட்டச்சத்து நிறைந்த உணவுகளை சாப்பிடுவதை தொடருங்கள்",
                    "🚶‍♂️ வாரத்திற்கு 150 நிமிடங்கள் தொடர்ந்து உடல் செயல்பாடுகளை பராமரிக்கவும்",
                    "💧 தினமும் 8-10 கிளாஸ் தண்ணீர் குடித்து நீரேற்றத்தை பராமரிக்கவும்",
                    "😴 தரமான தூக்கத்திற்கு முன்னுரிமை கொடுங்கள் (இரவுக்கு 7-9 மணி நேரம்)"
                ]
            },
            "அதிக எடை": {
                "emoji": "🔥",
                "main": "வாழ்க்கை முறை மாற்றங்கள் மூலம் நிலையான எடை குறைப்பில் கவனம் செலுத்துங்கள்",
                "tips": [
                    "🍽️ உணவு அளவு கட்டுப்பாடு மற்றும் கவனமுடன் உண்ணும் பழக்கத்தை கடைப்பிடிக்கவும்",
                    "🏃‍♀️ படிப்படியாக உடல் செயல்பாடு மற்றும் கார்டியோ அதிகரிக்கவும்",
                    "🚫 பதப்படுத்தப்பட்ட உணவுகள், இனிப்பு பானங்கள் மற்றும் சிற்றுண்டிகளை கட்டுப்படுத்துங்கள்",
                    "📱 உங்கள் உணவு உட்கொள்ளல் மற்றும் உடற்பயிற்சி முன்னேற்றத்தை கண்காணிக்கவும்"
                ]
            }
        }
    }
    
    lang_suggestions = suggestions.get(language, suggestions["english"])
    return lang_suggestions.get(category, lang_suggestions.get("Normal", lang_suggestions.get("சாதாரண")))

def get_motivational_content(category, language):
    """Get motivational content based on BMI category and language"""
    content = {
        "english": {
            "Underweight": {
                "videos": [
                    "https://www.youtube.com/watch?v=4e_pu8cdQbM",  # LIFE IS SHORT - Inspirational
                    "https://www.youtube.com/shorts/5f7E4DQG6kk",  # GET UP AND GRIND - Motivational Speech
                    "https://www.youtube.com/shorts/rhuctOYBNvc"   # The Secret To Better Health
                ],
                "quotes": [
                    "💪 Every healthy meal is a step toward building your strength and vitality!",
                    "🌟 Building a healthy body takes time, patience, and consistent effort!",
                    "🔥 Each day is a new challenge - you have the power to overcome it!",
                    "💯 Strong bodies are built through daily dedication and perseverance!"
                ],
                "goals": [
                    "🎯 Aim to gain 1-2 kg per month through healthy eating",
                    "🏋️‍♀️ Include strength training 3 times per week",
                    "📊 Track overall health, not just weight measurements",
                    "🧠 Focus on energy levels and strength improvements"
                ]
            },
            "Normal": {
                "videos": [
                    "https://www.youtube.com/watch?v=Cg_GW7yhq20",  # Healthy Lifestyle
                    "https://www.youtube.com/shorts/Aj0gIGDltQY",  # Healthy Habits Tips
                    "https://www.youtube.com/watch?v=r01DOmPpxjg"   # Motivational Words
                ],
                "quotes": [
                    "🌟 Consistent healthy habits lead to long-term wellness and vitality!",
                    "💪 Your body is your temple - maintain it with love and respect!",
                    "🎯 Health is not a destination, it's a lifestyle you choose daily!",
                    "✨ You're already doing great - keep building on these healthy habits!"
                ],
                "goals": [
                    "🎯 Maintain current weight within ±2 kg range",
                    "🏃‍♀️ Continue regular exercise routine for cardiovascular health",
                    "🥗 Keep eating balanced, nutritious meals consistently",
                    "😊 Focus on mental wellness alongside physical health"
                ]
            },
            "Overweight": {
                "videos": [
                    "https://www.youtube.com/shorts/5f7E4DQG6kk",  # GET UP AND GRIND
                    "https://www.youtube.com/watch?v=4e_pu8cdQbM",  # LIFE IS SHORT
                    "https://www.youtube.com/shorts/rhuctOYBNvc"   # Better Health Secret
                ],
                "quotes": [
                    "🔥 Every step you take is progress toward a healthier, stronger version of yourself!",
                    "💪 Your transformation begins with the decision you make today!",
                    "🌟 Small changes lead to big results - you have what it takes!",
                    "🎯 Focus on progress, not perfection. Every effort counts toward your goals!"
                ],
                "goals": [
                    "🎯 Target 0.5-1 kg of healthy weight loss per week",
                    "🏃‍♀️ Include 30 minutes of cardio exercise 5 days per week",
                    "🍽️ Create sustainable calorie deficit through balanced eating",
                    "📈 Celebrate non-scale victories like increased energy and strength"
                ]
            }
        },
        "tamil": {
            "குறைந்த எடை": {
                "videos": [
                    "https://www.youtube.com/shorts/Fv-7cu0KoFs",  # Tamil Powerful Motivation
                    "https://www.youtube.com/shorts/BdZLYTr9xek",  # Change Your Life Now Tamil
                    "https://www.youtube.com/shorts/aVUIv5gKkHk"   # Healthy Lifestyle Tips Tamil
                ],
                "quotes": [
                    "💪 உங்கள் உடல் எடை அதிகரிக்க தினமும் ஆரோக்கியமான உணவு சாப்பிடுங்கள்!",
                    "🌟 நல்ல உடல்நலம் என்பது நேரம் மற்றும் பொறுமையுடன் கிடைக்கும்!",
                    "🔥 ஒவ்வொரு நாளும் ஒரு புதிய சவால் - உங்களால் முடியும்!",
                    "💯 வலிமையான உடல் தினசரி முயற்சியின் விளைவு!"
                ],
                "goals": [
                    "🎯 மாதம் 1-2 கிலோ எடை அதிகரிக்க இலக்கு வைக்கவும்",
                    "🏋️‍♀️ வாரத்திற்கு 3 முறை வலிமை பயிற்சி செய்யவும்",
                    "📊 எடை மட்டுமல்ல, ஒட்டுமொத்த ஆரோக்கியத்தை கவனிக்கவும்",
                    "🧠 சக்தி மற்றும் நல்ல உணர்வில் கவனம் செலுத்துங்கள்"
                ]
            },
            "சாதாரண": {
                "videos": [
                    "https://www.youtube.com/shorts/aVUIv5gKkHk",  # Healthy Lifestyle Tips Tamil
                    "https://www.youtube.com/shorts/9NxbZ-PuYiY",  # Summer Health Tips Tamil
                    "https://www.youtube.com/shorts/e3NYyyQjxus"   # Best Tips For Healthy Gut Tamil
                ],
                "quotes": [
                    "🌟 நிலையான ஆரோக்கியமான பழக்கங்கள் நீண்டகால வெற்றிக்கு வழிவகுக்கும்!",
                    "💪 உங்கள் உடல் ஒரு கோயில் - அதை அன்பு மற்றும் மரியாதையுடன் பராமரியுங்கள்!",
                    "🎯 ஆரோக்கியம் என்பது இலக்கு அல்ல, அது நீங்கள் தினமும் தேர்ந்தெடுக்கும் வாழ்க்கை முறை!",
                    "✨ நீங்கள் ஏற்கனவே சிறப்பாக செய்து கொண்டிருக்கிறீர்கள் - தொடர்ந்து செய்யுங்கள்!"
                ],
                "goals": [
                    "🎯 தற்போதைய எடையை ±2 கிலோவிற்குள் பராமரிக்கவும்",
                    "🏃‍♀️ தினசரி உடற்பயிற்சி வழக்கத்தை தொடர்ந்து செய்யவும்",
                    "🥗 சமச்சீரான, சத்தான உணவுகளை சாப்பிட்டு வாருங்கள்",
                    "😊 உடல் ஆரோக்கியத்துடன் மன நலனையும் கவனிக்கவும்"
                ]
            },
            "அதிக எடை": {
                "videos": [
                    "https://www.youtube.com/shorts/NlqO3UAlReA",  # Powerful Best Motivational Speech Tamil
                    "https://www.youtube.com/shorts/2ChkKDktwis",  # Tamil Motivational Speech
                    "https://www.youtube.com/shorts/QoJ2uFbjIjk"   # Tamil motivation inspiration
                ],
                "quotes": [
                    "🔥 நீங்கள் எடுக்கும் ஒவ்வொரு அடியும் ஆரோக்கியமான உங்களை நோக்கி முன்னேற்றம்!",
                    "💪 உங்கள் மாற்றம் இன்று தொடங்கும் முடிவில் இருந்து ஆரம்பமாகிறது!",
                    "🌟 சிறிய மாற்றங்கள் பெரிய முடிவுகளுக்கு வழிவகுக்கும் - உங்களால் முடியும்!",
                    "🎯 முழுமையை அல்ல, முன்னேற்றத்தில் கவனம் செலுத்துங்கள்!"
                ],
                "goals": [
                    "🎯 வாரத்திற்கு 0.5-1 கிலோ ஆரோக்கியமான எடை குறைப்பு",
                    "🏃‍♀️ வாரத்திற்கு 5 நாள் 30 நிமிட கார்டியோ பயிற்சி",
                    "🍽️ சமச்சீரான உணவின் மூலம் கலோரி குறைப்பு",
                    "📈 எடை அளவுகோல் அல்லாத வெற்றிகளை கொண்டாடுங்கள்"
                ]
            }
        }
    }
    
    lang_content = content.get(language, content["english"])
    return lang_content.get(category, lang_content.get("Normal", lang_content.get("சாதாரண")))

def create_compact_gauge(bmi, category_color):
    """Create a compact BMI gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = bmi,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "BMI", 'font': {'size': 16, 'color': '#2c3e50'}},
        gauge = {
            'axis': {'range': [None, 35], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': category_color, 'thickness': 0.4},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 18.5], 'color': '#e8f4fd'},
                {'range': [18.5, 25], 'color': '#e8f8f5'},
                {'range': [25, 35], 'color': '#fdf4e8'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75,
                'value': bmi
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        font={'color': "#2c3e50", 'family': "Arial"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'english'

# Language Toggle in Sidebar
with st.sidebar:
    st.markdown("### 🌐 Language / மொழி")
    language = st.radio(
        "Choose Language / மொழியைத் தேர்ந்தெடுக்கவும்:",
        options=['english', 'tamil'],
        format_func=lambda x: "🇺🇸 English" if x == 'english' else "🇮🇳 தமிழ்",
        key='language_selector',
        index=0 if st.session_state.language == 'english' else 1
    )
    
    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()

# Get translations for current language
t = get_translations(st.session_state.language)

# Header
st.markdown(f'<h1 class="bmi-title">{t["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="bmi-subtitle">{t["subtitle"]}</p>', unsafe_allow_html=True)

# First Row - Main BMI Calculator (3 columns only)
col1, col2, col3 = st.columns([1, 1, 1])

# Column 1: Input Section
with col1:
    st.markdown(f"""
    <div class="input-card">
        <div class="section-header-white">{t["your_details"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    height = st.number_input(
        t["height"],
        min_value=100.0,
        max_value=250.0,
        value=170.0,
        step=0.1
    )
    
    weight = st.number_input(
        t["weight"],
        min_value=30.0,
        max_value=200.0,
        value=70.0,
        step=0.1
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    calculate_btn = st.button(t["calculate"], type="primary", use_container_width=True)

# Calculate BMI (always calculated for real-time updates)
bmi = calculate_bmi(weight, height)
category, category_class, category_color = get_bmi_category(bmi)

# Get language-appropriate category name
if st.session_state.language == 'tamil':
    category_names = {'Underweight': 'குறைந்த எடை', 'Normal': 'சாதாரண', 'Overweight': 'அதிக எடை'}
    display_category = category_names.get(category, category)
else:
    display_category = category

suggestions = get_health_suggestions(display_category, st.session_state.language)
motivational_content = get_motivational_content(display_category, st.session_state.language)

# Column 2: BMI Results
with col2:
    st.markdown(f"""
    <div class="result-card">
        <div class="section-header">{t["your_bmi"]}</div>
        <div class="bmi-value" style="color: {category_color};">{bmi}</div>
        <div style="text-align: center;">
            <span class="category-badge {category_class}">{display_category}</span>
        </div>
        <div style="text-align: center; margin-top: 1rem; color: #666;">
            <strong>{t["bmi_formula"]}</strong><br>
            Weight ÷ Height²<br>
            {weight} ÷ {height/100:.2f}² = {bmi}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Column 3: Visual Gauge
with col3:
    st.markdown(f"""
    <div class="result-card">
        <div class="section-header">{t["bmi_scale"]}</div>
    </div>
    """, unsafe_allow_html=True)
    
    gauge_fig = create_compact_gauge(bmi, category_color)
    st.plotly_chart(gauge_fig, use_container_width=True)

# Second Row - Action Plan and Reference (Full Width)
st.markdown("---")

# Action Plan and Reference in 2 columns
action_col1, action_col2 = st.columns([1.5, 1])

with action_col1:
    st.markdown(f"""
    <div class="tips-card">
        <div class="section-header">{suggestions['emoji']} {t["action_plan"]}</div>
        <div class="tips-main-text">
            {suggestions['main']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action items
    for tip in suggestions['tips']:
        st.markdown(f'<div class="tip-item">{tip}</div>', unsafe_allow_html=True)

with action_col2:
    st.markdown(f"### {t['bmi_categories']}")
    reference_data = {
        t['categories'][0]: ['< 18.5'],
        t['categories'][1]: ['18.5-24.9'], 
        t['categories'][2]: ['≥ 25.0']
    }
    
    df_data = {
        'Category' if st.session_state.language == 'english' else 'வகை': t['categories'],
        'BMI Range' if st.session_state.language == 'english' else 'BMI வரம்பு': ['< 18.5', '18.5-24.9', '≥ 25.0']
    }
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Third Row - Motivation Zone (Full Width)
st.markdown("---")
st.markdown(f"""
<div class="motivation-card">
    <div class="section-header" style="color: white; font-size: 2rem;">🎯 {t["motivation_hub"]} - {display_category}</div>
    <div style="margin-bottom: 2rem; font-size: 1.2rem;">
        {t["transform_text"].format(category=display_category.lower())}
    </div>
</div>
""", unsafe_allow_html=True)

# Motivation content in 3 columns
motivation_col1, motivation_col2, motivation_col3 = st.columns([1, 1, 1])

with motivation_col1:
    # Motivational Quote
    random_quote = random.choice(motivational_content['quotes'])
    st.markdown(f'<div class="motivation-quote">{t["daily_motivation"]}<br>{random_quote}</div>', unsafe_allow_html=True)

with motivation_col2:
    # Health Goals
    st.markdown(f"### {t['health_goals']}")
    for goal in motivational_content['goals']:
        st.markdown(f"""
        <div class="motivation-element">
            <div style="color: white; font-size: 0.9rem; text-align: center;">
                {goal}
            </div>
        </div>
        """, unsafe_allow_html=True)

with motivation_col3:
    # Motivational Video
    st.markdown(f"### {t['motivation_video']}")
    video_url = random.choice(motivational_content['videos'])
    
    # Extract video ID from YouTube URL
    if "shorts/" in video_url:
        video_id = video_url.split("shorts/")[1]
    elif "watch?v=" in video_url:
        video_id = video_url.split("watch?v=")[1]
        if "&" in video_id:
            video_id = video_id.split("&")[0]
    else:
        video_id = video_url.split("/")[-1]
    
    # Embed YouTube video
    st.markdown(f"""
    <div class="video-container">
        <iframe width="100%" height="315" 
        src="https://www.youtube.com/embed/{video_id}" 
        frameborder="0" allowfullscreen>
        </iframe>
    </div>
    """, unsafe_allow_html=True)

# Action Button
col_center1, col_center2, col_center3 = st.columns([1, 1, 1])
with col_center2:
    if st.button(t["get_new_motivation"], use_container_width=True, type="secondary"):
        st.rerun()

# Footer
st.markdown(f"""
<div style="text-align: center; color: rgba(255, 255, 255, 0.9); padding: 1.5rem; margin-top: 2rem; 
     background: rgba(255, 255, 255, 0.1); border-radius: 15px;">
    <h3 style="color: white;">{t["health_journey"]}</h3>
    <p style="font-size: 1.1rem;">{t["bmi_status"].format(bmi=bmi, category=display_category)}</p>
    <p><small>{t["disclaimer"]}</small></p>
    <p style="color: #ffc107; font-weight: bold;">{t["footer_message"]}</p>
    <p>🎓 Keep coding, keep learning! Made with ❤️ by Shaid</p>
</div>
""", unsafe_allow_html=True)


