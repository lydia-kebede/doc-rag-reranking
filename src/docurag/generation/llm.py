from dataclasses import dataclass
import re
from typing import Callable

from docurag.reranking.context_builder import ContextBuilder


@dataclass
class GenerationResult:
    answer: str
    citations: list[str]
    is_grounded: bool


class RAGGenerator:
    """Generate an answer from supplied passages using an injected LLM callable."""

    def __init__(
        self,
        llm: Callable[[str], str],
        context_builder: ContextBuilder | None = None,
    ) -> None:
        self.llm = llm
        self.context_builder = context_builder or ContextBuilder()

    @staticmethod
    def create_prompt(question: str, context: str) -> str:
        return f"""You are a document question-answering assistant.

Answer the question using ONLY the supplied context.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts or sources.
3. Cite supporting passages using [S1], [S2], etc.
4. If the context does not contain the answer, say that the information
   is not available in the provided documents.
5. Every factual claim must have a supporting citation.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    def generate(self, question: str, passages: list) -> GenerationResult:
        context = self.context_builder.build(passages)

        if not context.strip():
            return GenerationResult(
                answer="I could not find relevant information in the documents.",
                citations=[],
                is_grounded=False,
            )

        answer = str(self.llm(self.create_prompt(question, context)))
        citations = list(dict.fromkeys(re.findall(r"\[S(\d+)\]", answer)))

        available = {str(index) for index in range(1, len(passages) + 1)}
        valid_references = bool(citations) and all(
            citation in available for citation in citations
        )

        return GenerationResult(
            answer=answer,
            citations=citations,
            is_grounded=valid_references,
        )


def validate_citations(result: GenerationResult, passages: list) -> bool:
    """Validate citation IDs exist; this does not prove semantic entailment."""
    if not result.is_grounded or not result.citations:
        return False

    return all(
        citation.isdigit() and 1 <= int(citation) <= len(passages)
        for citation in result.citations
    )
