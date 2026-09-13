import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate as template
from langchain_core.output_parsers import StrOutputParser
#api key import here
from langchain_google_genai import ChatGoogleGenerativeAI as chat

load_dotenv()

def get_explainer_chain(temperature: float=0.7, num_questions: int = 5):

    #gemini model, chosen -> gemini 2.0 flash
    llm=chat(model="gemini-3.1-flash-lite", temperature=temperature)

    #prompt template
    prompt = template.from_messages([
        ("system", "You are an expert tutor. Explain concepts clearly and concisely. Use markdown for formatting."),
        ("user", "Explain '{topic}' for a beginner in simple terms, then provide {num_questions} quick quiz questions." )
    ])

    #output parsing and chain using pipe syntax
    parser = StrOutputParser()
    return prompt | llm | parser

#generate explaination function
def generate_explaination(topic: str, temperature: float = 0.7, num_questions: int = 5) -> str:   
    
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Gemini API not found in env")

    chain=get_explainer_chain(temperature=temperature, num_questions=num_questions)
    
    return chain.invoke({"topic":topic, "num_questions":num_questions})

#driver codeeeee
def main():
    print("Initializing the langchain topic explorer .... \n")

    topic = input("Enter a topic you wnt to learn about: \n")

    if not topic.strip():
        topic = "Langchain"

    print("\n Generating explaination for: {topic} .... \n")
    try:
        response = generate_explaination(topic)
        print("\n===== Explanation =====\n")
        print(response)
        print("\n=======================")

    except ValueError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

#driver code
if __name__ == "__main__":
    main()