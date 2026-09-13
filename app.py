import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate as template, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI as chat
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Automatically map GEMINI_API_KEY to GOOGLE_API_KEY for all LangChain Google modules
if os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Pydantic schemas for structured JSON output
class QuizQuestion(BaseModel):
    id: int = Field(description="Question number starting from 1")
    question: str = Field(description="The quiz question text")
    options: List[str] = Field(description="List of 4 distinct answer choices")
    answer_index: int = Field(description="0-based index of the correct option (0, 1, 2, or 3)")
    explanation: str = Field(description="Brief explanation of why the correct option is right")

class TopicLesson(BaseModel):
    topic: str = Field(description="The topic being explained")
    difficulty: str = Field(description="Target audience difficulty level")
    explanation: str = Field(description="Comprehensive explanation with analogies and markdown formatting")
    quiz: List[QuizQuestion] = Field(description="List of quiz questions")

def get_explainer_chain(temperature: float = 0.7):
    llm = chat(model="gemini-3.1-flash-lite", temperature=temperature)
    parser = JsonOutputParser(pydantic_object=TopicLesson)

    prompt = template.from_messages([
        ("system", "You are an expert tutor. Explain topics based on the requested difficulty level. "
                   "Output MUST strictly follow the JSON schema provided below:\n{format_instructions}"),
        ("user", "Explain the topic '{topic}' for a target audience level of '{difficulty}'. "
                 "Provide a clear, engaging explanation with markdown formatting, and then {num_questions} multiple choice quiz questions.")
    ])

    return prompt | llm | parser

def generate_explaination(
    topic: str, 
    difficulty: str = "Beginner", 
    temperature: float = 0.7, 
    num_questions: int = 5
) -> Dict[str, Any]:
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY not found in .env file")

    parser = JsonOutputParser(pydantic_object=TopicLesson)
    chain = get_explainer_chain(temperature=temperature)
    
    return chain.invoke({
        "topic": topic,
        "difficulty": difficulty,
        "num_questions": num_questions,
        "format_instructions": parser.get_format_instructions()
    })

# RAG Generator: Process custom document text
def generate_rag_explaination(
    document_text: str,
    topic: str = "Uploaded Document Summary",
    difficulty: str = "Beginner",
    temperature: float = 0.7,
    num_questions: int = 5
) -> Dict[str, Any]:
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY not found in .env file")

    # 1. Text Chunking
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_text(document_text)

    # --- APPROACH A: Google Cloud Embedding VectorStore (API-based) ---
    # embeddings = GoogleGenerativeAIEmbeddings(
    #     model="models/text-embedding-004",
    #     google_api_key=os.getenv("GEMINI_API_KEY")
    # )
    # vectorstore = InMemoryVectorStore.from_texts(chunks, embedding=embeddings)
    # retriever = vectorstore.as_retriever(k=4)

    # --- APPROACH B: Local In-Memory BM25 Retriever (0ms Latency, 100% Free, Offline) ---
    from langchain_community.retrievers import BM25Retriever
    retriever = BM25Retriever.from_texts(chunks, k=4)

    # 3. Retrieve Relevant Chunks
    retrieved_docs = retriever.invoke(topic)
    context_str = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # 4. Chain Execution with Document Context
    llm = chat(model="gemini-3.1-flash-lite", temperature=temperature)
    parser = JsonOutputParser(pydantic_object=TopicLesson)

    prompt = template.from_messages([
        ("system", "You are an expert tutor. Use the provided context below from the user's document to explain the topic and build quiz questions. "
                   "Output MUST strictly follow the JSON schema provided below:\n{format_instructions}\n\nContext:\n{context}"),
        ("user", "Explain the topic '{topic}' at a '{difficulty}' level based on the context. "
                 "Generate a comprehensive explanation and {num_questions} quiz questions.")
    ])

    chain = prompt | llm | parser
    return chain.invoke({
        "topic": topic,
        "difficulty": difficulty,
        "num_questions": num_questions,
        "context": context_str,
        "format_instructions": parser.get_format_instructions()
    })

# Multi-Turn Follow-Up Tutor
def ask_followup_tutor(user_query: str, history: List[Dict[str, str]], lesson_context: str) -> str:
    llm = chat(model="gemini-3.1-flash-lite", temperature=0.7)
    
    prompt = template.from_messages([
        ("system", "You are a friendly, encouraging AI tutor helping a student understand a topic. "
                   "Here is the background lesson context:\n{lesson_context}\n\n"
                   "Answer the student's question accurately using markdown."),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{query}")
    ])

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "lesson_context": lesson_context,
        "history": history,
        "query": user_query
    })

def main():
    print("Initializing LangChain Topic Explorer CLI...\n")
    topic = input("Enter a topic you want to learn about:\n")

    if not topic.strip():
        topic = "LangChain"

    print(f"\nGenerating explanation for: {topic}...\n")
    try:
        data = generate_explaination(topic)
        print("\n===== Explanation =====\n")
        print(data.get("explanation", ""))
        print("\n===== Quiz =====\n")
        for q in data.get("quiz", []):
            print(f"Q{q['id']}: {q['question']}")
            for idx, opt in enumerate(q['options']):
                print(f"  {chr(65+idx)}. {opt}")
            print(f"Correct Answer: {chr(65+q['answer_index'])}\n")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()