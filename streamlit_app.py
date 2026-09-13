import streamlit as st
from pypdf import PdfReader
from app import generate_explaination, generate_rag_explaination, ask_followup_tutor

# Page Configuration
st.set_page_config(
    page_title="LangChain AI Tutor & RAG Explainer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 LangChain AI Tutor & Document RAG Explainer")
st.caption("Learn topics from scratch OR upload your own PDFs/TXT files with interactive quizzes and follow-up chat!")

# Sidebar Controls
st.sidebar.title("⚙️ Controls")

mode = st.sidebar.radio("Learning Mode", ["Topic Mode", "Document Upload (RAG) Mode"])

difficulty = st.sidebar.selectbox(
    "Target Audience / Difficulty",
    options=["5-Year-Old (ELI5)", "Beginner", "Intermediate", "Advanced"],
    index=1
)

temp = st.sidebar.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
num_q = st.sidebar.slider("Number of Quiz Questions", min_value=3, max_value=10, value=5, step=1)

# Session State Initialization
if "lesson_data" not in st.session_state:
    st.session_state["lesson_data"] = None
if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = {}
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Main Input Section
uploaded_file_text = ""
topic = ""

if mode == "Document Upload (RAG) Mode":
    st.subheader("📄 Upload Document (PDF / TXT)")
    uploaded_file = st.file_uploader("Upload your textbook, notes, or paper:", type=["pdf", "txt"])
    
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            pdf_reader = PdfReader(uploaded_file)
            uploaded_file_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        else:
            uploaded_file_text = uploaded_file.read().decode("utf-8")
        
        st.success(f"✅ Processed {len(uploaded_file_text)} characters from '{uploaded_file.name}'")

    topic = st.text_input("Focus area or topic in document (optional):", value="Main Summary & Key Concepts")

else:
    # Topic Mode
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

    topic = st.text_input("Enter a topic you want to learn about:", value=selected_topic, placeholder="e.g. Docker, Microservices, Quantum Computing")

# Generate Button
if st.button("🚀 Generate Lesson & Interactive Quiz", type="primary"):
    if mode == "Document Upload (RAG) Mode" and not uploaded_file_text.strip():
        st.warning("Please upload a PDF or TXT file first!")
    elif mode == "Topic Mode" and not topic.strip():
        st.warning("Please enter a topic to learn about!")
    else:
        with st.spinner("Generating lesson & quiz with LangChain..."):
            try:
                if mode == "Document Upload (RAG) Mode":
                    data = generate_rag_explaination(
                        document_text=uploaded_file_text,
                        topic=topic if topic.strip() else "Document Summary",
                        difficulty=difficulty,
                        temperature=temp,
                        num_questions=num_q
                    )
                else:
                    data = generate_explaination(
                        topic=topic,
                        difficulty=difficulty,
                        temperature=temp,
                        num_questions=num_q
                    )

                st.session_state["lesson_data"] = data
                st.session_state["quiz_submitted"] = False
                st.session_state["user_answers"] = {}
                st.session_state["chat_history"] = []
            except Exception as e:
                st.error(f"Error: {e}")

# Display Lesson & Interactive Quiz
if st.session_state["lesson_data"]:
    lesson = st.session_state["lesson_data"]

    st.divider()
    st.header(f"📖 {lesson.get('topic', topic)} ({lesson.get('difficulty', difficulty)} Level)")
    st.markdown(lesson.get("explanation", ""))

    st.divider()
    st.header("📝 Interactive Quiz")
    quiz_list = lesson.get("quiz", [])

    with st.form(key="quiz_form"):
        for q in quiz_list:
            q_id = q["id"]
            st.subheader(f"Question {q_id}: {q['question']}")
            options = q["options"]
            selected_option = st.radio(f"Select answer for Q{q_id}:", options=options, key=f"q_{q_id}", index=None)
            if selected_option:
                st.session_state["user_answers"][q_id] = options.index(selected_option)

        submit_quiz = st.form_submit_button("✅ Submit Quiz & Grade Answers", type="primary")

    if submit_quiz:
        st.session_state["quiz_submitted"] = True

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

    # Follow-Up Chat Bot Section
    st.divider()
    st.header("💬 Follow-Up AI Tutor Chat")
    st.write("Have questions about this lesson or quiz? Ask the AI Tutor below!")

    # Display chat history
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if user_query := st.chat_input("Ask a follow-up question (e.g., 'Can you explain step 2 again with an example?')..."):
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("AI Tutor thinking..."):
                try:
                    formatted_history = [
                        ("user" if m["role"] == "user" else "assistant", m["content"])
                        for m in st.session_state["chat_history"][:-1]
                    ]
                    
                    answer = ask_followup_tutor(
                        user_query=user_query,
                        history=formatted_history,
                        lesson_context=lesson.get("explanation", "")
                    )
                    st.markdown(answer)
                    st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error: {e}")
