import streamlit as st
from groq import Groq
import base64
from streamlit_mic_recorder import mic_recorder
import io

# 1. Page Config
st.set_page_config(page_title="AURA", page_icon="✨", layout="centered")

# 2. Functional CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stHeader"], header, footer {display: none !important;}
    
    .brand { 
        color: #FFD700; font-family: 'Inter', sans-serif; font-weight: 200; 
        letter-spacing: 10px; text-align: center; padding: 20px 0; font-size: 32px; 
    }

    /* THE CHAT BAR CONTAINER */
    .chat-container {
        display: flex;
        align-items: center;
        background-color: #1a1a1a;
        border-radius: 30px;
        padding: 5px 15px;
        border: 1px solid #333;
    }

    /* Making the uploaders invisible but clickable */
    .stFileUploader {
        position: absolute;
        z-index: 2;
        opacity: 0; /* This makes it invisible but it still sits over the + icon */
        width: 40px;
    }
    
    /* Text Input Styling */
    .stTextInput input {
        background-color: transparent !important;
        border: none !important;
        color: white !important;
    }

    /* Submit Button (The White Arrow) */
    .stButton>button {
        width: 50px !important; height: 50px !important;
        border-radius: 50% !important; background-color: #FFFFFF !important;
        color: #000 !important; border: none; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API Logic
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.markdown('<div class="brand">AURA</div>', unsafe_allow_html=True)

# 4. THE FUNCTIONAL BAR
# We use columns to align them exactly like your screenshot
col_plus, col_text, col_mic = st.columns([1, 8, 1])

with col_plus:
    # This sits INVISIBLY on top of the plus icon. When you tap +, it opens your files.
    st.file_uploader("", type=['png', 'jpg', 'jpeg', 'mp4'], key="plus_upload", label_visibility="collapsed")
    st.markdown('<div style="font-size: 30px; color: #FFD700; pointer-events: none; margin-top: -45px;">⊕</div>', unsafe_allow_html=True)

with col_text:
    user_msg = st.text_input("", placeholder="Ask anything...", label_visibility="collapsed")

with col_mic:
    # Functional Mic Recorder
    # Note: If it doesn't record, ensure your site has HTTPS enabled!
    audio_data = mic_recorder(
        start_prompt="🎙️", 
        stop_prompt="🛑", 
        key='active_mic',
        use_container_width=False
    )

# 5. Energy Selection & Send
energy = st.select_slider("", options=["Soft", "Unbothered", "Confident", "CEO", "Bold"], label_visibility="collapsed")

st.write("")
if st.button("↑"):
    if user_msg or audio_data:
        with st.spinner(""):
            combined_input = user_msg
            
            # Handle the Voice recording if exists
            if audio_data:
                audio_bytes = audio_data['bytes']
                buffer = io.BytesIO(audio_bytes)
                buffer.name = "audio.wav"
                transcription = client.audio.transcriptions.create(
                    file=buffer, model="whisper-large-v3", response_format="text"
                )
                combined_input += f" [User Voice: {transcription}]"

            # Response Generation
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Respond with {energy} energy. Be sharp."},
                    {"role": "user", "content": combined_input}
                ]
            )
            
            st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border-left: 3px solid #FFD700;'>{response.choices[0].message.content}</div>", unsafe_allow_html=True)

# Visual Confirmation for Uploads
if st.session_state.plus_upload:
    st.toast("File attached successfully! 🖼️")
