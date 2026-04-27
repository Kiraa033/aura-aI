import streamlit as st
from groq import Groq
import base64
from streamlit_mic_recorder import mic_recorder
import io

# 1. High-End UI Config
st.set_page_config(page_title="AURA", page_icon="✨", layout="centered")

# 2. Ultra-Modern CSS (Removing all 'Jargon' and labels)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stHeader"], header, footer {display: none;}
    
    /* Clean Minimalist Header */
    .brand { 
        color: #FFD700; font-family: 'Inter', sans-serif; font-weight: 200; 
        letter-spacing: 8px; text-align: center; padding-top: 20px; font-size: 30px;
    }
    
    /* Sleek Input Bar (Like WhatsApp/Telegram) */
    .stTextArea textarea {
        background-color: #111111 !important; color: white !important;
        border: 1px solid #222 !important; border-radius: 25px !important;
        padding: 15px 20px !important; font-size: 16px !important;
    }

    /* Fixed Floating Action Button (The Arrow) */
    .stButton>button {
        width: 60px !important; height: 60px !important;
        border-radius: 50% !important; background-color: #FFD700 !important;
        position: fixed; bottom: 30px; right: 20px; z-index: 1000; border: none;
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.4);
    }

    /* Hiding the ugly Streamlit 'Upload' labels */
    .stFileUploader label { display: none; }
    .stFileUploader section { background-color: transparent !important; border: none !important; padding: 0 !important; }
    [data-testid="stFileUploaderDropzoneInstructions"] { display: none; }

    /* Icon Row Styling */
    .icon-btn { font-size: 26px; text-align: center; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# 3. Secure API Key Fetch (Hidden from User)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Connect API Key in Dashboard Secrets.")
    st.stop()

# 4. The Interface
st.markdown('<div class="brand">AURA</div>', unsafe_allow_html=True)
st.write("")

# Main Context Input
situation = st.text_area("", placeholder="Message...", height=100, label_visibility="collapsed")

# Professional Icon Row (No text, just tools)
c1, c2, c3, c4 = st.columns([1, 1, 1, 1])

with c1:
    img = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key="img", label_visibility="collapsed")
    st.markdown('<div class="icon-btn">🖼️</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div style="margin-top:-8px; text-align:center;">', unsafe_allow_html=True)
    voice = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic')
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    vid = st.file_uploader("", type=['mp4'], key="vid", label_visibility="collapsed")
    st.markdown('<div class="icon-btn">🎥</div>', unsafe_allow_html=True)

with c4:
    # Just an extra icon to balance the UI like a real app
    st.markdown('<div class="icon-btn">📁</div>', unsafe_allow_html=True)

# Discreet Energy Slider
st.write("")
energy = st.select_slider("", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"], label_visibility="collapsed")

# Submit Button (Floating Arrow)
if st.button("", icon=":material/arrow_forward:"):
    if situation or voice:
        with st.spinner(""):
            final_msg = situation
            if voice:
                buf = io.BytesIO(voice['bytes'])
                buf.name = "a.wav"
                trans = client.audio.transcriptions.create(file=buf, model="whisper-large-v3", response_format="text")
                final_msg += f" {trans}"
            
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"High-status {energy} energy. Short."}, {"role": "user", "content": final_msg}]
            )
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border-left:4px solid #FFD700; color:#FFD700;'>{resp.choices[0].message.content}</div>", unsafe_allow_html=True)
