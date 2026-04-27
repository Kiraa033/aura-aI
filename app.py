import streamlit as st
from groq import Groq
import base64

# 1. Page Configuration
st.set_page_config(page_title="AURA AI", page_icon="✨", layout="centered")

# 2. Professional CSS Styling (Dark/Gold Theme)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { color: #FFD700; text-align: center; font-weight: 800; }
    .stButton>button {
        width: 100%; border-radius: 50px; height: 3.5em;
        background-color: #FFD700; color: #000000; border: none; font-weight: bold;
    }
    .stButton>button:hover { background-color: #e6c200; box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.4); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1c24; border-radius: 10px; padding: 10px 20px; color: white; }
    .stTextArea textarea { background-color: #1a1c24 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize History
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("<h1>AURA AI</h1>")
st.markdown("<p style='text-align: center; color: #888;'>Multimodal Status & Communication Suite</p>", unsafe_allow_html=True)
st.write("---")

# 4. Sidebar for API and Logs
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Groq API Key", type="password")
    if st.session_state.history:
        st.divider()
        st.subheader("📜 Recent History")
        for item in reversed(st.session_state.history[-5:]):
            with st.expander(f"{item['energy']} Energy"):
                st.write(item['result'])

# 5. Core Application Logic
if api_key:
    try:
        client = Groq(api_key=api_key)
        
        # Tabs for Inputs
        tab1, tab2, tab3 = st.tabs(["📝 Text", "📸 Image/Vision", "🎤 Voice"])
        
        context_text = ""

        with tab1:
            context_text = st.text_area("Situation Context", placeholder="Describe the situation or paste a message...", height=150)

        with tab2:
            image_file = st.file_uploader("Upload screenshot or image", type=['png', 'jpg', 'jpeg'])
            if image_file:
                st.image(image_file, caption="Analysis Pending...", width=300)

        with tab3:
            audio_file = st.file_uploader("Upload voice note", type=['mp3', 'wav', 'm4a', 'ogg'])
            if audio_file:
                st.audio(audio_file)

        st.write("### Select Energy")
        energy_level = st.select_slider("", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"])

        # Final Action Button (Icon-only)
        if st.button("", icon=":material/arrow_forward:"):
            with st.spinner("Processing Multimodal Context..."):
                final_input = context_text
                
                # A. Handle Audio Transcription
                if audio_file:
                    transcription = client.audio.transcriptions.create(
                        file=(audio_file.name, audio_file.read()),
                        model="whisper-large-v3",
                        response_format="text"
                    )
                    final_input += f"\n[Audio Transcript: {transcription}]"

                # B. Handle Image Vision
                image_analysis = ""
                if image_file:
                    base64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
                    vision_resp = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Describe what is happening in this image briefly."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }]
                    )
                    image_analysis = vision_resp.choices[0].message.content
                    final_input += f"\n[Visual Context: {image_analysis}]"

                # C. Final Refinement
                if final_input.strip() == "":
                    st.warning("Please provide some form of input.")
                else:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": f"You are a communication strategist. Rewrite the user context using '{energy_level}' energy. Be concise and high-status."},
                            {"role": "user", "content": final_input}
                        ]
                    )
                    
                    output = response.choices[0].message.content
                    st.session_state.history.append({"energy": energy_level, "result": output})
                    
                    st.divider()
                    st.subheader(f"⚡ {energy_level} Output:")
                    st.success(output)
                    
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Please enter your Groq API Key in the sidebar to activate all features.")
