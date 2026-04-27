import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AURA AI", page_icon="✨")
st.title("✨ AURA AI")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    situation = st.text_area("What's the situation?", placeholder="e.g., Asking for a deadline extension")
    aura = st.select_slider("Select your Aura", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"])

    if st.button("Aura-fy"):
        if situation:
            prompt = f"Rewrite this situation with a '{aura}' aura. Keep it short, powerful, and high-status: {situation}"
            response = model.generate_content(prompt)
            st.subheader(f"{aura} Mode:")
            st.success(response.text)
        else:
            st.warning("Please describe a situation first!")
else:
    st.info("Please enter your Gemini API key in the sidebar to start.")
