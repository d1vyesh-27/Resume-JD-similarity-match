# Evaluation Strategy

The goal of this evaluation is to compare the three signals (TF-IDF, Semantic, Skill-Gap) on representative examples, demonstrating the strengths and weaknesses of each approach.

## 1. Validating the Preprocessing Strategy
Before finalizing the TF-IDF pipeline, we will test different preprocessing configurations to gather evidence on what works best for technical jargon:

- **Minimal preprocessing:** Only basic lowercasing and punctuation removal.
- **Lemmatized preprocessing:** Lowercasing, punctuation removal, and spaCy lemmatization.
- **Alias + lemmatized preprocessing:** The safe-word alias dictionary combined with lemmatization.

We will evaluate these against terms like `C++`, `C#`, `.NET`, `Python`, `R`, `PLC`, `SCADA`, `ISO 9001`, and `machine learning` to see which approach yields the most accurate TF-IDF scores without corrupting technical vocabulary.

## 2. Validating the Matching Signals
The application must be tested against these manually constructed test cases to observe how the three signals behave under different conditions:

### Case A — Exact lexical match
- **Scenario:** Resume and JD use almost identical terminology.
- **Expected Outcome:** 
  - TF-IDF: High score.
  - Semantic: High score.
  - Skill Coverage: High (few/no missing skills).

### Case B — Semantic equivalence
- **Scenario:** Different wording for the same concept. 
  - *Example Resume:* "Led a cross-functional team."
  - *Example JD:* "Experience in team leadership."
- **Expected Outcome:** 
  - TF-IDF: May be lower due to vocabulary mismatch.
  - Semantic: Should be relatively high, recognizing the meaning overlap.

### Case C — Missing technical skills
- **Scenario:** The resume shares general context but lacks specific requested technologies.
  - *Example JD:* Python, Docker, AWS, Kubernetes
  - *Example Resume:* Python, SQL
- **Expected Outcome:** 
  - Skill-gap analysis should explicitly identify Docker, AWS, and Kubernetes as missing technologies.

### Case D — Wrong domain
- **Scenario:** Completely mismatched technical backgrounds.
  - *Example Resume:* Python, pandas, scikit-learn
  - *Example JD:* PLC, SCADA, DCS, industrial automation
- **Expected Outcome:** 
  - Semantic similarity: Low.
  - Skill Coverage: Low.
  - TF-IDF: Potentially low.

### Case E — Keyword-heavy overlap
- **Scenario:** Keywords overlap substantially, but the actual context is weak or nonsensical (keyword stuffing).
- **Expected Outcome:** 
  - Used to demonstrate the limitations of pure lexical matching (TF-IDF could score high, while semantic matching might show a more realistic relationship).

### Case F — Synonyms / related terminology
- **Scenario:** Test wording differences where the underlying skill or experience is similar, but not identical.
- **Expected Outcome:** 
  - Semantic models should handle this better than TF-IDF.
