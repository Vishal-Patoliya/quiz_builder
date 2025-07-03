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

def is_valid_json(json_string):
    try:
        data = json.loads(json_string)
        return True, data  # It's valid JSON
    except json.JSONDecodeError as e:
        return False, str(e)  # Not valid, return error

# Start quiz button
if not st.session_state.quiz_started:
    if st.button("Start Quiz"):
        with st.spinner("Setting up  questions for you ..."):
            quiz_loaded = False

            for attempt in range(2):  # Try up to 2 times
                is_valid, result = run_llm(developer_category=developer_type, experience_level=level, note=prompt)

                if is_valid:
                    st.session_state.quiz_data = result
                    st.session_state.quiz_started = True
                    quiz_loaded = True
                    break
                else:
                    if attempt == 0:
                        st.warning("Received invalid quiz format. Retrying...")

            if not quiz_loaded:
                st.error("❌ Could not generate a valid quiz after retrying. Please try again later.")

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