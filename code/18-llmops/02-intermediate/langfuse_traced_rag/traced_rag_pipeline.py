from __future__ import annotations

from tracer import get_tracer

# Topic 08's RAG pipeline isn't implemented in this repo yet, so this wires tracing into a
# small mock RAG pipeline with the same retrieval/generation shape it would have.

_DOCS = {
    "vllm": "vLLM uses continuous batching and PagedAttention to serve LLMs efficiently.",
    "caching": "Semantic caching reuses responses for embedding-similar prompts to cut cost.",
}

_PRICE_PER_1K_TOKENS = 0.006


def mock_retrieve(question: str) -> list[str]:
    question_lower = question.lower()
    return [doc for key, doc in _DOCS.items() if key in question_lower] or [next(iter(_DOCS.values()))]


def mock_generate(question: str, contexts: list[str]) -> tuple[str, int]:
    answer = f"Based on context, {contexts[0][:60]}"
    tokens_used = len(question.split()) + len(answer.split())
    return answer, tokens_used


def traced_rag_answer(question: str, tracer=None) -> str:
    tracer = tracer or get_tracer()
    with tracer.span("rag_request", question=question):
        with tracer.span("retrieval", k=1) as retrieval_span:
            contexts = mock_retrieve(question)
            if hasattr(retrieval_span, "metadata"):
                retrieval_span.metadata["num_docs"] = len(contexts)

        with tracer.span("generation", model="mock-llm") as gen_span:
            answer, tokens_used = mock_generate(question, contexts)
            cost_usd = round((tokens_used / 1000) * _PRICE_PER_1K_TOKENS, 6)
            if hasattr(gen_span, "metadata"):
                gen_span.metadata["tokens_used"] = tokens_used
                gen_span.metadata["cost_usd"] = cost_usd

    return answer


if __name__ == "__main__":
    tracer = get_tracer()
    print(f"Using tracer: {type(tracer).__name__}\n")

    for question in ["What does vLLM do?", "How does semantic caching help?"]:
        answer = traced_rag_answer(question, tracer=tracer)
        print(f"Q: {question}\nA: {answer}\n")

    if hasattr(tracer, "print_tree"):
        print("Trace tree (total cost/latency visible per span):")
        tracer.print_tree()
