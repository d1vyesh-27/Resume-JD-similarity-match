"""
Lexical matching module using TF-IDF baseline.

IMPORTANT IMPLEMENTATION CONSTRAINT:
When implementing components in this module, first explain in comments:
1. What the concept is.
2. Why it is needed.
3. What the input is.
4. What the output is.
5. What the relevant library function does.
Do not dump unexplained code.
"""

def calculate_tfidf_score(resume_text: str, jd_text: str) -> float:
    """
    Calculates a lexical similarity score using TF-IDF and cosine similarity.
    
    This serves as the traditional lexical baseline measuring actual vocabulary overlap.
    
    IMPORTANT DESIGN QUESTION (Phase 2):
    Investigate whether to fit TF-IDF on:
    A) Pairwise: Only [resume, jd]. Simple, but IDF relies on 2 documents.
    B) Domain corpus: A larger collection of job descriptions/resumes. More stable IDF, but requires a corpus.
    
    This function should:
    - Create TF-IDF representations.
    - Transform resume and JD into the same feature space.
    - Calculate cosine similarity between the vectors.
    - Return a normalized similarity score (0.0 to 1.0).
    
    Args:
        resume_text (str): Preprocessed resume text.
        jd_text (str): Preprocessed job description text.
        
    Returns:
        float: Lexical similarity score.
    """
    # Phase 2 TODO: Implement TF-IDF vectorization
    # Phase 2 TODO: Ensure both documents are vectorized in the same vocabulary space
    # Phase 3 TODO: Calculate and return cosine similarity
    pass
