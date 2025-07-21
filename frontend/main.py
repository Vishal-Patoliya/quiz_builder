# Import necessary libraries
import streamlit as st
from backend.core import run_llm  # Core function that interacts with the LLM to generate quiz
from backend.utils import validate_input
from config.constants import RETRY_ATTEMPT
from config.constants import APP_NAME
import logging # For logging events and errors

# App title
st.title(APP_NAME)

# Initialize session state to manage quiz state across reruns
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}

# User selects developer type and experience level
developer_type = st.selectbox("Choose what type of developer you are:", [
    "Android Developer",
    "iOS Developer",
    "Web Developer",
    "Backend Developer",
    "Fullstack Developer",
    "Data Scientist",
    "DevOps Engineer"
])

# User selects experience level
level = st.selectbox("Choose your experience level:", [
    "Beginner",
    "Intermediate",
    "Expert"
])

# Optional prompt to guide question generation (e.g., specific modules)
prompt = st.text_input("Add Note", placeholder="You can add the context like questions must from defined modules")

# Start quiz button
if not st.session_state.quiz_started:
    if st.button("Start Quiz"):
        with st.spinner("Setting up  questions for you ..."):
            quiz_loaded = False

            # Attempt to get valid quiz data up to 2 times
            for attempt in range(RETRY_ATTEMPT):
                logging.info(f"Attempt {attempt + 1}/{RETRY_ATTEMPT} to generate quiz.")
                # Passing the all parameters to LLM for building the query and result the output along with validate input to prevent injection attacks.
                is_valid, result = run_llm(developer_category=developer_type, experience_level=level, note=validate_input(prompt))

                # If result is valid then display the quiz section to user
                if is_valid:
                    st.session_state.quiz_data = result
                    st.session_state.quiz_started = True
                    quiz_loaded = True
                    logging.info("Quiz successfully generated and loaded.")
                    break
                else:
                    logging.warning("Received invalid quiz format. Retrying...")
                    if attempt == 0:
                        st.warning("Received invalid quiz format. Retrying...")

            # Show error if quiz could not be loaded after retries
            if not quiz_loaded:
                st.error("❌ Could not generate a valid quiz after retrying. Please try again later.")
                logging.error("Failed to generate quiz after all retry attempts.")

# Display quiz questions once started
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
        # Store selected answer index or None
        st.session_state.answers[f"q_{idx}"] = item["options"].index(selected_option) if selected_option else None

    # Submit button for quiz
    if st.button("Submit"):
        st.session_state.quiz_submitted = True
        logging.info("Quiz submitted by the user.")

# Display results after submission
if st.session_state.quiz_submitted:
    correct = 0
    total = len(st.session_state.quiz_data)
    st.subheader("📝 Results")
    logging.info("Displaying quiz results to the user.")

    # Checking each questions and answers attempted by user to display result
    for idx, item in enumerate(st.session_state.quiz_data):
        selected_index = st.session_state.answers.get(f"q_{idx}")
        correct_index = item["answer"]

        # Show feedback per question
        if selected_index == correct_index:
            st.success(f"Q{idx + 1}: Correct ✅ (Your Answer: Option {selected_index + 1})")
            correct += 1
        elif selected_index is None:
            st.warning(f"Q{idx + 1}: No answer selected ⚠️")
        else:
            st.error(
                f"Q{idx + 1}: Incorrect ❌ (Your Answer: Option {selected_index + 1}, Correct: Option {correct_index + 1})")

    # Display final score
    st.markdown(f"### 🎯 Your Score: {correct} / {total}")
    logging.info(f"User's final score: {correct}/{total}")

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG for detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    filename="quiz_app.log",  # Log file name
    filemode="a"  # Append to the log file
)
