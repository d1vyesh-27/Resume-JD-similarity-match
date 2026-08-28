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

import spacy
import re

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

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
    
    for original_term, safe_term in TECHNICAL_ALIASES.items():
        cleaned_text = cleaned_text.replace(original_term, safe_term)
        
    doc = nlp(cleaned_text)
    
    final_tokens = []
    for token in doc:
        if not token.is_punct and not token.is_stop and not token.is_space:
            # Fixed the bug from the experiment notebook: token.lemma -> token.lemma_
            final_tokens.append(token.lemma_)
            
    return " ".join(final_tokens)

