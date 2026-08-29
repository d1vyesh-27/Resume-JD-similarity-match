"""
Semantic matching module using sentence-transformers.

IMPORTANT IMPLEMENTATION CONSTRAINT:
When implementing components in this module, first explain in comments:
1. What the concept is.
2. Why it is needed.
3. What the input is.
4. What the output is.
5. What the relevant library function does.
Do not dump unexplained code.
"""

from sentence_transformers import SentenceTransformer, util

def load_embedding_model():
    """
    1. Concept: Sentence Embeddings Model
    2. Why: Captures meaning and synonyms rather than just exact words.
    3. Input: None.
    4. Output: SentenceTransformer instance.
    5. Library: sentence_transformers.
    """
    return SentenceTransformer('BAAI/bge-small-en-v1.5')

def calculate_semantic_score(resume_text: str, jd_text: str, model=None) -> float:
    """
    1. Concept: Semantic Similarity Calculation
    2. Why: Scores the semantic overlap of the resume and JD.
    3. Input: Raw resume/JD texts and the model.
    4. Output: Cosine similarity score (float).
    5. Library: model.encode and util.cos_sim.
    """
    if not resume_text or not jd_text:
        return 0.0
        
    if model is None:
        model = load_embedding_model()
        
    embeddings1 = model.encode(resume_text, convert_to_tensor=True)
    embeddings2 = model.encode(jd_text, convert_to_tensor=True)
    
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    raw_score = float(cosine_scores[0][0])
    
    # Dense embeddings naturally cluster in a narrow cone in vector space. 
    # For bge-small, the "noise floor" for two English documents is ~0.40.
    # The "perfect match" ceiling for two highly similar but non-identical documents is ~0.85.
    # We apply a min-max scaling to stretch the [0.40, 0.85] range across [0.0, 1.0].
    baseline = 0.40
    ceiling = 0.85
    
    adjusted_score = (raw_score - baseline) / (ceiling - baseline)
    
    # Bound the score between 0.0 and 1.0 (so it can't go below 0% or above 100%)
    final_score = max(0.0, min(1.0, adjusted_score))
    
    return final_score

