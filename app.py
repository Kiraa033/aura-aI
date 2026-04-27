import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="AURA AI", page_icon="✨", layout="centered")

# 2. Professional CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #FFD700; text-align: center; font-family: 'Inter', sans-serif; font-weight: 800; }
    .stButton>button {
        width: 100%; border-radius: 50px; height: 3.5em;
        background-color: #FFD700; color: #000000; border: none; transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #e6c200; box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.4);
    }
    .stTextArea>div>div>textarea { background-color: #1a1c24; color: white; border-radius: 10px; }
    .stExpander { background-color: #1a1c24; border: none; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Session State for History
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("<h1>AURA AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Professional Status & Communication Suite</p>", unsafe_allow_html=True)
st.write("---")

# 4. Sidebar Configuration
with st.sidebar:
    st.header("⚙️ System Setup")
    api_key = st.text_input("Groq API Key", type="password")
    st.divider()
    if st.session_state.history:
        st.subheader("📜 Recent Logs")
        for h in reversed(st.session_state.history[-5:]):
            st.caption(f"**{h['energy']}**: {h['msg'][:50]}...")

# 5. Main Interface
if api_key:
    try:
        client = Groq(api_key=api_key)

        # Tabbed Interface for Multimedia
        tab1, tab2, tab3 = st.tabs(["📝 Text", "📸 Media", "🎤 Voice"])

        with tab1:
            situation = st.text_area("Context", placeholder="Describe your situation...", height=100)

        with tab2:
            st.write("Analyze visuals for better context")
            uploaded_file = st.file_uploader("Upload Image or Video", type=['png', 'jpg', 'mp4', 'mov'])
            if uploaded_file:
                st.info(f"Attached: {uploaded_file.name}")

        with tab3:
            st.write("Audio Input")
            audio_file = st.file_uploader("Upload Voice Note", type=['mp3', 'wav', 'm4a'])
            if audio_file:
                st.audio(audio_file)

        st.write("### Select Energy")
        aura = st.select_slider("", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"])

        # Final Arrow Action Button
        if st.button("", icon=":material/arrow_forward:"):
            if situation or uploaded_file or audio_file:
                with st.spinner("Analyzing Status..."):
                    # Process text (Multimedia analysis would require Vision/Whisper models in a full build)
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": f"High-status consultant mode. Transform the input into '{aura}' energy. Concise and powerful."},
                            {"role": "user", "content": f"Context: {situation}. Energy requested: {aura}"}
                        ]
                    )
                    
                    result = completion.choices[0].message.content
                    st.session_state.history.append({"energy": aura, "msg": result})
                    
                    st.divider()
                    st.markdown(f"### ⚡ Optimized Output")
                    st.success(result)
                    st.button("📋 Copy Response")
            else:
                st.warning("Please provide input via text, media, or voice.")

    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Please enter your API credentials in the sidebar.")
