import streamlit as st
from groq import Groq
import base64
from streamlit_mic_recorder import mic_recorder
import io

# 1. Page Config
st.set_page_config(page_title="AURA", page_icon="✨", layout="centered")

# 2. The "ChatGPT-Style" CSS (Hiding all the jargon)
st.markdown("""
    <style>
    /* Absolute Dark Mode */
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stHeader"], header, footer {display: none !important;}
    
    .brand { 
        color: #FFD700; font-family: 'Inter', sans-serif; font-weight: 200; 
        letter-spacing: 10px; text-align: center; padding: 20px 0; font-size: 32px; 
    }

    /* FORCING HORIZONTAL ALIGNMENT */
    [data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Hiding the default 'Upload' box and jargon completely */
    .stFileUploader { position: absolute; opacity: 0; z-index: -1; width: 0; }
    div[data-testid="stFileUploaderDropzone"] { display: none !important; }

    /* The Text Box - No Border, No Label */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
    }

    /* Icons */
    .plus-btn { font-size: 32px; cursor: pointer; color: #888; transition: 0.3s; }
    .plus-btn:hover { color: #FFD700; }

    /* The Send Button */
    .stButton>button {
        width: 50px !important; height: 50px !important;
        border-radius: 50% !important; background-color: #FFFFFF !important;
        color: #000000 !important; border: none; font-weight: bold;
        display: flex; align-items: center; justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Secure API Logic
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Secrets not configured correctly.")
    st.stop()

st.markdown('<div class="brand">AURA</div>', unsafe_allow_html=True)

# 4. THE UNIFIED BAR (One single line for everything)
# [Plus] [Text Input] [Mic]
col1, col2, col3 = st.columns([1, 8, 1])

with col1:
    # Invisible uploader triggered by the '+' icon
    st.file_uploader("", type=['png', 'jpg', 'jpeg', 'mp4'], key="plus_vault", label_visibility="collapsed")
    st.markdown('<div class="plus-btn">⊕</div>', unsafe_allow_html=True)

with col2:
    # Main chat bar
    msg = st.text_input("", placeholder="Ask anything...", label_visibility="collapsed")

with col3:
    # Voice icon
    st.markdown('<div style="margin-top: 5px;">', unsafe_allow_html=True)
    voice_input = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='chat_mic')
    st.markdown('</div>', unsafe_allow_html=True)

# 5. The Submit Area
st.write("")
col_left, col_right = st.columns([8, 1])
with col_left:
    # Hidden energy slider
    energy = st.select_slider("", options=["Soft", "Chill", "Steady", "CEO", "Bold"], label_visibility="collapsed")
with col_right:
    # The Send Arrow
    submit = st.button("↑")

# 6. Response Logic
if submit:
    if msg or voice_input:
        with st.spinner(""):
            final_text = msg
            if voice_input:
                b = io.BytesIO(voice_input['bytes']); b.name = "input.wav"
                trans = client.audio.transcriptions.create(file=b, model="whisper-large-v3", response_format="text")
                final_text += f" {trans}"
            
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"High-status {energy} energy."}, {"role": "user", "content": final_text}]
            )
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border-left:3px solid #FFD700; margin-top:20px;'>{resp.choices[0].message.content}</div>", unsafe_allow_html=True)
