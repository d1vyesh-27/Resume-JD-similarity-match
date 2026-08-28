"""
Main Streamlit application for Resume-to-Job-Description Match Scorer.
"""
# pyrefly: ignore [missing-import]
import streamlit as st
from src.parser import extract_resume_text
from src.preprocessing import clean_text
from src.matcher import calculate_tfidf_score
from src.semantic_matcher import calculate_semantic_score
from src.keyword_extractor import extract_jd_skills, analyze_skill_gap


def main():
    st.set_page_config(page_title="Resume Matcher", layout="wide")
    st.title("Resume-to-Job-Description Match Scorer")
    
    st.write("Welcome to the Resume Matcher application.")
    st.write("Note: Similarity scores are not hiring probabilities and should not be interpreted as the percentage of job requirements satisfied.")
    
    # Phase 8: Create UI for resume upload
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])
    
    # Phase 8: Create UI for pasted Job Description
    st.subheader("2. Paste Job Description")
    jd_text = st.text_area("Paste the job description text here:", height=200)

    # Phase 8: Add [ Analyze ] button and validate inputs
    if st.button("Analyze Match"):
        if not uploaded_file or not jd_text.strip():
            st.error("Please upload a resume AND paste a job description!")
            return
            
        with st.spinner("Analyzing..."):
            # Phase 7: Call parser to extract text
            try:
                resume_text = extract_resume_text(uploaded_file, uploaded_file.name)
            except ValueError as e:
                st.error(str(e))
                return
                
            # Phase 1: Call preprocessing on resume and JD
            clean_resume = clean_text(resume_text)
            clean_jd = clean_text(jd_text)
            
            # Phase 2: Call TF-IDF matcher for lexical baseline
            lexical_score = calculate_tfidf_score(clean_resume, clean_jd)
            
            # Phase 4: Call semantic matcher for semantic similarity
            semantic_score = calculate_semantic_score(clean_resume, clean_jd)
            
            # Phase 6: Call skill extraction for explicit skill-gap analysis
            jd_skills = extract_jd_skills(jd_text)
            skill_gap = analyze_skill_gap(jd_skills, resume_text)
            
            st.divider()
            st.subheader("Analysis Results")
            
            # Phase 8: Display results in distinct sections
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Lexical Match (TF-IDF)", value=f"{lexical_score * 100:.1f}%")
            with col2:
                st.metric(label="Semantic Match", value=f"{semantic_score * 100:.1f}%")
            with col3:
                coverage = skill_gap.get('coverage', 0.0)
                st.metric(label="Skill Coverage", value=f"{coverage * 100:.1f}%")
            
            st.divider()
            
            # 4. Matched Skills (List)
            # 5. Potentially Missing Skills (List)
            col_match, col_miss = st.columns(2)
            
            with col_match:
                st.success("✅ Matched Skills")
                matched_skills = skill_gap.get('matched', [])
                if matched_skills:
                    for skill in matched_skills:
                        st.write(f"- {skill}")
                else:
                    st.write("No explicit skills matched.")
                    
            with col_miss:
                st.error("❌ Potentially Missing Skills")
                missing_skills = skill_gap.get('missing', [])
                if missing_skills:
                    for skill in missing_skills:
                        st.write(f"- {skill}")
                else:
                    st.write("No missing skills detected!")
                    
            st.divider()
            
            # Phase 8: Add an Interpretation section
            st.subheader("💡 Interpretation")
            if semantic_score > lexical_score + 0.2:
                st.info("The semantic score is significantly higher than the lexical score. This candidate may have the right experience described in different words than the job description.")
            elif lexical_score > semantic_score + 0.2:
                st.warning("The lexical score is significantly higher than the semantic score. This candidate might be keyword stuffing, or their context doesn't match the job description.")
            else:
                st.info("The lexical and semantic scores are balanced, suggesting the resume aligns well with both the keywords and the meaning of the job description.")

if __name__ == "__main__":
    main()
