"""
Tests for the lexical TF-IDF matcher module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.matcher import calculate_tfidf_score

def test_identical_documents():
    text = "python developer experience"
    score = calculate_tfidf_score(text, text)
    assert score > 0.99

def test_unrelated_documents():
    resume = "chef cooking food restaurant"
    jd = "python developer software engineering"
    score = calculate_tfidf_score(resume, jd)
    assert score < 0.1

def test_empty_input():
    assert calculate_tfidf_score("", "python") == 0.0
    assert calculate_tfidf_score("python", "") == 0.0
    assert calculate_tfidf_score("", "") == 0.0

def test_same_feature_space():
    # Vectors should be aligned; partial overlap should return a medium score
    resume = "python django developer"
    jd = "python developer"
    score = calculate_tfidf_score(resume, jd)
    assert 0.3 < score < 0.99
