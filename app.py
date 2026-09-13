import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate as template
from langchain_core.output_parsers import StrOutputParser
#api key import here
from langchain_google_genai import ChatGoogleGenerativeAI as chat

load_dotenv()

def main():
    if not os.getenv("GEMINI_API_KEY"):
        print("api not found, check .env file")
        return

    print("Initializing lang chain topic explorer \n")

    #gemini model, chosen -> gemini 2.0 flash
    llm=chat(model="gemini-3.1-flash-lite", temperature=0.7)

    #prompt template
    prompt = template.from_messages([
        ("system", "You are an expert tutor. Explain concepts clearly and concisely. Use markdown for formatting."),
        ("user", "Explain '{topic}' for a beginner in simple terms, then provide 5 quick quiz questions." )
    ])

    #output parsing and chain using pipe syntax
    parser = StrOutputParser()
    chain = prompt | llm | parser

    topic = input("Enter a topic you want to learn about : \n")

    if not topic.strip():
        topic = "Langchain"

    print(f"\n Generating the explaination for: {topic} ...\n")

    response= chain.invoke({"topic":topic})
    print(response)

if __name__ == "__main__":
    main()