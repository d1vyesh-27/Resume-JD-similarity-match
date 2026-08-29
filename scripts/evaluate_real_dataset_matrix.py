import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing import clean_text
from src.matcher import calculate_tfidf_score
from src.semantic_matcher import calculate_semantic_score
from src.keyword_extractor import extract_jd_skills, analyze_skill_gap

def main():
    print("Loading datasets...")
    resume_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Resume.csv')
    jd_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'job_title_des.csv')
    
    resume_df = pd.read_csv(resume_csv_path)
    jd_df = pd.read_csv(jd_csv_path)
    
    jd_df = jd_df.dropna(subset=['Job Title', 'Job Description'])
    resume_df = resume_df.dropna(subset=['Resume_str', 'Category'])
    
    # Select 1 matching pair (IT / Software)
    it_resumes = resume_df[resume_df['Category'] == 'INFORMATION-TECHNOLOGY']
    it_resume = it_resumes.sample(1, random_state=42)
    
    it_jds = jd_df[jd_df['Job Title'].str.contains('Developer|Engineer|IT', case=False, na=False)]
    it_jd = it_jds.sample(1, random_state=42)
    
    # Select 4 random non-IT pairs
    other_resumes = resume_df[resume_df['Category'] != 'INFORMATION-TECHNOLOGY'].sample(4, random_state=42)
    other_jds = jd_df[~jd_df['Job Title'].str.contains('Developer|Engineer|IT', case=False, na=False)].sample(4, random_state=42)
    
    # Combine
    sample_resumes = pd.concat([it_resume, other_resumes])
    sample_jds = pd.concat([it_jd, other_jds])
    
    results = []
    
    print("\nStarting 5x5 Matrix Evaluation on Real Datasets...")
    count = 0
    for r_idx, r_row in sample_resumes.iterrows():
        resume_cat = r_row['Category']
        raw_resume = r_row['Resume_str']
        clean_res = clean_text(raw_resume)
        
        for j_idx, j_row in sample_jds.iterrows():
            jd_title = j_row['Job Title']
            raw_jd = j_row['Job Description']
            
            clean_jd_text = clean_text(raw_jd)
            jd_skills = extract_jd_skills(raw_jd)
            
            lexical = calculate_tfidf_score(clean_res, clean_jd_text)
            semantic = calculate_semantic_score(clean_res, clean_jd_text)
            gap = analyze_skill_gap(jd_skills, raw_resume)
            coverage = gap['coverage']
            
            if len(jd_skills) > 0:
                final_score = (semantic * 0.50) + (coverage * 0.35) + (lexical * 0.15)
            else:
                final_score = (semantic * 0.80) + (lexical * 0.20)
                
            results.append({
                "Resume_Category": resume_cat,
                "JD_Title": jd_title,
                "Lexical": round(lexical, 3),
                "Semantic": round(semantic, 3),
                "Coverage": round(coverage, 3),
                "Final_Score": round(final_score, 3)
            })
            count += 1
            if count % 5 == 0:
                print(f"Computed {count}/25...")
                
    df_results = pd.DataFrame(results)
    
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "real_evaluation_matrix.csv")
    df_results.to_csv(output_path, index=False)
    print(f"\n✅ Evaluation complete! Saved to {output_path}")
    
    # Print the specific match
    print("\n--- Expected Match Details ---")
    match_row = df_results[(df_results['Resume_Category'] == 'INFORMATION-TECHNOLOGY') & 
                           (df_results['JD_Title'] == it_jd.iloc[0]['Job Title'])].iloc[0]
    print(f"Resume: {match_row['Resume_Category']}")
    print(f"JD: {match_row['JD_Title']}")
    print(f"Lexical: {match_row['Lexical']}, Semantic: {match_row['Semantic']}, Skill: {match_row['Coverage']}")
    print(f"Final Score: {match_row['Final_Score']}")

if __name__ == "__main__":
    main()
