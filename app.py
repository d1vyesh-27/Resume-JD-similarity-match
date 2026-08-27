"""
Main Streamlit application for Resume-to-Job-Description Match Scorer.
"""
import streamlit as st

# TODO: Import parser, preprocessing, matcher, semantic_matcher, keyword_extractor

def main():
    st.set_page_config(page_title="Resume Matcher", layout="wide")
    st.title("Resume-to-Job-Description Match Scorer")
    
    st.write("Welcome to the Resume Matcher application.")
    st.write("Note: Similarity scores are not hiring probabilities and should not be interpreted as the percentage of job requirements satisfied.")
    
    # Phase 8 TODO: Create UI for resume upload (PDF/DOCX)
    # Phase 8 TODO: Create UI for pasted Job Description
    
    # Phase 8 TODO: Add [ Analyze ] button and validate inputs
    
    # Phase 7 TODO: Call parser to extract text
    
    # Phase 1 TODO: Call preprocessing on resume and JD
    
    # Phase 2 TODO: Call TF-IDF matcher for lexical baseline
    
    # Phase 4 TODO: Call semantic matcher for semantic similarity
    
    # Phase 6 TODO: Call skill extraction for explicit skill-gap analysis
    
    # Phase 8 TODO: Display results in distinct sections:
    # 1. TF-IDF Match
    # 2. Semantic Match
    # 3. Skill Coverage
    # 4. Matched Skills (List)
    # 5. Potentially Missing Skills (List)
    
    # Phase 8 TODO: Add an Interpretation section comparing the semantic and lexical scores
    
    # Phase 8 TODO: Display warnings/errors if any

if __name__ == "__main__":
    main()
