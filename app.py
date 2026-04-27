import streamlit as st
from groq import Groq
import io
from streamlit_mic_recorder import mic_recorder

# 1. High-End Configuration
st.set_page_config(page_title="AURA", page_icon="✨", layout="centered")

# 2. Total Stealth CSS (Hiding 'Manage App', Footers, and Jargon)
st.markdown("""
    <style>
    /* Absolute Dark Mode */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* KILL ALL STREAMLIT BRANDING & TOOLBARS */
    [data-testid="stHeader"], footer, #MainMenu, .stDeployButton, [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* AURA Title Styling */
    .brand { 
        color: #FFD700; font-family: 'Inter', sans-serif; font-weight: 200; 
        letter-spacing: 10px; text-align: center; padding: 40px 0 20px 0; font-size: 32px; 
    }

    /* THE UNIFIED INPUT BAR (WhatsApp/ChatGPT Style) */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
    }

    /* Hiding the ugly 'Upload' box logic */
    .stFileUploader { position: absolute; z-index: 2; opacity: 0; width: 50px; height: 50px; }
    div[data-testid="stFileUploaderDropzone"] { display: none !important; }

    /* Icons Positioning */
    .plus-icon { font-size: 32px; color: #FFD700; margin-top: -5px; cursor: pointer; }
    
    /* Circular Submit Button */
    .stButton>button {
        width: 55px !important; height: 55px !important;
        border-radius: 50% !important; background-color: #FFFFFF !important;
        color: #000 !important; border: none; font-weight: bold;
        box-shadow: 0px 4px 10px rgba(255,255,255,0.1);
    }

    /* Response Box */
    .response-style {
        background: #111; padding: 20px; border-radius: 15px; 
        border-left: 3px solid #FFD700; margin-top: 25px; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Secure API Connection
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Connect your Groq API Key in the Streamlit Secrets dashboard.")
    st.stop()

# 4. Interface Layout
st.markdown('<div class="brand">AURA</div>', unsafe_allow_html=True)

# The Row: [ + ] [ Message ] [ Mic ]
col_plus, col_text, col_mic = st.columns([1, 8, 1])

with col_plus:
    # Clicking the yellow plus actually triggers this invisible uploader
    st.file_uploader("", type=['png', 'jpg', 'jpeg', 'mp4'], key="vault", label_visibility="collapsed")
    st.markdown('<div class="plus-icon">⊕</div>', unsafe_allow_html=True)

with col_text:
    user_msg = st.text_input("", placeholder="Ask anything...", label_visibility="collapsed")

with col_mic:
    # Actual functional microphone
    audio_data = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='recorder')

# Energy Slider (Discreet)
energy = st.select_slider("", options=["Soft", "Unbothered", "Confident", "CEO", "Bold"], label_visibility="collapsed")

# The Submit Arrow (Floating style)
st.write("")
col_left, col_btn = st.columns([8, 1])
with col_btn:
    submit = st.button("↑")

# 5. Logic: Processing Input
if submit:
    if user_msg or audio_data:
        with st.spinner(""):
            context = user_msg
            
            # If user recorded audio, transcribe it first
            if audio_data:
                audio_bytes = audio_data['bytes']
                buf = io.BytesIO(audio_bytes)
                buf.name = "input.wav"
                transcription = client.audio.transcriptions.create(
                    file=buf, model="whisper-large-v3", response_format="text"
                )
                context += f" [Transcript: {transcription}]"

            # Generate the high-status response
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"You are a high-status consultant. Refine the user's input into a {energy} response. Be concise."},
                    {"role": "user", "content": context}
                ]
            )
            
            st.markdown(f"<div class='response-style'>{chat_completion.choices[0].message.content}</div>", unsafe_allow_html=True)

# Toast notification for uploads so user knows it worked
if st.session_state.vault:
    st.toast("Media attached! 🖼️")
