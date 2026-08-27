# System Limitations

This document outlines the known limitations of the Resume-to-Job-Description Match Scorer.

## Interpretation Limitations
- **Similarity is NOT hiring probability:** The matching scores (Lexical and Semantic) do not reflect the likelihood of a candidate being hired, nor do they represent the percentage of job requirements satisfied. They simply measure text/meaning similarity.
- **Skill possession verification:** The skill-gap analysis identifies if a skill is mentioned in the text. It does not verify the candidate's actual proficiency or possession of that skill.

## TF-IDF (Lexical Baseline) Limitations
- **Sensitive to exact wording:** TF-IDF relies heavily on lexical overlap. If the resume and JD use different synonyms for the same skill, the lexical score will be artificially low.
- **Context-blind:** "Managed a team of Python developers" vs "Looking for a Python developer" might have overlapping keywords without sharing identical context.

## Semantic Model Limitations
- **Context misunderstanding:** Pretrained sentence-transformers can still misunderstand context and produce false similarities.
- **Domain-specific meanings:** Lightweight general-purpose models may miss nuanced, domain-specific engineering jargon.
- **Ambiguous terminology:** Short, ambiguous technical terms can confuse the embedding representation.
- **Resource Constraints:** There is a tradeoff between semantic quality and inference speed/model size, especially for Streamlit deployment.

## Skill-Gap Analysis Limitations
- **Imperfect Extraction:** Skill extraction relies on heuristics or simple NLP techniques, which may miss newly emerging technologies or over-extract generic phrases.
- **Abbreviation normalization:** Technical abbreviations (e.g., AWS vs Amazon Web Services) can be difficult to normalize and match correctly without a dedicated taxonomy.

## Parsing Limitations
- **Scanned PDFs:** PDF parsing can fail on scanned or image-only PDFs without OCR.
- **Complex Layouts:** Multi-column resumes, tables, headers, and footers can parse poorly and scramble text structure, affecting both TF-IDF and Semantic embeddings.
