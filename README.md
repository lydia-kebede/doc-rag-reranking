# Doc-RAG: reranking and grounded generation contribution

This folder contains the assigned modules for:
- Cross-Encoder reranking of candidate passages
- Context selection and source labelling
- LLM answer generation with citation references
- Basic tests using a mock LLM (no API key required)

## Add this to the common repository

1. Unzip this folder.
2. Open the unzipped `doc-rag-reranking-contribution` folder in VS Code.
3. Copy its `src/docurag/reranking` and `src/docurag/generation` folders into the matching `src/docurag/` location in your team repository. Merge files if those folders already exist; do not overwrite teammates' work.
4. Copy `tests/test_rag_generation.py` into the repository's `tests/` folder (or merge its test into the existing test layout).
5. Add this dependency to the repository's existing requirements file:

   `sentence-transformers`

   Do not replace the team's existing requirements file.

## Install and test

From the root of the team repository:

```bash
python -m pip install sentence-transformers pytest
PYTHONPATH=src python -m compileall -q src/docurag
PYTHONPATH=src python -m pytest tests/test_rag_generation.py -q
```

The first Cross-Encoder run downloads the model, so it needs an internet connection.

## Connect the team's LLM

`RAGGenerator` accepts an LLM callable that takes a prompt string and returns an answer string. Pass your team's existing provider/client wrapper:

```python
generator = RAGGenerator(llm=your_llm_function)
result = generator.generate(question, reranked_passages)
```

The `passages` argument should be the list returned by `CrossEncoderReranker.rerank()`.

## Important integration note

The reranker supports passage dictionaries with `text`, `content`, or `page_content`, and objects with corresponding attributes. Check your team's actual `SearchResult` shape and adjust `_get_text()` if it uses another field.

Citation validation checks that cited source labels exist. It does not establish that a cited passage semantically supports every claim; that needs a separate evaluation step.
# doc-rag-reranking
# doc-rag-reranking
