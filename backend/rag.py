import os
from dotenv import load_dotenv
from .search import search_employees
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Choose model
MODEL_NAME = "gemini-2.0-flash"  # text model

def rag_pipeline(query: str):
    # 1. Retrieve top matching employees
    results = search_employees(query)
    if not results:
        return "No matching employees found."

    # 2. Create context from retrieved employees
    context = "\n".join([
        f"Name: {emp['name']}\nSkills: {', '.join(emp['skills'])}\nExperience: {emp['experience_years']} years\nProjects: {', '.join(emp['projects'])}\nAvailability: {emp['availability']}"
        for emp in results
    ])

    # 3. Build structured prompt
    prompt = f"""
You are an expert HR assistant. Only use the provided candidate data to answer.

The user asked: "{query}"

Candidates:
{context}

Rules:
1. Recommend only candidates who match the query requirements.
2. Mention why each candidate is a good fit.
3. Do NOT invent information not in the candidate profiles.
4. If no one matches, clearly say so.

Final Answer:
"""

    # 4. Call Gemini
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    # 5. Return clean output
    return response.text.strip() if response.text else "No response generated."
