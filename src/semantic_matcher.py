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

def load_embedding_model():
    """
    Loads a pretrained sentence-transformer model.
    
    IMPORTANT: 
    - Model loading should not happen repeatedly for every button click in Streamlit.
    - Design this so Streamlit can cache the model using @st.cache_resource.
    - Model selection should prioritize a lightweight pretrained model (e.g., all-MiniLM-L6-v2) 
      balancing semantic quality, model size, and inference speed for deployment.
    
    Returns:
        Model object.
    """
    # Phase 4 TODO: Import sentence_transformers and load a lightweight model
    pass

def calculate_semantic_score(resume_text: str, jd_text: str, model=None) -> float:
    """
    Calculates a semantic similarity score using pretrained sentence embeddings.
    
    This measures meaning overlap (e.g., "Led a cross-functional team" vs "Experience in team leadership").
    
    This function should:
    - Encode resume and JD using the loaded model to generate embeddings.
    - Calculate cosine similarity between the embeddings.
    - Return a normalized semantic similarity score (0.0 to 1.0).
    
    Args:
        resume_text (str): Preprocessed resume text.
        jd_text (str): Preprocessed job description text.
        model: Preloaded sentence-transformer model.
        
    Returns:
        float: Semantic similarity score.
    """
    # Phase 4 TODO: Generate embeddings for both texts
    # Phase 4 TODO: Calculate and return cosine similarity
    pass
