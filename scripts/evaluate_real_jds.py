import sys
import os
import pandas as pd
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing import clean_text
from src.matcher import calculate_tfidf_score
from src.semantic_matcher import calculate_semantic_score
from src.keyword_extractor import extract_jd_skills, analyze_skill_gap

# Use the Software Engineer resume for testing
TEST_RESUME = "Experienced Python developer with 5 years in Django and Flask. Skills: Python, SQL, C++, HTML, CSS. Built a machine learning pipeline using scikit-learn. Graduated from NIT."

def main():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'job_title_des.csv')
    df = pd.read_csv(csv_path)
    
    # Drop rows with missing values
    df = df.dropna(subset=['Job Title', 'Job Description'])
    
    # Sample 5 random rows
    sample_df = df.sample(5, random_state=42)
    
    clean_res = clean_text(TEST_RESUME)
    
    print("Evaluating Test Resume (Python/Django Software Engineer) against 5 random real-world JDs...\n")
    print("-" * 80)
    
    for idx, row in sample_df.iterrows():
        jd_title = row['Job Title']
        raw_jd = row['Job Description']
        
        clean_jd = clean_text(raw_jd)
        jd_skills = extract_jd_skills(raw_jd)
        
        lexical = calculate_tfidf_score(clean_res, clean_jd)
        semantic = calculate_semantic_score(clean_res, clean_jd)
        gap = analyze_skill_gap(jd_skills, TEST_RESUME)
        
        # Calculate Final Weighted Score (Semantic 50%, Skill 35%, Lexical 15%)
        # If no skills found in JD, shift weights: Semantic 80%, Lexical 20%
        if len(jd_skills) > 0:
            final_score = (semantic * 0.50) + (gap['coverage'] * 0.35) + (lexical * 0.15)
        else:
            final_score = (semantic * 0.80) + (lexical * 0.20)
            
        print(f"JD Title: {jd_title}")
        print(f"Extracted JD Skills: {jd_skills}")
        print(f"Scores:")
        print(f"  - Lexical (TF-IDF): {lexical:.3f}")
        print(f"  - Semantic (Cos Sim): {semantic:.3f}")
        print(f"  - Skill Coverage: {gap['coverage']:.3f} ({len(gap['matched'])}/{len(gap['matched']) + len(gap['missing'])})")
        print(f"  - **Final Weighted Score: {final_score:.3f}**")
        print("-" * 80)

if __name__ == '__main__':
    main()
