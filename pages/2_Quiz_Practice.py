import streamlit as st
import re
from utils.gemini_api import call_gemini

st.title("🧠 Practice Quiz")

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.correct_answers = {}
    st.session_state.user_answers = {}
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.submitted = False

# Step 1: Generate quiz from Gemini
if not st.session_state.questions:
    topic = st.text_input("Enter a topic (e.g. Python, HR, Java)")
    if st.button("🎯 Generate Quiz"):
        prompt = f"""
        Create a 5-question multiple choice quiz on the topic: {topic}.
        Each question should have 4 options labeled A-D.
        Format:
        1. Question text
        A. Option A
        B. Option B
        C. Option C
        D. Option D

        Answers:
        1. A
        2. B
        ...
        """
        quiz_text = call_gemini(prompt)

        # Split into question and answer sections
        split_text = quiz_text.split("Answers:")
        question_part = split_text[0].strip()
        answer_part = split_text[1].strip() if len(split_text) > 1 else ""

        # Extract answer keys
        answers = {}
        answer_lines = answer_part.strip().split("\n")
        for line in answer_lines:
            if "." in line:
                qnum, ans = line.strip().split(".")
                answers[int(qnum.strip()) - 1] = ans.strip().upper()

        # Extract questions and options
        question_blocks = re.findall(r"\d+\..*?(?=\n\d+\.|$)", question_part, re.DOTALL)
        questions = []
        for block in question_blocks:
            lines = block.strip().split("\n")
            q_text = lines[0].strip()
            options = [line.strip() for line in lines[1:] if line.strip().startswith(("A.", "B.", "C.", "D."))]
            if options:
                questions.append({
                    "question": q_text,
                    "options": options
                })

        st.session_state.questions = questions
        st.session_state.correct_answers = answers
        st.experimental_rerun()

# Step 2: Show one question at a time
if st.session_state.questions and not st.session_state.submitted:
    q_idx = st.session_state.q_index
    current_q = st.session_state.questions[q_idx]

    st.markdown(f"### Question {q_idx + 1}")
    st.write(current_q["question"])
    answer = st.radio("Choose an option:", current_q["options"], key=f"q{q_idx}")

    if st.button("Next ➡️"):
        if answer:
            st.session_state.user_answers[q_idx] = answer
            st.session_state.q_index += 1
            if st.session_state.q_index >= len(st.session_state.questions):
                st.session_state.submitted = True
            st.experimental_rerun()
        else:
            st.warning("⚠️ Please select an option before moving to the next question.")

# Step 3: Show final score
if st.session_state.submitted:
    st.markdown("## 🧾 Quiz Results")
    score = 0
    for idx, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.user_answers.get(idx, "Not Answered")
        correct_letter = st.session_state.correct_answers.get(idx, "?")
        correct_option = next((opt for opt in q["options"] if opt.startswith(correct_letter + ".")), "Unknown")

        is_correct = user_ans and user_ans.startswith(correct_letter)
        if is_correct:
            score += 1

        st.markdown(f"**Q{idx + 1}:** {'✅' if is_correct else '❌'}")
        st.markdown(f"Your answer: `{user_ans}`  \nCorrect answer: `{correct_option}`")

    st.success(f"🎉 Final Score: {score} / {len(st.session_state.questions)}")

    if st.button("🔁 Try Again"):
        for key in ["questions", "correct_answers", "user_answers", "q_index", "score", "submitted"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()
