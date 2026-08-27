# System Architecture

This document explains the high-level architecture of the Resume-to-Job-Description Match Scorer.

The architecture is built around **three complementary analysis signals**:
1. TF-IDF lexical similarity
2. Semantic similarity using sentence embeddings
3. Explicit skill-gap analysis

## Data Flow Diagram

```text
                         USER
                           │
                           ↓
                  Streamlit Interface
                           │
                           ↓
                  Resume PDF / DOCX
                           │
                           ↓
                     Text Parser
                           │
                           ↓
                    Text Cleaning
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
           TF-IDF      Embeddings    Skill Extractor
              ↓            ↓            ↓
        TF-IDF Vector   Embeddings   JD Skills
              ↓            ↓            ↓
              │        Cosine          │
              │       Similarity        │
              ↓            ↓            ↓
        Lexical Score  Semantic Score  Skill Coverage
              │            │            │
              └────────────┼────────────┘
                           ↓
                    Match Analysis
                           │
               ┌───────────┴───────────┐
               ↓                       ↓
         Similarity Scores       Skill Gap Report
               ↓                       ↓
         Streamlit Results
```

## Component Responsibilities

- **Streamlit Interface (`app.py`):** Orchestrates the components and handles user inputs (file uploads, text pasting). Displays the three signals independently.
- **Text Parser (`src/parser.py`):** Extracts raw text from uploaded PDF or DOCX files.
- **Preprocessing Layer (`src/preprocessing.py`):** Cleans text (lowercasing, tokenization) while carefully preserving important technical vocabulary (e.g., C++, .NET).
- **TF-IDF Matcher (`src/matcher.py`):** Computes a lexical baseline similarity score by converting documents to TF-IDF vectors and calculating their cosine similarity.
- **Semantic Matcher (`src/semantic_matcher.py`):** Computes semantic similarity by generating dense embeddings using a pretrained lightweight sentence-transformer and calculating cosine similarity.
- **Skill Extraction (`src/keyword_extractor.py`):** Analyzes the JD to find key technical terms (languages, frameworks, cloud tools) and compares them against the resume text to highlight explicit gaps.

## Development Phases

1. **Phase 1:** Get text preprocessing working.
2. **Phase 2:** Implement TF-IDF baseline.
3. **Phase 3:** Implement cosine similarity and verify the baseline manually.
4. **Phase 4:** Implement sentence-transformer semantic matching.
5. **Phase 5:** Compare TF-IDF and semantic results on controlled examples.
6. **Phase 6:** Implement skill extraction and missing-skill detection.
7. **Phase 7:** Integrate PDF/DOCX parsing.
8. **Phase 8:** Build Streamlit UI.
9. **Phase 9:** Evaluate and refine all three signals.
10. **Phase 10:** Deploy.
