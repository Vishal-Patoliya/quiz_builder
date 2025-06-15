import streamlit as st
from backend.core import run_llm
import json

st.title("🧠 Developer Quiz System")

# Initialize session state
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}

developer_type = st.selectbox("Choose what type of developer you are:", [
    "Android Developer",
    "iOS Developer",
    "Web Developer",
    "Backend Developer",
    "Fullstack Developer",
    "Data Scientist",
    "DevOps Engineer"
])

level = st.selectbox("Choose your experience level:", [
    "Beginner",
    "Intermediate",
    "Expert"
])

prompt = st.text_input("Add Note", placeholder="You can add the context like questions must from defined modules")

# Start quiz button
if not st.session_state.quiz_started:
    if st.button("Start Quiz"):
        with st.spinner("Setting up  questions for you ..."):
            generated_response = run_llm(developer_category=developer_type, experience_level=level, note=prompt)
            st.session_state.quiz_data = json.loads(
                generated_response.message.get("content").__getitem__(0).get("text"))
        st.session_state.quiz_started = True

# Display Quiz
if st.session_state.quiz_started:
    st.subheader("📋 Quiz Questions")

    for idx, item in enumerate(st.session_state.quiz_data):
        selected_option = st.radio(
            f"Q{idx + 1}: {item['question']}",
            item["options"],
            index=None,
            key=f"q_{idx}",
            format_func=lambda x: f"{x}"
        )
        st.session_state.answers[f"q_{idx}"] = item["options"].index(selected_option) if selected_option else None

    # Submit Button
    if st.button("Submit"):
        st.session_state.quiz_submitted = True

# Show Result
if st.session_state.quiz_submitted:
    correct = 0
    total = len(st.session_state.quiz_data)
    st.subheader("📝 Results")

    for idx, item in enumerate(st.session_state.quiz_data):
        selected_index = st.session_state.answers.get(f"q_{idx}")
        correct_index = item["answer"]  # Assuming this is the correct index (e.g., 0, 1, 2, etc.)

        if selected_index == correct_index:
            st.success(f"Q{idx + 1}: Correct ✅ (Your Answer: Option {selected_index + 1})")
            correct += 1
        elif selected_index is None:
            st.warning(f"Q{idx + 1}: No answer selected ⚠️")
        else:
            st.error(
                f"Q{idx + 1}: Incorrect ❌ (Your Answer: Option {selected_index + 1}, Correct: Option {correct_index + 1})")

    st.markdown(f"### 🎯 Your Score: {correct} / {total}")
