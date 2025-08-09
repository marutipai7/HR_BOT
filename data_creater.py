import json
import random
from faker import Faker

fake = Faker()

# Skill pools
skill_categories = {
    "python": ["Python", "Django", "Flask", "FastAPI", "Pandas", "NumPy", "Scikit-learn", "PyTorch", "TensorFlow"],
    "frontend": ["React", "Vue.js", "Angular", "JavaScript", "TypeScript", "Next.js"],
    "backend": ["Java", "Spring Boot", "Kotlin", "Node.js", "Express", "C#", ".NET"],
    "cloud": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform"],
    "data": ["SQL", "PostgreSQL", "MySQL", "MongoDB", "Data Science", "NLP"],
    "security": ["Cybersecurity", "Network Security", "Penetration Testing", "Ethical Hacking"],
    "design": ["UI/UX Design", "Figma", "Adobe XD", "Photoshop"],
    "devops": ["Jenkins", "CI/CD", "Prometheus", "Grafana", "GitLab CI"]
}

# Projects mapped by skills
project_ideas = {
    "Python": ["Job Portal API", "Inventory Management System", "Chatbot Service"],
    "Django": ["Healthcare Prediction API", "Learning Management System"],
    "React": ["E-commerce Platform", "Social Media Dashboard"],
    "AWS": ["Cloud Migration Project", "Serverless Data Pipeline"],
    "Java": ["Banking Transaction System", "Loan Approval Engine"],
    "Machine Learning": ["Fraud Detection Model", "Customer Segmentation Tool"],
    "UI/UX Design": ["Mobile Banking App Design", "E-learning Platform UI"],
    "Cybersecurity": ["Firewall Optimization", "Bank Security Audit"],
    "Data Science": ["Sales Forecasting System", "Sentiment Analysis Tool"]
}

availability_options = ["available", "busy"]

def generate_employee(id_counter):
    # Pick random name
    name = fake.name()

    # Random skills (fix: sample size <= available skills)
    num_skill_groups = random.randint(1, 3)
    chosen_groups = random.sample(list(skill_categories.keys()), num_skill_groups)
    available_skills = [skill for group in chosen_groups for skill in skill_categories[group]]
    sample_size = min(len(available_skills), random.randint(2, 5))
    skills = random.sample(available_skills, sample_size)

    # Experience
    experience_years = random.randint(1, 15)

    # Projects based on skills
    related_projects = []
    for skill in skills:
        if skill in project_ideas:
            related_projects.extend(random.sample(project_ideas[skill], k=min(2, len(project_ideas[skill]))))
    if not related_projects:  # fallback if no mapped project
        related_projects = [fake.sentence(nb_words=3) for _ in range(2)]

    # Availability
    availability = random.choice(availability_options)

    return {
        "id": id_counter,
        "name": name,
        "skills": skills,
        "experience_years": experience_years,
        "projects": related_projects,
        "availability": availability
    }

# Generate dataset
employees = [generate_employee(i+1) for i in range(2000)]

# Save to JSON
with open("employees_2000.json", "w", encoding="utf-8") as f:
    json.dump({"employees": employees}, f, indent=2)

print("✅ Generated 2000 employee records → employees_2000.json")
