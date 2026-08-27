"""
Document parsing module to extract text from PDF and DOCX files.

IMPORTANT IMPLEMENTATION CONSTRAINT:
When implementing components in this module, first explain in comments:
1. What the concept is.
2. Why it is needed.
3. What the input is.
4. What the output is.
5. What the relevant library function does.
Do not dump unexplained code.
"""

def extract_pdf_text(file) -> str:
    """
    Extracts text from a PDF file.
    
    Args:
        file: A file-like object (e.g., uploaded via Streamlit).
        
    Returns:
        str: Extracted text.
    """
    # Phase 7 TODO: Implement PDF parsing (e.g., using pdfplumber)
    # Phase 7 TODO: Handle edge cases: scanned/image-only PDFs, empty extraction, multi-column layouts, tables, headers/footers, unusual encoding.
    pass

def extract_docx_text(file) -> str:
    """
    Extracts text from a DOCX file.
    
    Args:
        file: A file-like object.
        
    Returns:
        str: Extracted text.
    """
    # Phase 7 TODO: Implement DOCX parsing (e.g., using python-docx)
    pass

def extract_resume_text(file, filename: str) -> str:
    """
    Wrapper function to handle text extraction based on file extension.
    
    Args:
        file: A file-like object.
        filename (str): Name of the file to determine extension.
        
    Returns:
        str: Extracted text.
    """
    # Phase 7 TODO: Check file extension and route to extract_pdf_text or extract_docx_text
    # Phase 7 TODO: Handle unsupported file types cleanly
    pass
