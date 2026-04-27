import streamlit as st
from groq import Groq
import base64
from streamlit_mic_recorder import mic_recorder
import io

# 1. Page Config
st.set_page_config(page_title="AURA", page_icon="✨", layout="centered")

# 2. Advanced CSS - Stripping away all "shitty" default UI elements
st.markdown("""
    <style>
    /* Pure Black Background */
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stHeader"], header, footer {display: none !important;}
    
    /* Elegant Gold Brand */
    .brand { 
        color: #FFD700; font-family: 'Inter', sans-serif; font-weight: 200; 
        letter-spacing: 8px; text-align: center; padding-top: 20px; font-size: 30px; 
    }
    
    /* WhatsApp-style Input Box */
    .stTextArea textarea {
        background-color: #111111 !important; color: white !important;
        border: 1px solid #222 !important; border-radius: 25px !important;
        padding: 15px 20px !important; font-size: 16px !important;
    }

    /* FORCIBLY HIDING THE UPLOAD BOXES (The 'Jargon' you hate) */
    .stFileUploader label { display: none !important; }
    .stFileUploader section { 
        background-color: transparent !important; 
        border: none !important; 
        padding: 0 !important; 
        min-height: 0px !important;
    }
    div[data-testid="stFileUploaderDropzone"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    div[data-testid="stFileUploaderDropzoneInstructions"] { display: none !important; }
    
    /* Floating Yellow Arrow */
    .stButton>button {
        width: 65px !important; height: 65px !important;
        border-radius: 50% !important; background-color: #FFD700 !important;
        position: fixed; bottom: 30px; right: 20px; z-index: 1000; border: none;
        box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.4);
    }

    /* Icon Layout - Centered and Clean */
    .icon-container { 
        font-size: 28px; text-align: center; cursor: pointer; 
        margin-top: -35px; /* Pulls icons up to remove the gap */
    }
    
    /* Removing the Red slider labels */
    div[data-testid="stMetricValue"] { color: #FFD700 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Silent API Key Fetch
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.stop()

# 4. The Interface
st.markdown('<div class="brand">AURA</div>', unsafe_allow_html=True)
st.write("---")

# Message Input
situation = st.text_area("", placeholder="Message...", height=100, label_visibility="collapsed")

# The Icon Row (Pure Visuals)
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.file_uploader("", type=['png', 'jpg'], key="img", label_visibility="collapsed")
    st.markdown('<div class="icon-container">🖼️</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="text-align:center; margin-top:-10px;">', unsafe_allow_html=True)
    voice = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic')
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.file_uploader("", type=['mp4'], key="vid", label_visibility="collapsed")
    st.markdown('<div class="icon-container">🎥</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="icon-container">📁</div>', unsafe_allow_html=True)

# Energy Slider
st.write("")
energy = st.select_slider("", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"], label_visibility="collapsed")

# Submit Arrow
if st.button("", icon=":material/arrow_forward:"):
    if situation or voice:
        with st.spinner(""):
            final_msg = situation
            if voice:
                b = io.BytesIO(voice['bytes']); b.name = "a.wav"
                trans = client.audio.transcriptions.create(file=b, model="whisper-large-v3", response_format="text")
                final_msg += f" {trans}"
            
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"Transform into {energy} energy. Concise."}, {"role": "user", "content": final_msg}]
            )
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border-left:4px solid #FFD700; color:#FFD700;'>{resp.choices[0].message.content}</div>", unsafe_allow_html=True)
