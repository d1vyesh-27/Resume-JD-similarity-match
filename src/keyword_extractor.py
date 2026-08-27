"""
Keyword and explicit skill extraction module for Job Descriptions and Resumes.

IMPORTANT IMPLEMENTATION CONSTRAINT:
When implementing components in this module, first explain in comments:
1. What the concept is.
2. Why it is needed.
3. What the input is.
4. What the output is.
5. What the relevant library function does.
Do not dump unexplained code.
"""

def extract_jd_skills(jd_text: str) -> list:
    """
    Extracts explicit technical skills from a Job Description.
    
    IMPORTANT: This is NOT just generic keyword extraction. Do not simply extract the top 20 
    TF-IDF words (like 'experience' or 'candidate'). Focus on explicit technical requirements:
    - Programming languages (Python, C++)
    - Frameworks and libraries
    - Cloud technologies (Docker, AWS, Kubernetes)
    - Databases (SQL)
    - Domain tools (PLC, SCADA, MATLAB)
    - Multi-word technical phrases (Machine Learning, REST APIs)
    
    Args:
        jd_text (str): Raw or preprocessed job description text.
        
    Returns:
        list: List of extracted technical skills/phrases.
    """
    # Phase 6 TODO: Implement explicit technical skill extraction logic
    pass

def analyze_skill_gap(jd_skills: list, resume_text: str) -> dict:
    """
    Compares JD skills against the resume to explicitly identify matched and missing skills.
    
    This component answers: "What explicit technical requirements from the JD appear to be missing?"
    
    Args:
        jd_skills (list): Technical skills extracted from the JD.
        resume_text (str): Text extracted from the resume.
        
    Returns:
        dict: A dictionary containing 'matched', 'missing', and potentially a 'skill_coverage' score.
    """
    # Phase 6 TODO: Compare extracted JD skills with resume content
    # Phase 6 TODO: Return structured results highlighting what is present vs missing
    pass
