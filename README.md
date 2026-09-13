# 🧠 LangChain AI Tutor & Document RAG Explainer

An interactive, multi-mode AI learning platform built with **LangChain (LCEL)**, **Pydantic**, **BM25 RAG Retrieval**, **Google Gemini 3.1 Flash-Lite**, and **Streamlit**. 

Learn any software or AI topic from scratch, or upload your own PDF/TXT documents (textbooks, notes, research papers) to generate tailored explanations, auto-graded interactive quizzes, and engage in multi-turn follow-up Q&A tutoring!

---

## ✨ Features

### 📖 1. Dual Learning Modes
- **Topic Mode**: Enter any topic (e.g. *Docker*, *Microservices*, *Transformers*) or click preset quick chips.
- **Document Upload (RAG) Mode**: Upload custom **PDF** or **TXT** files. The app chunks text (`RecursiveCharacterTextSplitter`), performs local BM25 context retrieval, and grounds all explanations & quizzes directly in your document!

### 🎯 2. Audience & Difficulty Customization
Select target difficulty levels: **5-Year-Old (ELI5)**, **Beginner**, **Intermediate**, or **Advanced**.

### 📝 3. Interactive Auto-Graded Quiz Engine
- Interactive radio-button quiz options.
- Instant scorecard calculation (% score).
- Detailed answer explanations for correct and incorrect choices.
- Celebratory animations (`st.balloons()`) on 100% scores!

### 💬 4. Multi-Turn Follow-Up AI Tutor Chat
- Conversational chat interface (`st.chat_input` & `st.chat_message`) at the bottom of the screen.
- Ask follow-up questions about the lesson or quiz (e.g., *"Can you explain step 2 again with a code example?"*).
- Uses LangChain's `MessagesPlaceholder` to maintain full conversational context.

### 📥 5. Export Study Notes
- Download complete generated lessons and quizzes as formatted `.md` markdown files with a single click.

---

## 📁 Repository Structure

```
.
├── app.py              # LangChain LCEL chains, Pydantic schemas, RAG BM25 retriever & CLI
├── streamlit_app.py    # Streamlit Web UI with RAG uploader, quiz engine & chat tutor
├── .env                # Secret environment variables (GEMINI_API_KEY)
├── .gitignore          # Git ignore rules for virtualenv and secrets
└── README.md           # Project documentation
```

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone git@github-second:achxx7/langchain-topic-explainer.git
cd langchain-topic-explainer
```

### 2. Create & Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install langchain langchain-core langchain-community langchain-google-genai langchain-text-splitters pydantic python-dotenv streamlit pypdf rank_bm25
```

### 4. Configure API Key
Create a `.env` file in the root directory and add your Google Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
*(Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)).*

---

## 🚀 Running the Application

### Option 1: Run Interactive Web UI (Streamlit)
```bash
streamlit run streamlit_app.py
```
*(Opens automatically at `http://localhost:8501`).*

### Option 2: Run Terminal CLI
```bash
python3 app.py
```

---

## 📜 License
MIT License
