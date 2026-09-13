# 🧠 LangChain AI Topic Explainer & Quizzer

An interactive AI-powered educational application built with **LangChain (LCEL)**, **Google Gemini 3.5 Flash-Lite**, and **Streamlit**. It turns complex AI and software topics into simple, beginner-friendly explanations paired with custom quizzes to test your understanding.

---

## ✨ Features

- 🔗 **Modular LangChain Architecture**: Uses LangChain Expression Language (LCEL) to chain `ChatPromptTemplate` → `ChatGoogleGenerativeAI` → `StrOutputParser`.
- 🖥️ **Dual Interface**:
  - **Interactive Streamlit Web UI** with sliders for creativity and quiz length.
  - **Lightweight CLI Interface** for fast terminal execution.
- ⚡ **Powered by Google Gemini**: Uses the free, ultra-fast `gemini-3.5-flash-lite` model.
- 💡 **Quick Topic Presets**: One-click exploration for popular topics like *LangChain Agents*, *Vector Databases*, *RAG*, and *Neural Networks*.

---

## 📁 Repository Structure

```
.
├── app.py              # Core LangChain logic & CLI entry point
├── streamlit_app.py    # Streamlit Web UI interface
├── .env                # Environment variables (GEMINI_API_KEY)
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
pip install langchain langchain-core langchain-google-genai python-dotenv streamlit
```

### 4. Configure API Key
Create a `.env` file in the root directory and add your Google Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
*(Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)).*

---

## 🚀 Running the Application

### Option 1: Run Web UI (Streamlit)
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
