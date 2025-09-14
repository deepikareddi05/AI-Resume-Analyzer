# semantic.py
from sentence_transformers import SentenceTransformer, util

# load once
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def semantic_similarity(a_text, b_text):
    """
    Returns a similarity score between 0..1
    """
    if not a_text or not b_text:
        return 0.5  # neutral if missing
    model = get_model()
    a_emb = model.encode(a_text, convert_to_tensor=True)
    b_emb = model.encode(b_text, convert_to_tensor=True)
    score = util.cos_sim(a_emb, b_emb).item()
    # cos_sim between -1..1 -> normalize to 0..1
    return max(0.0, min(1.0, (score + 1) / 2))
