import streamlit as st
from app import generate_explaination

# Page setup
st.set_page_config(
    page_title="LangChain Topic Explainer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 LangChain AI Topic Explainer")
st.caption("Learn complex AI & software concepts with interactive AI explanations and quizzes!")

# Sidebar Controls
st.sidebar.title("Controls for you")
temp = st.sidebar.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
num_q = st.sidebar.slider("Number of Questions", min_value=3, max_value=10, value=5, step=1)

# Initialize default topic before checking buttons
selected_topic = ""

# Quick Buttons
st.write("Quick Topics:")
col1, col2, col3, col4 = st.columns(4)
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
    placeholder="e.g. Docker, Microservices, Quantum Computing"
)

# Submit Button
if st.button("🚀 Explain & Generate Quiz", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic to learn about!")
    else:
        with st.spinner(f"Generating explanation for '{topic}'..."):
            try:
                result = generate_explaination(topic=topic, temperature=temp, num_questions=num_q)
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")
