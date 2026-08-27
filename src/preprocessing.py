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

def clean_text(text: str) -> str:
    """
    Cleans and preprocesses the input text.
    
    Potential processing steps:
    - Lowercase conversion
    - Tokenization
    - Stopword handling
    - Lemmatization
    
    IMPORTANT: Be conservative with technical terms! 
    Do not blindly remove tokens like C++, C#, .NET, SQL, AWS, PLC, SCADA, MATLAB, ROS.
    These are critical for matching technical roles.
    
    Args:
        text (str): Raw text from resume or JD.
        
    Returns:
        str: Cleaned text.
    """
    # Phase 1 TODO: Implement basic cleaning logic
    # Phase 1 TODO: Add logic to preserve technical vocabulary (C++, C#, .NET, etc.)
    pass
