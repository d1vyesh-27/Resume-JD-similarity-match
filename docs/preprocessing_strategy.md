# Preprocessing Strategy for Resume-JD Matching

Handling technical terminology correctly is one of the most common pitfalls in NLP for HR tech. This document outlines a robust, student-friendly strategy that avoids over-engineering while preventing the destruction of critical technical terms.

## 1. Two Different Pipelines, Two Different Approaches

A critical design decision for this project is that **TF-IDF and Sentence-Transformers require completely different preprocessing.**

### Approach A: Sentence-Transformer Pipeline (Minimal Preprocessing)
Pretrained transformers (like `all-MiniLM-L6-v2`) have their own tokenization (e.g., BPE/WordPiece) and preprocessing pipelines. 
- **What we do:** Minimal text cleanup (e.g., removing PDF extraction artifacts) → pretrained Sentence Transformer → embeddings → cosine similarity.
- **Why:** Don't manually strip punctuation, stopwords, or linguistic structure before sending text to the pretrained sentence-transformer. The model is trained on raw text and its own tokenizer is best equipped to handle sentence structure.

### Approach B: TF-IDF Pipeline (Controlled/Conservative Preprocessing)
TF-IDF relies entirely on exact string overlap. If the JD says "c++" and the resume says "C++," they must resolve to the exact same token.
- **What we do:** A carefully controlled, conservative cleaning process designed to protect technical terms before general cleaning occurs. 
- **Summary:** Controlled preprocessing + technical-term protection + optional lemmatization + unigrams/bigrams.

---

## 2. The TF-IDF Preprocessing Steps

We will use a combination of **Custom Dictionary Normalization**, **spaCy**, and **scikit-learn**. 

### Step 1: Technical Alias Normalization (The "Safe-Word" Approach)
Before applying *any* lowercasing or punctuation removal, we use a simple dictionary replacement to map symbol-heavy technical terms to safe, alphanumeric strings.
- **Why:** Regex word boundaries (`\b`) fail on symbols like `+` and `#`. Explicit string replacement is foolproof and highly interpretable. 
- **Bonus:** This dictionary can also conservatively normalize common equivalent representations (e.g., `"machine-learning" -> "machine learning"`, `"restful api" -> "rest api"`). However, we must be *very conservative* to avoid accidentally declaring two different technologies equivalent.

### Step 2: Lowercasing
Convert the entire text to lowercase.

### Step 3: Tokenization & Stopword Removal (spaCy)
Pass the text through a lightweight `spaCy` pipeline (`en_core_web_sm`).
- Remove standard English stopwords.
- Remove standalone punctuation.
- **Crucial Override:** Keep 1-letter tokens (so "r" and "c" are not discarded).

### Step 4: Optional Lemmatization
Use spaCy to lemmatize words (e.g., "developed" -> "develop") to maximize overlap. 
- **Note:** This is *optional* and its effectiveness must be validated (see Section 6). Technical terminology can sometimes be harmed by aggressive linguistic processing.

### Step 5: N-Grams (in scikit-learn)
When configuring `TfidfVectorizer`, we will use `ngram_range=(1, 2)` (unigrams and bigrams).
- **Why:** This automatically captures multi-word terms like "machine learning" and "iso 9001" without needing complex Named Entity Recognition (NER).

---

## 3. Concrete Before/After Examples (TF-IDF Pipeline)

Here is how the pipeline processes specific terms using the Alias approach:

| Original Term | After Step 1 (Alias) | After TF-IDF Pipeline (Tokens generated) | Why it works |
| :--- | :--- | :--- | :--- |
| `C++` | `cplusplus` | `['cplusplus']` | Protected from `+` being stripped as punctuation. |
| `C#` | `csharp` | `['csharp']` | Protected from `#` being stripped. |
| `.NET` | `dotnet` | `['dotnet']` | Protected from `.` being split or stripped. |
| `Node.js` | `nodejs` | `['nodejs']` | Protected from being split into "Node" and "js". |
| `scikit-learn` | `scikitlearn` | `['scikitlearn']` | Hyphen is removed via alias to ensure one token. |
| `restful api` | `rest api` | `['rest', 'api', 'rest api']` | Normalizes common equivalents. |
| `SQL` | `SQL` | `['sql']` | Standard lowercasing handles this perfectly. |
| `PLC/SCADA` | `PLC/SCADA` | `['plc', 'scada', 'plc scada']` | Slashes naturally separate terms; 2-grams capture the combination. |
| `ISO 9001` | `ISO 9001` | `['iso', '9001', 'iso 9001']` | 2-grams naturally capture the standard designation. |
| `machine learning` | `machine learning` | `['machine', 'learning', 'machine learning']` | 2-grams capture the phrase. |
| `R` | `R` | `['r']` | Custom rule prevents 1-letter tokens from being dropped. |

---

## 4. Tradeoffs of This Approach

### Advantages
1. **Highly Interpretable:** The student can literally read the dictionary mapping (`{"C++": "cplusplus"}`). There is no "black box" regex magic.
2. **Easy to Debug:** If a new term breaks (e.g., `F#`), fixing it takes 5 seconds (add `"F#": "fsharp"` to the dictionary).
3. **Appropriate Complexity:** It balances robustness with the limitations of a 5-day educational project.

### Limitations
1. **Maintenance Burden:** The alias dictionary is manual. It won't automatically know how to handle a brand new symbolic language unless it's added to the map.
2. **False Positives in N-grams:** Generating 2-grams means we also generate nonsense tokens. However, TF-IDF naturally mitigates this because nonsense bigrams will have low frequencies.

---

## 5. Validating the Preprocessing Strategy

We will not assume that our preprocessing strategy is perfect. We will evaluate and compare different TF-IDF preprocessing variations on our test cases to gather evidence for our final preprocessing choice:

```text
                    TF-IDF
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
Minimal          Lemmatized       Alias + lemmatized
preprocessing    preprocessing     preprocessing
       │               │                │
       └───────────────┼────────────────┘
                       ↓
                  Test cases
                       ↓
                 Compare results
```

We will specifically test how terms like `C++`, `C#`, `.NET`, `Python`, `R`, `PLC`, `SCADA`, `ISO 9001`, and `machine learning` are impacted across these variations.

---

## 6. Final Preprocessing Architecture Summary

- **TF-IDF:** Controlled preprocessing + technical-term protection + optional lemmatization + unigrams/bigrams.
- **Semantic:** Minimal text cleanup → pretrained Sentence Transformer → embeddings → cosine similarity.
- **Skill gap:** Separate pipeline focused specifically on identifying explicit technical skills/requirements.
