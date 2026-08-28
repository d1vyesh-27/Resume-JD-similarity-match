"""
Tests for the keyword and skill extraction module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.keyword_extractor import extract_jd_skills, analyze_skill_gap

def test_technical_term_extraction():
    jd = "We need a Python developer who knows SQL."
    skills = extract_jd_skills(jd)
    # The function returns the exact canonical capitalization from tech_skills.json
    assert "Python" in skills
    assert "SQL" in skills

def test_multi_word_terms():
    jd = "Experience in Machine Learning and REST APIs."
    skills = extract_jd_skills(jd)
    assert "Machine Learning" in skills
    # "REST APIs" is an alias. Our function maps it to the canonical "REST API".
    assert "REST API" in skills

def test_missing_terms_detected():
    jd_skills = ["Python", "Docker", "AWS"]
    resume = "I am a Python developer."
    gap = analyze_skill_gap(jd_skills, resume)
    
    assert "Python" in gap["matched"]
    assert "Docker" in gap["missing"]
    assert "AWS" in gap["missing"]
    assert gap["coverage"] < 1.0
