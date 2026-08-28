"""
Tests for the preprocessing module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing import clean_text

def test_lowercase():
    text = "SOFTWARE DEVELOPER"
    assert "software" in clean_text(text)

def test_empty_input():
    assert clean_text("") == ""
    assert clean_text(None) == ""

def test_technical_tokens_preserved():
    # Our tech_skills.json has "c++" which aliases to "cplusplus"
    text = "I know C++ and .NET"
    cleaned = clean_text(text)
    assert "cplusplus" in cleaned
    assert "dotnet" in cleaned
