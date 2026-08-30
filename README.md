# Resume-to-Job-Description Match Scorer

🚀 **Live Application:** [https://resume-jd-similarity-match-7xghqhiorwcz8ht2kvacxp.streamlit.app/](https://resume-jd-similarity-match-7xghqhiorwcz8ht2kvacxp.streamlit.app/)
## Overview
A web application that evaluates how well a resume matches a given Job Description (JD). The project uses **three complementary analysis signals** to provide a transparent and actionable matching analysis:
1. **TF-IDF Lexical Similarity:** A baseline measuring exact keyword overlap.
2. **Semantic Similarity:** Uses pretrained sentence embeddings to measure meaning overlap.
3. **Explicit Skill-Gap Analysis:** Extracts important technical skills from the JD and identifies which ones appear to be absent from the resume.

**Note:** The application provides a *matching analysis*, not a hiring prediction. Similarity scores are not equivalent to hiring probability.

## Problem
Comparing a resume to a job description manually is time-consuming. However, simple keyword-matching systems often miss relevant candidates who use different terminology (synonyms). This project bridges that gap by combining a lexical baseline (exact keyword overlap) with semantic scoring (meaning overlap) and explicit technical skill-gap detection.

## Features
- **Resume Parsing:** Supports extracting text from PDF and DOCX formats.
- **Three-Signal Analysis:**
  - **TF-IDF Match:** Calculates similarity based on exact vocabulary overlap.
  - **Semantic Match:** Calculates similarity based on meaning using pretrained sentence-transformers.
  - **Skill Coverage:** Identifies matched and potentially missing technical skills (e.g., programming languages, frameworks, cloud technologies).
- **No Arbitrary Final Score:** The signals answer different questions and are presented separately rather than being blindly averaged.

## System Architecture
Please see [docs/architecture.md](docs/architecture.md) for a detailed system diagram showing the parallel signal architecture.

## Methodology
The application uses three distinct approaches. For detailed rationale, see [docs/methodology.md](docs/methodology.md).

### TF-IDF Baseline
Measures exact term overlap between the resume and JD using Term Frequency-Inverse Document Frequency. This approximates traditional keyword-oriented resume screening.

### Semantic Matching
Uses pretrained sentence-transformers to capture the semantic meaning of the texts, allowing the system to recognize when different words (e.g., "cross-functional team leadership" vs. "management experience") mean the same thing.

### Missing Skill Detection
Focuses exclusively on explicit technical requirements (programming languages, tools, frameworks) and compares them against the resume to highlight potential gaps, answering: *What explicit technical requirements from the JD appear to be missing from the resume?*

## Tech Stack
- **Python**
- **Streamlit** (Web Interface)
- **scikit-learn** (TF-IDF Baseline)
- **sentence-transformers** (Semantic Matching)
- **spaCy** (NLP Preprocessing)
- **pdfplumber / python-docx** (Document Parsing)

## Project Structure
- `src/`: Core application logic (parsing, preprocessing, matching).
- `tests/`: Unit tests for core modules.
- `notebooks/`: Jupyter notebooks for data exploration and experimentation.
- `data/`: Local directory for datasets (ignored in version control).
- `docs/`: Detailed project documentation.

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

## Installation
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally
Launch the Streamlit application:
```bash
streamlit run app.py
```

## Example Usage
1. Open the application in your browser.
2. Upload a PDF or DOCX resume.
3. Paste the target Job Description text.
4. View the Lexical Match, Semantic Match, and Skill Coverage scores separately.
5. Review the list of Matched and Potentially Missing skills.

## Evaluation
Please see [docs/evaluation.md](docs/evaluation.md) for the evaluation strategy and edge case tests.

## Limitations
Please see [docs/limitations.md](docs/limitations.md) for important caveats. **A similarity score is NOT equivalent to hiring probability.**

## Future Improvements
- Better technical skill extraction with NER or domain-specific taxonomies.
- Section-aware resume parsing (separating Experience, Education, Skills).
- Cross-encoder reranking for better semantic matching.
- OCR support for scanned resumes.

## Author
Developer
