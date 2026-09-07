import os

import streamlit as st
from dotenv import load_dotenv

from memory.conversation_memory import ConversationMemory
from chains.interview_chain import InterviewChain
from chains.evaluation_chain import EvaluationChain


# Load environment variables
load_dotenv()


# -----------------------------
# Streamlit configuration
# -----------------------------

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------
# Initialize session state
# -----------------------------

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "interview_chain" not in st.session_state:
    st.session_state.interview_chain = InterviewChain(
        st.session_state.memory
    )

if "evaluation_chain" not in st.session_state:
    st.session_state.evaluation_chain = EvaluationChain()

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None


# -----------------------------
# Page Header
# -----------------------------

st.title("🎯 AI Interview Coach")

st.write(
    "Practice technical interviews with an AI interviewer "
    "and receive instant feedback on your answers."
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚙️ Interview Settings")

    role = st.selectbox(
        "Job Role",
        [
            "Java Developer",
            "React Developer",
            "Node.js Developer",
            "MERN Stack Developer",
            "Python Developer",
            "Software Developer"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.divider()

    st.subheader("📊 Interview Progress")

    question_count = len(
        st.session_state.memory.get_questions()
    )

    st.metric(
        "Questions Asked",
        question_count
    )

    if st.button(
        "🔄 Restart Interview",
        use_container_width=True
    ):

        st.session_state.memory.clear()
        st.session_state.current_question = None
        st.session_state.evaluation = None

        st.rerun()


# -----------------------------
# Check API Key
# -----------------------------

if not os.getenv("GEMINI_API_KEY"):
    st.error("GEMINI_API_KEY is missing. Please add it to your .env file.")
    st.stop()


# -----------------------------
# Start Interview
# -----------------------------

if st.session_state.current_question is None:

    st.subheader("🚀 Ready to start?")

    st.write(
        f"**Role:** {role}"
    )

    st.write(
        f"**Difficulty:** {difficulty}"
    )

    if st.button(
        "🚀 Start Interview",
        type="primary"
    ):

        with st.spinner(
            "Preparing your first question..."
        ):

            question = (
                st.session_state
                .interview_chain
                .generate_question(
                    role=role,
                    difficulty=difficulty
                )
            )

        st.session_state.current_question = question

        st.rerun()


# -----------------------------
# Interview Screen
# -----------------------------

else:

    st.subheader("💬 Interview Question")

    st.info(
        st.session_state.current_question
    )

    answer = st.text_area(
        "Your Answer",
        height=220,
        placeholder="Type your answer here..."
    )

    col1, col2 = st.columns(2)

    # -------------------------
    # Submit Answer
    # -------------------------

    with col1:

        if st.button(
            "✅ Submit Answer",
            type="primary",
            use_container_width=True
        ):

            if not answer.strip():

                st.warning(
                    "Please enter an answer first."
                )

            else:

                st.session_state.memory.add_answer(
                    answer
                )

                with st.spinner(
                    "🤖 Evaluating your answer..."
                ):

                    evaluation = (
                        st.session_state
                        .evaluation_chain
                        .evaluate_answer(
                            question=(
                                st.session_state
                                .current_question
                            ),
                            answer=answer,
                            role=role
                        )
                    )

                st.session_state.evaluation = evaluation

                st.rerun()

    # -------------------------
    # Next Question
    # -------------------------

    with col2:

        if st.button(
            "➡️ Next Question",
            use_container_width=True
        ):

            with st.spinner(
                "Generating next question..."
            ):

                question = (
                    st.session_state
                    .interview_chain
                    .generate_question(
                        role=role,
                        difficulty=difficulty
                    )
                )

            st.session_state.current_question = question
            st.session_state.evaluation = None

            st.rerun()


# -----------------------------
# Evaluation
# -----------------------------

if st.session_state.evaluation:

    st.divider()

    st.subheader("📊 AI Evaluation")

    st.markdown(
        st.session_state.evaluation
    )


# -----------------------------
# Interview History
# -----------------------------

history = (
    st.session_state
    .memory
    .get_history()
)

if history:

    st.divider()

    st.subheader("📚 Interview History")

    for index, item in enumerate(
        history,
        start=1
    ):

        with st.expander(
            f"Question {index}"
        ):

            st.write(
                item["question"]
            )

            if item["answer"]:

                st.markdown(
                    "**Your Answer:**"
                )

                st.write(
                    item["answer"]
                )