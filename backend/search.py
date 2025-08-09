import re
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

def parse_query_for_filters(query: str):
    """
    Extract required skills and minimum experience from the query.
    """
    exp_match = re.search(r'(\d+)\s*(?:year|years)', query, re.IGNORECASE)
    required_experience = int(exp_match.group(1)) if exp_match else None

    # Rough skills extraction: split by common separators
    skills = [
        word.strip().lower()
        for word in re.split(r'[,/ ]+', query)
        if len(word) > 1
    ]
    return skills, required_experience

def search_employees(query: str, top_k: int = 3):
    """
    Flexible semantic + filter search.
    Matches if employee has ANY skill or meets experience requirement.
    """
    skills_required, exp_required = parse_query_for_filters(query)

    # Step 1: Semantic search
    query_emb = get_embeddings([query])
    distances, indices = index.search(query_emb, top_k * 5)  # more candidates for filtering

    results = []
    for i in indices[0]:
        emp = employees_data[i]
        emp_skills_lower = [s.lower() for s in emp["skills"]]

        # Flags
        skill_match = False
        exp_match = False

        # Experience check
        if exp_required is not None:
            exp_match = emp["experience_years"] >= exp_required

        # Skills check
        if skills_required:
            skill_match = any(skill in emp_skills_lower for skill in skills_required if skill)

        # Include if matches ANY
        if skill_match or exp_match:
            results.append(emp)

        if len(results) >= top_k:
            break

    # Step 2: Fallback to top semantic matches if no results
    if not results:
        for i in indices[0][:top_k]:
            results.append(employees_data[i])

    return results
