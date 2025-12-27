import streamlit as st

# ✅ This controls browser tab title and sidebar label
st.set_page_config(
    page_title="AI Recruitment Platform",     # Appears in browser tab
    page_icon="🤖",                           # Optional icon
    layout="centered"                         # or "wide"
)
st.title("🤖 Welcome to AI Recruitment Platform")

st.markdown("""
Use the sidebar to explore:
- 📄 Resume Assistant
- 🧠 Quiz Practice
- 💼 Job Board
""")
