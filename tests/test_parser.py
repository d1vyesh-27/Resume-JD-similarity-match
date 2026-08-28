"""
Tests for the document parser module.
"""

import pytest
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import extract_resume_text

@patch('src.parser.extract_pdf_text')
def test_supported_extensions_pdf(mock_pdf_extractor):
    # Mock the PDF extractor so we don't need a real PDF file
    mock_pdf_extractor.return_value = "Extracted PDF text"
    
    result = extract_resume_text(None, "resume.pdf")
    assert result == "Extracted PDF text"
    mock_pdf_extractor.assert_called_once()

@patch('src.parser.extract_docx_text')
def test_supported_extensions_docx(mock_docx_extractor):
    # Mock the DOCX extractor
    mock_docx_extractor.return_value = "Extracted DOCX text"
    
    # Notice we test uppercase .DOCX to ensure case-insensitivity works!
    result = extract_resume_text(None, "resume.DOCX")
    assert result == "Extracted DOCX text"
    mock_docx_extractor.assert_called_once()

def test_unsupported_files():
    # Verify that passing an unsupported file type throws our ValueError
    with pytest.raises(ValueError, match="Unsupported file format"):
        extract_resume_text(None, "resume.txt")
        
    with pytest.raises(ValueError, match="Unsupported file format"):
        extract_resume_text(None, "image.png")
