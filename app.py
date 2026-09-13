import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate as template
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI as chat

load_dotenv()

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