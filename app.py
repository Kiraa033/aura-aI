import streamlit as st
from groq import Groq
import base64
from streamlit_mic_recorder import mic_recorder
import io

# 1. Page Configuration
st.set_page_config(page_title="AURA", page_icon="✨", layout="centered")

# 2. Modern Unified Input CSS
st.markdown("""
    <style>
    /* Absolute Dark Mode */
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stHeader"], header, footer {display: none !important;}
    
    /* Branding */
    .brand { 
        color: #FFD700; font-family: 'Inter', sans-serif; font-weight: 200; 
        letter-spacing: 10px; text-align: center; padding: 20px 0; font-size: 28px; 
    }

    /* THE UNIFIED BAR CONTAINER */
    .input-container {
        display: flex;
        align-items: center;
        background-color: #1a1a1a;
        border-radius: 30px;
        padding: 5px 15px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }

    /* Hiding Streamlit's default ugly boxes */
    .stFileUploader { position: absolute; opacity: 0; z-index: -1; width: 0; height: 0; }
    div[data-testid="stFileUploaderDropzone"] { display: none !important; }

    /* Styling the Text Input to look like a chat bar */
    .stTextInput input {
        background-color: transparent !important;
        border: none !important;
        color: white !important;
        padding: 10px !important;
    }

    /* Floating Action Button */
    .stButton>button {
        width: 50px !important; height: 50px !important;
        border-radius: 50% !important; background-color: #FFFFFF !important;
        color: black !important; border: none; font-weight: bold;
    }
    
    /* Slider Styling */
    .stSlider { padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Secure API Key
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("System Error: Key not found.")
    st.stop()

st.markdown('<div class="brand">AURA</div>', unsafe_allow_html=True)

# 4. UNIFIED INPUT ROW (The + icon, Text, and Mic)
# We use columns to force them onto one line
col_plus, col_text, col_mic = st.columns([1, 8, 1])

with col_plus:
    # This is the "plus" icon that triggers your file upload
    st.file_uploader("", type=['png', 'jpg', 'jpeg', 'mp4'], key="vault")
    st.markdown('<div style="font-size: 30px; cursor: pointer; text-align: center; padding-top: 5px;">⊕</div>', unsafe_allow_html=True)

with col_text:
    # The message box
    msg = st.text_input("", placeholder="Ask anything...", label_visibility="collapsed")

with col_mic:
    # The live voice icon
    st.markdown('<div style="margin-top: 5px;">', unsafe_allow_html=True)
    voice_data = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic_bar')
    st.markdown('</div>', unsafe_allow_html=True)

# 5. Energy Selection (Minimalist)
energy = st.select_slider("", options=["Soft", "Unbothered", "Confident", "CEO", "Bold"], label_visibility="collapsed")

# 6. The Send Button (White Circle Icon)
st.write("")
if st.button("↑"):
    if msg or voice_data:
        with st.spinner(""):
            final_query = msg
            if voice_data:
                b = io.BytesIO(voice_data['bytes']); b.name = "voice.wav"
                trans = client.audio.transcriptions.create(file=b, model="whisper-large-v3", response_format="text")
                final_query += f" {trans}"
            
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"You are a high-status consultant. Respond with {energy} energy."}, 
                          {"role": "user", "content": final_query}]
            )
            
            st.markdown(f"<div style='background:#1a1a1a; padding:20px; border-radius:15px; border-left: 3px solid #FFD700; margin-top:20px;'>{resp.choices[0].message.content}</div>", unsafe_allow_html=True)
