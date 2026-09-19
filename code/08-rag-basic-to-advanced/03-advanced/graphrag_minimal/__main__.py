from __future__ import annotations

from .extraction import extract_triples
from .graph import build_graph
from .traversal import explain_path, multi_hop_search


def answer_multi_hop_question() -> None:
    triples = extract_triples()
    graph = build_graph(triples)

    # A flat single-hop vector RAG fails here: no single document mentions both
    # "Bob" and "Alice" - the connection only exists by chaining three separate facts.
    question = "Who founded the company where Bob works?"
    path = multi_hop_search(graph, start_node="Bob", target_relation="founded")

    print(f"Question: {question}")
    if path:
        answer = path[-1][2]
        print(f"Answer: {answer}")
        print(f"Reasoning path: {explain_path(path)}")
    else:
        print("No connecting path found within the hop limit.")


if __name__ == "__main__":
    answer_multi_hop_question()
