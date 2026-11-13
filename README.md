# Doc-RAG: Cross-Encoder Reranking & LLM Answer Generation

## Overview

This repository contains my contribution to the Doc-RAG (Document Retrieval-Augmented Generation) project.

My main responsibility is improving the relevance of retrieved document passages and generating accurate, evidence-supported answers using Large Language Models (LLMs).

The implementation focuses on three main components:

1. Cross-Encoder Reranking
2. Context Selection and Assembly
3. LLM Answer Generation with Citation Support

## System Workflow

The components follow this workflow:

```text
User Question
      |
      v
Hybrid Retriever
      |
      v
Candidate Passages
      |
      v
Cross-Encoder Reranking
      |
      v
Context Selection & Assembly
      |
      v
LLM Answer Generation
      |
      v
Answer with Source Citations
```

## 1. Cross-Encoder Reranking

**File:** `src/docurag/reranking/cross_encoder.py`

The hybrid retriever returns candidate passages that may contain relevant information. However, not all retrieved passages are equally relevant to the user's question.

To improve retrieval quality, I implemented a Cross-Encoder reranking module using Sentence Transformers.

### Main functionalities

- Receives a user query and candidate passages.
- Evaluates query-passage pairs.
- Assigns relevance scores.
- Sorts passages according to their relevance.
- Returns the top-ranked passages.

### Model Used

`cross-encoder/ms-marco-MiniLM-L-6-v2`

The model evaluates the relationship between the query and each passage to produce relevance scores.

## 2. Context Selection and Assembly

**File:** `src/docurag/reranking/context_builder.py`

After reranking, the system needs to prepare relevant passages for the LLM.

I implemented a Context Builder to select and organize the highest-ranked passages.

### Main functionalities

- Selects relevant ranked passages.
- Assigns source identifiers such as `[S1]`, `[S2]`, and `[S3]`.
- Preserves original source identifiers.
- Combines passages into an organized context.
- Enforces a maximum context character limit.

This makes the retrieved information easier for the LLM to process and allows generated answers to reference their supporting passages.

## 3. LLM Answer Generation

**File:** `src/docurag/generation/llm.py`

The LLM generation module uses the selected document context to generate answers.

I implemented an answer-generation pipeline that accepts an LLM callable, constructs an evidence-restricted prompt, and processes the generated response.

### Main functionalities

- Creates prompts using the user's question and retrieved context.
- Restricts answers to the supplied document evidence.
- Instructs the model not to invent facts or sources.
- Requests source citations for factual claims.
- Extracts citation references from generated answers.
- Performs basic citation reference validation.

### Grounded Answer Generation

The prompt instructs the LLM to:

- Use only the supplied context.
- Avoid unsupported information.
- Include citations such as `[S1]` and `[S2]`.
- Clearly indicate when the answer is unavailable in the documents.

## 4. Citation Validation

The implementation includes a citation validation function.

It checks whether the citation identifiers referenced in the generated answer correspond to available context passages.

**Note:** Citation reference validation does not guarantee that a cited passage semantically supports every claim. More advanced evidence evaluation would be required for that.

## Project Structure

```text
src/
└── docurag/
    ├── reranking/
    │   ├── __init__.py
    │   ├── cross_encoder.py
    │   └── context_builder.py
    │
    └── generation/
        ├── __init__.py
        └── llm.py

tests/
└── test_rag_generation.py
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Sentence Transformers | Cross-Encoder reranking |
| MiniLM | Pretrained reranking model |
| Large Language Models | Answer generation |
| Prompt Engineering | Evidence-restricted generation |
| Pytest | Automated testing |

## Installation

Install the required dependencies:

```bash
pip install sentence-transformers pytest
```

## Testing

Run Python compilation checks:

```bash
PYTHONPATH=src python -m compileall -q src/docurag
```

Run the generation and citation tests:

```bash
PYTHONPATH=src python -m pytest tests/test_rag_generation.py -q
```

The tests use a mock LLM function, so an external LLM API key is not required for those tests.

The first Cross-Encoder execution may download the pretrained model and therefore requires an internet connection.

## Learning Outcomes

Through this implementation, I gained practical experience in:

- Transformer-based document reranking.
- Query-passage relevance scoring.
- Context selection and management.
- LLM integration.
- Prompt engineering.
- Citation extraction and validation.
- Grounded answer generation and hallucination reduction.

## Conclusion

My contribution focuses on improving the quality and reliability of the Doc-RAG system.

By combining Cross-Encoder reranking, structured context assembly, and evidence-restricted LLM generation, the implementation helps ensure that generated answers are based on relevant document passages and include references to their sources.

---

**Project:** Doc-RAG  
**Contribution:** Cross-Encoder Reranking, Context Selection, and LLM Answer Generation  
**Developer:** Lydia Kebede
