## **HR CHATBOT**

## **1️⃣ Employee Dataset (Sample)**

We’ll make **at least 15 employees** with diverse skills, projects, and availability.
You can save this in `employees.json` for quick loading.


## **2️⃣ RAG Architecture**

We’ll use **embedding-based retrieval** + optional **LLM** for natural responses.

### **Flow**

1. **User Query →** `"Find Python developers with 3+ years experience"`
2. **Embedding Model →** Convert query & employee profiles into vector embeddings.
3. **Vector Search →** FAISS (or Chroma) finds top matching employees.
4. **Augmentation →** Retrieve their profile details.
5. **Generation →** (Optional) LLM formats a friendly HR-style answer.

---

### **Components**

#### **a) Embedding Model**

* **Option 1:** `text-embedding-3-small` (OpenAI) – Cloud, accurate, paid.
* **Option 2:** `all-MiniLM-L6-v2` (HuggingFace, free) – Good for local dev.

#### **b) Vector Store**

* **FAISS**: Fast, lightweight, local vector search.
* Store employee embeddings once at startup.

#### **c) Backend**

* **FastAPI**

  * `POST /chat` → Accepts query, runs RAG pipeline, returns answer.
  * `GET /employees/search` → Filter employees by skills, experience, availability.

#### **d) Frontend**

* **Option 1:** Streamlit (fastest for demo)
* **Option 2:** HTML + JS chat UI

---

### **Directory Structure**

```
hr_chatbot/
│── backend/
│   ├── main.py             # FastAPI app
│   ├── data/
│   │   └── employees.json  # Sample dataset
│   ├── rag.py              # Retrieval & generation logic
│   ├── embeddings.py       # Embedding functions
│   ├── search.py           # FAISS search
│   └── requirements.txt
│
│── frontend/
│   └── app.py              # Streamlit chat UI
│
└── README.md
