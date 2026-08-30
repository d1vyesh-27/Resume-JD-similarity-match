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

import torch
from sentence_transformers import SentenceTransformer, util

def load_embedding_model():
    """
    1. Concept: Sentence Embeddings Model
    2. Why: Captures meaning and synonyms rather than just exact words.
    3. Input: None.
    4. Output: SentenceTransformer instance.
    5. Library: sentence_transformers.
    """
    return SentenceTransformer('all-MiniLM-L6-v2')

def get_chunked_embeddings(text: str, model, chunk_size=150, overlap=30):
    """
    1. Concept: Text Chunking and Mean Pooling
    2. Why: Models like all-MiniLM have a 256-token limit. Long documents get cut off.
            By chunking, embedding, and averaging, we capture the full document's meaning.
    3. Input: Raw text string, the loaded model, and chunk sizes (in words).
    4. Output: A single averaged embedding vector (Tensor) representing the entire text.
    5. Library: model.encode for vectors, torch.mean to average them.
    """
    words = text.split()
    
    # Fallback for empty text
    if not words:
        return model.encode("", convert_to_tensor=True).unsqueeze(0)
        
    chunks = []
    # Slide a window over the words, stepping by (chunk_size - overlap)
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
        
        # Stop if we've included the last word
        if i + chunk_size >= len(words):
            break
            
    # Embed all chunks at once. This returns a tensor of shape (num_chunks, embedding_size)
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    
    # Average the vectors together. dim=0 means we average across the chunks.
    document_embedding = torch.mean(chunk_embeddings, dim=0)
    
    # Return as a 2D tensor of shape (1, embedding_size) so it plays nicely with util.cos_sim
    return document_embedding.unsqueeze(0)


def calculate_semantic_score(resume_text: str, jd_text: str, model=None) -> float:
    """
    1. Concept: Semantic Similarity Calculation (with Chunking)
    2. Why: Scores the semantic overlap of the resume and JD across their entire length.
    3. Input: Raw resume/JD texts and the model.
    4. Output: Cosine similarity score (float).
    5. Library: util.cos_sim.
    """
    if not resume_text or not jd_text:
        return 0.0
        
    if model is None:
        model = load_embedding_model()
        
    # Use our new chunking function instead of directly encoding
    embeddings1 = get_chunked_embeddings(resume_text, model)
    embeddings2 = get_chunked_embeddings(jd_text, model)
    
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    raw_score = float(cosine_scores[0][0])
    
    # We use all-MiniLM-L6-v2 which has a much more isotropic vector space.
    # Unrelated documents naturally score around ~0.20 (the noise floor).
    # Highly similar matching documents score around ~0.80.
    # We apply a min-max scaling to stretch the [0.20, 0.80] range across [0.0, 1.0].
    baseline = 0.20
    ceiling = 0.80
    
    adjusted_score = (raw_score - baseline) / (ceiling - baseline)
    
    # Bound the score between 0.0 and 1.0 (so it can't go below 0% or above 100%)
    final_score = max(0.0, min(1.0, adjusted_score))
    
    return final_score

