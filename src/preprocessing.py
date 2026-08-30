"""
Text preprocessing module for resumes and job descriptions.

IMPORTANT IMPLEMENTATION CONSTRAINT:
When implementing components in this module, first explain in comments:
1. What the concept is.
2. Why it is needed.
3. What the input is.
4. What the output is.
5. What the relevant library function does.
Do not dump unexplained code.
"""

import streamlit as st
import spacy
import re

@st.cache_resource
def get_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except Exception:
        from spacy.cli import download
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

TECHNICAL_ALIASES = {
    # C/C++ Family
    "c++": "cplusplus",
    "c++11": "cplusplus11",
    "c++14": "cplusplus14",
    "c++17": "cplusplus17",
    "c++20": "cplusplus20",
    "c#": "csharp",
    
    # .NET Family
    ".net": "dotnet",
    ".net core": "dotnetcore",
    "asp.net": "aspnet",
    ".net framework": "dotnetframework",
    
    # JavaScript Frameworks
    "node.js": "nodejs",
    "react.js": "reactjs",
    "angular.js": "angularjs",
    "vue.js": "vuejs",
    "express.js": "expressjs",
    
    # ML / Data Science / Hyphenated terms
    "scikit-learn": "scikitlearn",
    "machine-learning": "machinelearning",
    "deep-learning": "deeplearning",
    "artificial-intelligence": "artificialintelligence",
    "data-science": "datascience",
    "computer-vision": "computervision",
    
    # Other Punctuation
    "pl/sql": "plsql",
    "ci/cd": "cicd"
}

RESUME_JD_STOP_WORDS = {
    # Structural & Timeline
    "resume", "experience", "education", "skill", "objective", "summary", 
    "reference", "present", "month", "year", "day", "work", "company", "role",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december", "jan", "feb", "mar", "apr",
    "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec", "include", 
    "responsibilitie", "responsibility", "daily", "weekly", "monthly", "yearly", 
    "annual", "current", "currently", "past", "future", "date",
    
    # Contact & Headers
    "name", "email", "phone", "address", "linkedin", "github", "portfolio", 
    "website", "mobile", "contact", "profile", "overview", "background", 
    "history", "career", "professional", "personal", "detail", "information",
    
    # JD HR Boilerplate
    "requirement", "qualification", "candidate", "apply", "description", "duty", 
    "duties", "task", "job", "position", "salary", "benefit", "location", "hire", 
    "hiring", "opportunity", "team", "environment", "culture", "client", "customer", 
    "employer", "employee", "workplace", "equal", "veteran", "disability", 
    "gender", "race", "religion", "sexual", "orientation", "accommodate", "accommodation",
    "pay", "compensation", "bonus", "medical", "dental", "vision", "insurance",
    
    # Pure Fluff Adjectives & Action Verbs
    "strong", "excellent", "good", "great", "outstanding", "exceptional", "dynamic", 
    "motivated", "driven", "passionate", "highly", "proven", "track", "record", 
    "ability", "capable", "success", "successful", "detail-oriented", "oriented", 
    "fast-paced", "involve", "require", "demonstrate", "show", "perform", 
    "participate", "contribute", "assist", "help", "need", "seek", "look",
    
    # Generic Soft Skills / Filler
    "communication", "verbal", "written", "interpersonal", "organized", "time", 
    "deadline", "player", "worker", "self-starter", "fast-learner", "learner",
    "expert", "proficient", "familiar", "working", "knowledge", "understanding"
}

def clean_text(text: str) -> str:
    """
    1. Concept: Preprocessing Pipeline
    2. Why: Standardizes text, removes noise, and protects technical symbols.
    3. Input: Raw text string.
    4. Output: Cleaned string.
    5. Library: spaCy for tokenization/lemmatization, re for noise removal.
    """
    if not text:
        return ""
        
    cleaned_text = text.lower()
    
    # --- REGEX NOISE REMOVAL ---
    # Remove URLs
    cleaned_text = re.sub(r'http\S+|www\.\S+', '', cleaned_text)
    # Remove Emails
    cleaned_text = re.sub(r'\S+@\S+', '', cleaned_text)
    # Remove Phone Numbers
    cleaned_text = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', '', cleaned_text)
    # Remove all standalone numbers (years, quantities, metrics)
    cleaned_text = re.sub(r'\b\d+\b', '', cleaned_text)
    # Remove common bullet points and weird formatting characters
    cleaned_text = re.sub(r'[•·▪➢✓✔*]', '', cleaned_text)
    
    for original_term, safe_term in TECHNICAL_ALIASES.items():
        cleaned_text = cleaned_text.replace(original_term, safe_term)
        
    nlp = get_spacy_model()
    doc = nlp(cleaned_text)
    
    final_tokens = []
    for token in doc:
        # Filter out punctuation, standard stop words, whitespace, and custom resume/JD stop words
        if not token.is_punct and not token.is_stop and not token.is_space and not token.like_num:
            lemma = token.lemma_
            if lemma not in RESUME_JD_STOP_WORDS and len(lemma) > 1 or lemma in ['c', 'r']:
                final_tokens.append(lemma)
            
    return " ".join(final_tokens)

