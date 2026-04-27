import streamlit as st
from groq import Groq
import base64
from streamlit_mic_recorder import mic_recorder
import io

# 1. Professional Minimalist UI
st.set_page_config(page_title="AURA", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stHeader"], header, footer {display: none;}
    
    .brand { 
        color: #FFD700; font-family: 'Inter', sans-serif; font-weight: 200; 
        letter-spacing: 8px; text-align: center; padding-top: 40px; font-size: 35px;
    }
    
    .stTextArea textarea {
        background-color: #111111 !important; color: white !important;
        border: 1px solid #222 !important; border-radius: 15px !important;
        padding: 20px !important;
    }

    .stButton>button {
        width: 65px !important; height: 65px !important;
        border-radius: 50% !important; background-color: #FFD700 !important;
        position: fixed; bottom: 30px; right: 30px; z-index: 1000; border: none;
    }

    .icon-box { text-align: center; font-size: 26px; margin-top: -45px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Key Fetching Logic
try:
    # This must match the name in your Secrets exactly
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Missing Secrets Configuration.")
    st.stop()

# 3. App Layout
st.markdown('<div class="brand">AURA</div>', unsafe_allow_html=True)
st.write("---")

# Invisible Label Input
situation = st.text_area("", placeholder="What is the context?", height=150, label_visibility="collapsed")

# Tools Row
c1, c2, c3 = st.columns(3)
with c1:
    st.file_uploader("", type=['png', 'jpg'], key="img", label_visibility="collapsed")
    st.markdown('<div class="icon-box">🖼️</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div style="text-align:center; margin-top:-10px;">', unsafe_allow_html=True)
    voice = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic')
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.file_uploader("", type=['mp4'], key="vid", label_visibility="collapsed")
    st.markdown('<div class="icon-box">🎥</div>', unsafe_allow_html=True)

# Stealth Energy Slider
st.write("")
energy = st.select_slider("", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"], label_visibility="collapsed")

# Floating Action Arrow
if st.button("", icon=":material/arrow_forward:"):
    if situation or voice:
        with st.spinner(""):
            final_text = situation
            if voice:
                buf = io.BytesIO(voice['bytes'])
                buf.name = "audio.wav"
                trans = client.audio.transcriptions.create(file=buf, model="whisper-large-v3", response_format="text")
                final_text += f" {trans}"
            
            # AI Refinement
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"High-status {energy} rewrite. Sharp, concise, and professional."},
                    {"role": "user", "content": final_text}
                ]
            )
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border-left:4px solid #FFD700; color:#FFD700; margin-top:20px;'>{resp.choices[0].message.content}</div>", unsafe_allow_html=True)
