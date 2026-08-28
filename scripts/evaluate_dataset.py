"""
Cross-Matrix Evaluation Script for Resume-JD Matching Pipeline
"""
import sys
import os
import pandas as pd
from datasets import load_dataset
from sklearn.feature_extraction.text import CountVectorizer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing import clean_text
from src.matcher import calculate_tfidf_score
from src.semantic_matcher import calculate_semantic_score
from src.keyword_extractor import extract_jd_skills, analyze_skill_gap

# --- SYNTHETIC DATASET ---
BASE_RESUMES = [
    {"Category": "Software Engineer", "Text": "Experienced Python developer with 5 years in Django and Flask. Skills: Python, SQL, C++, HTML, CSS. Built a machine learning pipeline using scikit-learn. Graduated from NIT."},
    {"Category": "Data Scientist", "Text": "Data Scientist with expertise in NLP, Pandas, and NumPy. Trained random forest and neural networks. Skills: Python, R, SQL, TensorFlow. Masters in Data Science."},
    {"Category": "Frontend Developer", "Text": "Creative Frontend Engineer. Skills: JavaScript, React, Vue.js, HTML, CSS. Built responsive web apps using Tailwind and Redux. Passionate about UI/UX."},
    {"Category": "HR Manager", "Text": "Human Resources Manager with 10 years experience. Skilled in talent acquisition, onboarding, and employee relations. Managed a team of 5 recruiters. Strong communication skills."},
    {"Category": "Sales Executive", "Text": "Top performing Sales Executive. Exceeded quota by 150%. Skills: B2B Sales, Salesforce CRM, Lead Generation, Cold Calling. Excellent negotiation skills."}
]

BASE_JDS = [
    {"Title": "Backend Python Engineer", "Text": "Looking for a Backend Engineer with strong Python and SQL skills. Experience with Django or Flask is required. C++ is a plus."},
    {"Title": "Senior Data Scientist", "Text": "We need a Data Scientist to build NLP models. Must know Python, Pandas, and Scikit-learn. Experience with neural networks is preferred."},
    {"Title": "Frontend React Developer", "Text": "Hiring a Frontend Developer to build UIs. Must be an expert in JavaScript, React, and CSS. Vue.js experience is a bonus."},
    {"Title": "HR Business Partner", "Text": "Seeking an HR Manager to handle employee relations and talent acquisition. Must have strong communication and team management skills."},
    {"Title": "Enterprise Sales Rep", "Text": "Looking for a Sales Executive to drive B2B sales. Must have experience with Salesforce CRM and lead generation. High quota expectations."}
]

resumes = BASE_RESUMES
jds = BASE_JDS

def main():
    print("Loading Synthetic Dataset to test Weighted TF-IDF...")
    results = []
    
    print(f"\nStarting 5x5 Matrix Evaluation (25 total comparisons)...")
    print("This should only take about 10 seconds.")
    
    count = 0
    for r_idx, resume_row in enumerate(resumes):
        raw_resume = resume_row['Text']
        resume_category = resume_row['Category']
        clean_res = clean_text(raw_resume)
        
        for j_idx, jd_row in enumerate(jds):
            raw_jd = jd_row['Text']
            jd_title = jd_row['Title']
            
            clean_jd_text = clean_text(raw_jd)
            jd_skills = extract_jd_skills(raw_jd)
            
            # Scores
            lexical = calculate_tfidf_score(clean_res, clean_jd_text)
            semantic = calculate_semantic_score(clean_res, clean_jd_text)
            gap = analyze_skill_gap(jd_skills, raw_resume)
            
            results.append({
                "Resume_ID": r_idx,
                "Resume_Category": resume_category,
                "JD_ID": j_idx,
                "JD_Title": jd_title,
                "Lexical_Score": round(lexical, 3),
                "Semantic_Score": round(semantic, 3),
                "Skill_Coverage": round(gap['coverage'], 3),
            })
            
            count += 1
            if count % 25 == 0:
                print(f"Computed {count}/25 matches...")
                
    # Save to CSV
    df = pd.DataFrame(results)
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "evaluation_matrix_hf.csv")
    df.to_csv(output_path, index=False)
    print(f"\n✅ Matrix Evaluation complete! Saved 625 scores to: {output_path}")
    
    print("\n💡 Open data/evaluation_matrix_hf.csv in Excel/Google Sheets to analyze the scores!")

if __name__ == "__main__":
    main()
