import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="AURA AI", page_icon="✨")
st.title("✨ AURA AI")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Get your key at aistudio.google.com")

if api_key:
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        # Using the 2026 stable flash model
        model = genai.GenerativeModel('gemini-2.0-flash')

        situation = st.text_area("What's the situation?", placeholder="e.g., Someone interrupted me in a meeting")
        aura = st.select_slider("Select your Aura", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"])

        if st.button("Aura-fy"):
            if situation:
                with st.spinner("Processing your Aura..."):
                    prompt = f"Rewrite this situation with a '{aura}' aura. Keep it short, powerful, and high-status. Do not explain, just give the response: {situation}"
                    response = model.generate_content(prompt)
                    st.subheader(f"{aura} Mode:")
                    st.success(response.text)
            else:
                st.warning("Please describe a situation first!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your Gemini API key in the sidebar to start.")
