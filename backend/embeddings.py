# embeddings.py → handles loading the embedding model and generating vectors

from sentence_transformers import SentenceTransformer

# Load model once globally (avoids reloading for each request)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """
    Convert a string into a dense vector embedding.
    """
    return model.encode([text], convert_to_tensor=False)[0]

def get_embeddings(texts: list[str]):
    """
    Convert a list of strings into embeddings.
    """
    return model.encode(texts, convert_to_tensor=False)
