# Methodology

The application uses **three complementary analysis signals**. They are not simply averaged into a single arbitrary score; each component answers a distinct question about the resume and the job description.

## 1. Signal 1: TF-IDF Lexical Similarity

### Purpose
To measure how much the resume and JD overlap in their actual vocabulary. This serves as a lexical baseline that approximates traditional keyword-oriented resume screening.

### TF-IDF Design Question
During implementation, the project will investigate how to fit the TF-IDF vectorizer:
- **Approach A (Pairwise TF-IDF):** Fitting only on the `[resume, JD]` pair. Simple, focused on the current comparison, but IDF statistics are based only on two documents.
- **Approach B (Domain corpus TF-IDF):** Fitting on a relevant collection of job descriptions/resumes to establish more stable IDF statistics. Requires a suitable corpus which can distort statistics if poorly composed.

## 2. Signal 2: Semantic Similarity

### Purpose
To measure how similar the meanings of the resume and JD are. TF-IDF relies heavily on lexical overlap and struggles with synonyms (e.g., "Led a cross-functional team" vs. "Experience in team leadership"). 

### Approach
We use a pretrained sentence-transformer model to generate dense embedding vectors for both texts, and compute their cosine similarity. Semantic models capture relationships between different terms. We prioritize lightweight pretrained models balancing semantic quality, model size, and inference speed for the Streamlit deployment.

## 3. Signal 3: Explicit Skill-Gap Analysis

### Purpose
To answer: *"Which important skills mentioned by the JD appear to be absent from the resume?"*

### Approach
This is **NOT** just generic keyword extraction (e.g., extracting "experience" or "candidate" using top TF-IDF words). Skill-gap analysis focuses strictly on explicit technical requirements:
- Programming languages (Python, C++)
- Frameworks and libraries
- Cloud technologies (AWS, Docker, Kubernetes)
- Databases (SQL)
- Engineering tools (PLC, SCADA, MATLAB)
- Relevant domain methodologies and multi-word phrases (Machine Learning, REST APIs)

## Why Semantic Matching and Skill Matching are Different
Semantic similarity determines if the overall meaning is similar (e.g., "Developed predictive models" matches "Experience with machine learning" semantically). 
However, skill extraction answers a stricter question: Did the candidate explicitly list "Machine Learning" as requested? Thus, a resume might have a high semantic score but still be missing a critical explicit skill according to the skill-gap analysis. Both components are required for a transparent analysis.
