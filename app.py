import streamlit as st
from groq import Groq
import base64
from streamlit_mic_recorder import mic_recorder
import io

# 1. Page Config
st.set_page_config(page_title="AURA", page_icon="✨", layout="centered")

# 2. Modern CSS (No clutter, pure professional look)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stHeader"], header, footer {display: none;}
    
    .brand { 
        color: #FFD700; font-family: 'Inter', sans-serif; font-weight: 200; 
        letter-spacing: 6px; text-align: center; padding-top: 20px; font-size: 32px;
    }
    
    .stTextArea textarea {
        background-color: #111111 !important; color: white !important;
        border: 1px solid #222 !important; border-radius: 15px !important;
    }

    .stButton>button {
        width: 65px !important; height: 65px !important;
        border-radius: 50% !important; background-color: #FFD700 !important;
        position: fixed; bottom: 30px; right: 30px; z-index: 1000; border: none;
    }

    .icon-label { text-align: center; font-size: 24px; margin-top: -40px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Silent API Key Fetch
try:
    # Pulls directly from the TOML you set up in Step 1
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Missing Secrets Configuration.")
    st.stop()

# 4. Interface
st.markdown('<div class="brand">AURA</div>', unsafe_allow_html=True)
st.write("---")

# Text Input
situation = st.text_area("", placeholder="Speak...", height=150, label_visibility="collapsed")

# Tool Icons
c1, c2, c3 = st.columns(3)
with c1:
    st.file_uploader("", type=['png', 'jpg'], key="img", label_visibility="collapsed")
    st.markdown('<div class="icon-label">🖼️</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div style="text-align:center; margin-top:-10px;">', unsafe_allow_html=True)
    voice = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic')
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.file_uploader("", type=['mp4'], key="vid", label_visibility="collapsed")
    st.markdown('<div class="icon-label">🎥</div>', unsafe_allow_html=True)

# Energy Slider
energy = st.select_slider("", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"], label_visibility="collapsed")

# Execute
if st.button("", icon=":material/arrow_forward:"):
    if situation or voice:
        with st.spinner(""):
            final_msg = situation
            if voice:
                buf = io.BytesIO(voice['bytes'])
                buf.name = "audio.wav"
                trans = client.audio.transcriptions.create(file=buf, model="whisper-large-v3", response_format="text")
                final_msg += f" {trans}"
            
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"High-status {energy} rewrite. Sharp and concise."},
                    {"role": "user", "content": final_msg}
                ]
            )
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border-left:4px solid #FFD700; color:#FFD700;'>{resp.choices[0].message.content}</div>", unsafe_allow_html=True)
