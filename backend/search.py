# search.py → handles FAISS index creation and retrieval
import faiss
import json
from pathlib import Path
from .embeddings import get_embeddings

# Load dataset
DATA_PATH = Path(__file__).parent / "data" / "employees.json"
with open(DATA_PATH, "r") as f:
    employees_data = json.load(f)["employees"]

# Prepare employee descriptions for embedding
employee_texts = [
    f"{emp['name']} Skills: {', '.join(emp['skills'])} "
    f"Experience: {emp['experience_years']} years. "
    f"Projects: {', '.join(emp['projects'])}. "
    f"Availability: {emp['availability']}."
    for emp in employees_data
]

# Create embeddings
embeddings = get_embeddings(employee_texts)

# Create FAISS index
dim = len(embeddings[0])
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

def search_employees(query: str, top_k: int = 3):
    """
    Search for employees matching the query using vector similarity.
    """
    query_emb = get_embeddings([query])
    distances, indices = index.search(query_emb, top_k)
    results = [employees_data[i] for i in indices[0]]
    return results
