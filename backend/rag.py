# rag.py → Retrieval + Augmentation + (Optional) Generation
from .search import search_employees

def rag_pipeline(query: str):
    """
    Full RAG pipeline:
    1. Retrieve relevant employees
    2. Augment with context
    3. (Optional) Generate natural language output
    """
    results = search_employees(query)
    
    # Simple template-based generation (no LLM)
    if not results:
        return "No matching employees found."
    
    response = "Here are the top candidates for your query:\n\n"
    for emp in results:
        response += (
            f"**{emp['name']}** — {emp['experience_years']} years experience\n"
            f"Skills: {', '.join(emp['skills'])}\n"
            f"Projects: {', '.join(emp['projects'])}\n"
            f"Availability: {emp['availability']}\n\n"
        )
    return response
