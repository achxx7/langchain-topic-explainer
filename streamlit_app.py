import streamlit as st
from app import generate_explaination

# Page Configuration
st.set_page_config(
    page_title="LangChain AI Topic Explainer & Quizzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 LangChain AI Topic Explainer & Quizzer")
st.caption("Learn complex AI & software concepts with interactive AI explanations, auto-graded quizzes, and exportable notes!")

# Sidebar Controls
st.sidebar.title("⚙️ Controls")

difficulty = st.sidebar.selectbox(
    "Target Audience / Difficulty",
    options=["5-Year-Old (ELI5)", "Beginner", "Intermediate", "Advanced"],
    index=1
)

temp = st.sidebar.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
num_q = st.sidebar.slider("Number of Quiz Questions", min_value=3, max_value=10, value=5, step=1)

# Session state initialization
if "lesson_data" not in st.session_state:
    st.session_state["lesson_data"] = None
if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = {}

# Preset Quick Topics
st.write("**Quick Topics:**")
col1, col2, col3, col4 = st.columns(4)
selected_topic = ""
if col1.button("🤖 LangChain Agents"):
    selected_topic = "LangChain Agents"
if col2.button("📊 Vector Databases"):
    selected_topic = "Vector Databases"
if col3.button("⚡ RAG Architecture"):
    selected_topic = "RAG Architecture"
if col4.button("🧠 Neural Networks"):
    selected_topic = "Neural Networks"

# Inputs
topic = st.text_input(
    "Enter a topic you want to learn about:",
    value=selected_topic,
    placeholder="e.g. Docker, Microservices, Quantum Computing, Transformers"
)

# Generate Button
if st.button("🚀 Explain & Generate Interactive Quiz", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic to learn about!")
    else:
        with st.spinner(f"Generating '{difficulty}' level explanation & quiz for '{topic}'..."):
            try:
                data = generate_explaination(
                    topic=topic, 
                    difficulty=difficulty, 
                    temperature=temp, 
                    num_questions=num_q
                )
                st.session_state["lesson_data"] = data
                st.session_state["quiz_submitted"] = False
                st.session_state["user_answers"] = {}
            except Exception as e:
                st.error(f"Error: {e}")

# Display Lesson & Interactive Quiz
if st.session_state["lesson_data"]:
    lesson = st.session_state["lesson_data"]

    st.divider()
    st.header(f"📖 {lesson.get('topic', topic)} ({lesson.get('difficulty', difficulty)} Level)")

    # Explanation
    st.markdown(lesson.get("explanation", ""))

    st.divider()
    st.header("📝 Interactive Quiz")
    st.write("Select your answers below and click Submit to grade your quiz!")

    quiz_list = lesson.get("quiz", [])

    # Interactive Quiz Form
    with st.form(key="quiz_form"):
        for q in quiz_list:
            q_id = q["id"]
            st.subheader(f"Question {q_id}: {q['question']}")
            
            options = q["options"]
            selected_option = st.radio(
                f"Select answer for Q{q_id}:",
                options=options,
                key=f"q_{q_id}",
                index=None
            )
            if selected_option:
                st.session_state["user_answers"][q_id] = options.index(selected_option)

        submit_quiz = st.form_submit_button("✅ Submit Quiz & Grade Answers", type="primary")

    if submit_quiz:
        st.session_state["quiz_submitted"] = True

    # Auto-Grading & Results
    if st.session_state["quiz_submitted"]:
        st.divider()
        st.subheader("🎯 Quiz Results & Scorecard")

        correct_count = 0
        total_q = len(quiz_list)

        for q in quiz_list:
            q_id = q["id"]
            user_ans = st.session_state["user_answers"].get(q_id, None)
            correct_ans = q["answer_index"]

            if user_ans == correct_ans:
                correct_count += 1
                st.success(f"**Q{q_id}: Correct!** 🎉\n\nYour Answer: {q['options'][correct_ans]}\n\n*Explanation:* {q['explanation']}")
            else:
                user_str = q['options'][user_ans] if user_ans is not None else "No answer selected"
                st.error(f"**Q{q_id}: Incorrect.** ❌\n\nYour Answer: {user_str}\n\nCorrect Answer: **{q['options'][correct_ans]}**\n\n*Explanation:* {q['explanation']}")

        score_pct = int((correct_count / total_q) * 100) if total_q > 0 else 0
        
        if score_pct == 100:
            st.balloons()
            st.success(f"🏆 **Perfect Score! {correct_count}/{total_q} ({score_pct}%)**")
        elif score_pct >= 60:
            st.info(f"👍 **Good Job! {correct_count}/{total_q} ({score_pct}%)**")
        else:
            st.warning(f"📚 **Keep Learning! Score: {correct_count}/{total_q} ({score_pct}%)**")

    # Export Notes Section
    st.divider()
    st.subheader("📥 Export Learning Notes")

    md_notes = f"# 🧠 Lesson Notes: {lesson.get('topic', topic)}\n\n"
    md_notes += f"**Difficulty:** {lesson.get('difficulty', difficulty)}\n\n"
    md_notes += f"## Explanation\n\n{lesson.get('explanation', '')}\n\n"
    md_notes += "## Quiz Questions\n\n"
    for q in quiz_list:
        md_notes += f"### Q{q['id']}: {q['question']}\n"
        for idx, opt in enumerate(q['options']):
            marker = " (Correct Answer)" if idx == q['answer_index'] else ""
            md_notes += f"- {chr(65+idx)}. {opt}{marker}\n"
        md_notes += f"\n*Explanation:* {q['explanation']}\n\n"

    st.download_button(
        label="📥 Download Notes & Quiz (.md)",
        data=md_notes,
        file_name=f"{topic.lower().replace(' ', '_')}_notes.md",
        mime="text/markdown"
    )
