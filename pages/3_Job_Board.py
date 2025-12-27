import streamlit as st

st.title("💼 Job Board")

jobs = [
    {"title": "Frontend Developer", "location": "Remote", "company": "TechWave"},
    {"title": "AI Research Intern", "location": "Bangalore", "company": "NeuroAI"},
    {"title": "Product Manager", "location": "Delhi", "company": "BuildVerse"},
]

for job in jobs:
    st.subheader(job["title"])
    st.write(f"📍 {job['location']} | 🏢 {job['company']}")
    if st.button(f"Apply to {job['title']}"):
        st.success(f"Application submitted for {job['title']}! (Dummy)")
