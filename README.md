# 🧠 LangChain AI Topic Explainer & Interactive Quizzer

An interactive AI-powered educational application built with **LangChain (LCEL)**, **Pydantic**, **Google Gemini 3.5 Flash-Lite**, and **Streamlit**. It turns complex AI and software topics into tailored, beginner-to-advanced explanations paired with **interactive, auto-graded quizzes** and downloadable Markdown study notes.

---

## ✨ Key Features (Phase 1)

- 🔗 **Modular LangChain Architecture**: Built using LangChain Expression Language (LCEL) with `JsonOutputParser` and `Pydantic` schemas for type-safe, structured JSON responses.
- 🎯 **Target Audience / Difficulty Selector**: Choose between **5-Year-Old (ELI5)**, **Beginner**, **Intermediate**, and **Advanced** explanation levels.
- 📝 **Interactive Auto-Graded Quiz Engine**:
  - Interactive radio-button choices for quiz questions.
  - Instant scorecard with percentage score calculation.
  - Automatic answer grading with detailed explanations for right and wrong choices.
  - Celebratory animations (`st.balloons()`) on perfect scores!
- 📥 **Export Study Notes**: Download complete lessons and quizzes as formatted `.md` files with a single click.
- ⚙️ **Customization Sliders**: Adjust model creativity (temperature) and quiz question counts (3 to 10 questions).
- 🖥️ **Dual Mode**:
  - **Interactive Streamlit Web App** (`streamlit_app.py`)
  - **Terminal CLI Interface** (`app.py`)

---

## 📁 Repository Structure

```
.
├── app.py              # LangChain LCEL chain, Pydantic schemas & CLI interface
├── streamlit_app.py    # Streamlit Web UI with interactive quiz engine & export
├── .env                # Secret environment variables (GEMINI_API_KEY)
├── .gitignore          # Git ignore rules for virtualenv and secrets
└── README.md           # Comprehensive project documentation
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
pip install langchain langchain-core langchain-google-genai pydantic python-dotenv streamlit
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
