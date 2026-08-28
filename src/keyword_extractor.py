"""
Keyword and explicit skill extraction module for Job Descriptions and Resumes.
"""

import json
from pathlib import Path
import re

def load_skill_taxonomy() -> dict:
    taxonomy_dict = {}
    
    # Locate the tech_skills.json file relative to this script
    data_path = Path(__file__).parent.parent / "data" / "tech_skills.json"
    
    # If the file doesn't exist, return an empty dictionary to prevent crashing
    if not data_path.exists():
        return taxonomy_dict
        
    # Open the JSON file in read mode with UTF-8 encoding
    with open(data_path, 'r', encoding='utf-8') as f:
        # Parse the JSON string into a Python list of dictionaries
        skills_data = json.load(f)
        
    # Iterate over every skill object in the list
    for skill in skills_data:
        # Extract the official name (e.g., "Python")
        official_name = skill['name']
        
        # Map the lowercased official name to itself (e.g., {"python": "Python"})
        taxonomy_dict[official_name.lower()] = official_name
        
        # Use .get() to safely loop over aliases (defaults to an empty list if missing)
        for alias in skill.get('aliases', []):
            # Map the lowercased alias to the official name (e.g., {"python3": "Python"})
            taxonomy_dict[alias.lower()] = official_name
            
    return taxonomy_dict

# Load it once when the module is imported
TAXONOMY = load_skill_taxonomy()

def extract_jd_skills(jd_text: str) -> list:
    # 1. Defensive check: if the input is empty or None, return an empty list immediately.
    if not jd_text: 
        return []
        
    # 2. Lowercase the entire text because our TAXONOMY dictionary keys are all lowercase.
    jd_lower = jd_text.lower()
    
    # 3. Create a 'padded' version of the text.
    # We use regex to replace punctuation with spaces, and add a space to the very beginning and end.
    # This guarantees every word is surrounded by spaces (e.g., "Python," becomes " Python ").
    padded_jd = " " + re.sub(r'[\n\t.,;()!]', ' ', jd_lower) + " "
    
    # 4. Use a 'set' to store extracted skills. Sets automatically prevent duplicates.
    # If the JD says both "React" and "ReactJS", we only want "React" added once.
    extracted_skills = set()
    
    # 5. Loop through every search_term (e.g., "c++") and official_name (e.g., "C++") in our dictionary.
    for (search_term, official_name) in TAXONOMY.items():
        
        # 6. Check if the term exists in the text.
        # CRITICAL FIX: We MUST put spaces around the search term in the f-string: f" {search_term} "
        # Otherwise, searching for "go" will falsely trigger on the word "good".
        if f" {search_term} " in padded_jd:
            # 7. If found, add the properly capitalized official name to our set.
            extracted_skills.add(official_name)
            
    # 8. Convert the set back to a standard Python list and return it.
    return list(extracted_skills)
    

def analyze_skill_gap(jd_skills: list, resume_text: str) -> dict:
    # 1. Defensive programming
    if not resume_text or not jd_skills:
        return {"matched": [], "missing": jd_skills, "coverage": 0.0}
        
    # 2. DRY Principle: Re-use our existing function to extract skills from the resume
    resume_skills = extract_jd_skills(resume_text)
    
    # 3. Convert both lists to sets for easy mathematical comparison
    jd_set = set(jd_skills)
    resume_set = set(resume_skills)
    
    # 4. Find matches (Intersection: what is in BOTH sets)
    matched = list(jd_set.intersection(resume_set))
    
    # 5. Find missing (Difference: what is in JD, but NOT in Resume)
    missing = list(jd_set.difference(resume_set))
    
    # 6. Calculate coverage percentage (e.g., 2 / 4 skills = 0.5)
    coverage = len(matched) / len(jd_skills)
    
    return {
        "matched": matched,
        "missing": missing,
        "coverage": round(coverage, 2)
    }
    pass

