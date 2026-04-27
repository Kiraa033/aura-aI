import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="AURA AI", page_icon="✨", layout="centered")

# Professional Dark & Gold UI Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    h1 {
        color: #FFD700;
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    /* Icon-Only Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background-color: #FFD700;
        color: #000000;
        border: none;
        transition: 0.3s;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .stButton>button:hover {
        background-color: #e6c200;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.4);
    }
    /* Remove default button label spacing */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 24px !important;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>AURA AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Refine your communication status instantly.</p>", unsafe_allow_html=True)
st.write("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Groq API Key", type="password")

if api_key:
    try:
        client = Groq(api_key=api_key)
        
        # Core Interface
        situation = st.text_area("Input", placeholder="Enter text to transform...", height=120)
        
        st.write("Select Energy")
        aura = st.select_slider("", options=["Soft Power", "Unbothered", "Confident", "CEO", "Bold"])

        # Icon-only arrow button
        if st.button("", icon=":material/arrow_forward:"):
            if situation:
                with st.spinner("Processing..."):
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": f"Professional consultant mode. Rewrite the input to have a '{aura}' energy. Concise, high-status, no preamble."},
                            {"role": "user", "content": situation}
                        ]
                    )
                    st.write("---")
                    st.success(completion.choices[0].message.content)
            else:
                st.warning("Please enter text first.")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Enter your Groq key in the sidebar to begin.")
