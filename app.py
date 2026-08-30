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
    
    # Title in the middle top
    st.markdown(
        """
        <div style='text-align: center; margin-top: -2rem; margin-bottom: 2rem;'>
            <h1>Resume Job Description Similarity Score</h1>
            <p style='color: gray;'>Note: Similarity scores are not hiring probabilities and should not be interpreted as the percentage of job requirements satisfied.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Divide into 2 sections
    col_upload, col_paste = st.columns(2)
    
    with col_upload:
        st.subheader("📄 Upload Resume")
        uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"], label_visibility="collapsed")
        
    with col_paste:
        st.subheader("📋 Paste Job Description")
        jd_text = st.text_area("Paste the job description text here:", height=200, label_visibility="collapsed")
        st.caption("💡 *Tip: For the best results, try to paste only the core requirements and responsibilities. Removing redundant boilerplate (like company culture or benefits) improves accuracy.*")
        
    st.markdown("<br>", unsafe_allow_html=True)

    # Just below it analyze button
    col_empty1, col_btn, col_empty2 = st.columns([3, 2, 3])
    with col_btn:
        analyze_clicked = st.button("🔍 Analyze Match", use_container_width=True, type="primary")
        
    if analyze_clicked:
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
                
            resume_text_to_process = resume_text
            jd_text_to_process = jd_text
                
            # Phase 1: Call preprocessing on resume and JD
            clean_resume = clean_text(resume_text_to_process)
            clean_jd = clean_text(jd_text_to_process)
            
            # Phase 2: Call TF-IDF matcher for lexical baseline
            lexical_score = calculate_tfidf_score(clean_resume, clean_jd)
            
            # Phase 4: Call semantic matcher for semantic similarity
            # IMPORTANT: We pass the raw text here so the model retains the natural sentence structure and grammar, avoiding artificially high semantic scores.
            semantic_score = calculate_semantic_score(resume_text_to_process, jd_text_to_process)
            
            # Phase 6: Call skill extraction for explicit skill-gap analysis
            jd_skills = extract_jd_skills(jd_text)
            skill_gap = analyze_skill_gap(jd_skills, resume_text)
            
            coverage = skill_gap.get('coverage', 0.0)
            
            st.divider()
            st.subheader("Analysis Results")
            
            # Phase 8: Display results in distinct sections
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Lexical Match (TF-IDF)", value=f"{lexical_score * 100:.1f}%")
            with col2:
                st.metric(label="Semantic Match", value=f"{semantic_score * 100:.1f}%")
            with col3:
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
            
            # Reasoning
            st.subheader("💡 Reasoning")
            
            # All three high
            if semantic_score >= 0.5 and lexical_score >= 0.3 and coverage >= 0.4:
                st.success("Strong match — resume aligns on exact keywords, underlying meaning, and required skills.")
                
            # Semantic high, lexical notably lower, skill moderate+
            elif semantic_score >= 0.5 and lexical_score < 0.3 and coverage >= 0.2:
                st.success("Strong conceptual fit — resume covers the underlying meaning and skills of this role even where exact wording differs.")
                
            # Lexical high, semantic notably lower
            elif lexical_score >= 0.3 and semantic_score < 0.5:
                st.warning("Resume shares keywords with this posting, but overall context alignment is weaker — possible keyword overlap without full domain fit.")
                
            # All three low
            elif semantic_score < 0.25 and lexical_score < 0.1 and coverage < 0.2:
                st.error("Weak match — this role differs substantially from the resume in wording, meaning, and required skills.")
                
            # Skill low but semantic/lexical moderate+
            elif coverage < 0.4 and (semantic_score >= 0.25 or lexical_score >= 0.1):
                st.info("Conceptually related field, but missing several of the specific required skills.")
                
            else:
                st.info("Mixed signals — review the individual scores above for a detailed breakdown.")
                
            # Conditional Note on Scoring (Only show if lexical is dragging down a good semantic match)
            if (semantic_score - lexical_score > 0.2) and (semantic_score > 0.4):
                st.markdown(
                    """
                    <br>
                    <div style='background-color: #262730; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #4B4B52;'>
                        <p><strong>🧠 Note on Scoring</strong><br>
                        In real-world scenarios, prioritize the <strong>Semantic Match</strong> and <strong>Skill Coverage</strong>. The Lexical (TF-IDF) score requires exact word-for-word overlap and naturally provides less value for well-written, natural language resumes.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
    st.divider()
    
    # My details
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p><strong>Developed by Divyesh Kuduva</strong></p>
            <p>Resume-JD Similarity Matching Engine</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
