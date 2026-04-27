import streamlit as st
from groq import Groq

# Page setup
st.set_page_config(page_title="AURA AI", page_icon="✨")
st.title("✨ AURA AI (Groq Edition)")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    # Note: Label changed to Groq API Key
    api_key = st.text_input("Groq API Key", type="password")
    st.info("Get your key at console.groq.com")

if api_key:
    try:
        # Configure Groq
        client = Groq(api_key=api_key)
        
        situation = st.text_area("What's the situation?", placeholder="e.g., Someone interrupted me in a meeting")
        aura = st.select_slider("Select your Aura", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"])

        if st.button("Aura-fy"):
            if situation:
                with st.spinner("Processing your Aura..."):
                    # Using Llama 3.3 70B - very powerful and fast
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": f"You are an expert in high-status communication. Rewrite the user's situation with a '{aura}' aura. Keep it short and powerful. Only give the response text."},
                            {"role": "user", "content": situation}
                        ]
                    )
                    st.subheader(f"{aura} Mode:")
                    st.success(completion.choices[0].message.content)
            else:
                st.warning("Please describe a situation first!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your Groq API key in the sidebar to start.")
