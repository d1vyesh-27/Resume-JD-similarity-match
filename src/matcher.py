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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import numpy as np
import scipy.sparse as sp
from functools import lru_cache
from src.preprocessing import clean_text

@lru_cache(maxsize=1)
def load_tech_skills() -> set:
    """Loads technical skills from the taxonomy to use for weighting."""
    skills_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tech_skills.json')
    skills_set = set()
    try:
        with open(skills_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # data is a list of dicts: [{"name": "Python", "aliases": ["py"]}, ...]
            for item in data:
                name = clean_text(item.get("name", ""))
                if name:
                    skills_set.add(name)
                for alias in item.get("aliases", []):
                    cleaned_alias = clean_text(alias)
                    if cleaned_alias:
                        skills_set.add(cleaned_alias)
        return skills_set
    except (FileNotFoundError, json.JSONDecodeError, AttributeError):
        return set()

def calculate_tfidf_score(resume_text: str, jd_text: str) -> float:
    """
    1. Concept: Weighted Pairwise TF-IDF Lexical Similarity
    2. Why: Establishes a baseline for exact keyword overlap, but heavily boosts recognized tech skills to silence noise.
    3. Input: Cleaned resume and JD text strings.
    4. Output: Cosine similarity score (float).
    5. Library: scikit-learn TfidfVectorizer and scipy.sparse for weighting.
    """
    if not resume_text or not jd_text:
        return 0.0
        
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), use_idf=False)
    
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    except ValueError:
        return 0.0
        
    # --- NOISE REDUCTION (Signal Boosting) ---
    skills = load_tech_skills()
    vocab = vectorizer.vocabulary_
    
    # By default every word has a weight of 1.0
    weights = np.ones(len(vocab))
    
    # If the word is a recognized skill, boost its mathematical importance by 5x
    for term, idx in vocab.items():
        if term in skills:
            weights[idx] = 5.0
            
    # Apply the weight matrix to the original TF-IDF matrix
    weight_matrix = sp.diags(weights)
    weighted_tfidf = tfidf_matrix * weight_matrix
        
    similarity = cosine_similarity(weighted_tfidf[0:1], weighted_tfidf[1:2])
    return float(similarity[0][0])
