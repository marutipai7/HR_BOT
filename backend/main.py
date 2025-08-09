# main.py → FastAPI backend for HR chatbot
from fastapi import FastAPI, Query
from pydantic import BaseModel
from .rag import rag_pipeline
from .search import search_employees

app = FastAPI(title="HR Resource Query Chatbot")

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "HR Resource Query Chatbot API is running"}

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Accepts a natural language query and returns HR recommendations.
    """
    result = rag_pipeline(request.query)
    return {"response": result}

@app.get("/employees/search")
def employee_search(
    skill: str = Query(None),
    min_experience: int = Query(0),
    availability: str = Query(None)
):
    """
    Basic filtering search (not semantic) — useful for direct filtering.
    """
    results = []
    for emp in search_employees(skill if skill else ""):
        if skill and skill not in emp["skills"]:
            continue
        if emp["experience_years"] < min_experience:
            continue
        if availability and emp["availability"] != availability:
            continue
        results.append(emp)
    return {"employees": results}
