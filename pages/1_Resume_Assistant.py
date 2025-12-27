import streamlit as st
import fitz  # PyMuPDF
from utils.gemini_api import call_gemini

st.title("📤 Resume Assistant")

uploaded_file = st.file_uploader("Upload your resume (PDF/TXT)", type=["pdf", "txt"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
    else:
        text = uploaded_file.read().decode("utf-8")

    st.subheader("🔎 AI Suggestions")
    if st.button("Get Job Recommendations & Enhancements"):
        prompt = f"""Analyze this resume and suggest 5 suitable job roles.
Also suggest 3 specific ways to improve the resume:

{text}"""
        result = call_gemini(prompt)
        st.write(result)
