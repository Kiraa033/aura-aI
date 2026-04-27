import streamlit as st
from groq import Groq
import base64
from streamlit_mic_recorder import mic_recorder
import io

# 1. Page Configuration
st.set_page_config(page_title="AURA AI", page_icon="✨", layout="centered")

# 2. Professional CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { color: #FFD700; text-align: center; font-weight: 800; margin-bottom: 0px; }
    .stButton>button {
        width: 100%; border-radius: 50px; height: 3.5em;
        background-color: #FFD700; color: #000000; border: none; font-weight: bold;
    }
    .stButton>button:hover { background-color: #e6c200; box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.4); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1c24; border-radius: 10px; padding: 10px 20px; color: white; }
    .stTextArea textarea { background-color: #1a1c24 !important; color: white !important; }
    /* Style for the Mic Recorder button to fit the gold theme */
    div[data-testid="stVerticalBlock"] > div:has(button) { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("<h1>AURA AI</h1>")
st.markdown("<p style='text-align: center; color: #888;'>Multimodal Status & Communication Suite</p>", unsafe_allow_html=True)
st.write("---")

# 3. Sidebar for API and Logs
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Groq API Key", type="password")
    if st.session_state.history:
        st.divider()
        st.subheader("📜 Recent History")
        for item in reversed(st.session_state.history[-5:]):
            with st.expander(f"{item['energy']} Energy"):
                st.write(item['result'])

# 4. Core Application Logic
if api_key:
    try:
        client = Groq(api_key=api_key)
        
        tab1, tab2, tab3 = st.tabs(["📝 Text", "📸 Media", "🎤 Live Voice"])
        
        context_text = ""
        live_audio_input = None

        with tab1:
            context_text = st.text_area("Context", placeholder="Describe your situation...", height=150)

        with tab2:
            st.write("Analyze visuals or video files")
            image_file = st.file_uploader("Upload screenshot or image", type=['png', 'jpg', 'jpeg'])
            video_file = st.file_uploader("Upload video context", type=['mp4', 'mov'])

        with tab3:
            st.write("Click to Record (Live Mic)")
            # This adds the Mic Icon and Recording capability
            audio_record = mic_recorder(
                start_prompt="Start Recording 🎙️",
                stop_prompt="Stop Recording 🛑",
                key='recorder'
            )
            
            if audio_record:
                st.audio(audio_record['bytes'])
                live_audio_input = audio_record['bytes']

        st.write("### Select Energy")
        energy_level = st.select_slider("", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"])

        # Final Action Button
        if st.button("", icon=":material/arrow_forward:"):
            with st.spinner("Processing Multimodal Context..."):
                final_input = context_text
                
                # Handle Live Voice Transcription
                if live_audio_input:
                    # Convert bytes to file-like object for Groq Whisper
                    buffer = io.BytesIO(live_audio_input)
                    buffer.name = "recording.wav"
                    transcription = client.audio.transcriptions.create(
                        file=buffer,
                        model="whisper-large-v3",
                        response_format="text"
                    )
                    final_input += f"\n[Live Voice Transcript: {transcription}]"

                # Handle Image Analysis (Vision)
                if image_file:
                    base64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
                    vision_resp = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "What is happening in this image?"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }]
                    )
                    final_input += f"\n[Visual Analysis: {vision_resp.choices[0].message.content}]"

                # Final Refinement
                if final_input.strip() == "":
                    st.warning("Please provide some form of input (Text or Voice).")
                else:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": f"You are a communication strategist. Rewrite the user input using '{energy_level}' energy. Concise, powerful, high-status. Provide only the text."},
                            {"role": "user", "content": final_input}
                        ]
                    )
                    
                    output = response.choices[0].message.content
                    st.session_state.history.append({"energy": energy_level, "result": output})
                    
                    st.divider()
                    st.success(output)
                    
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Please enter your Groq API Key in the sidebar.")
