from __future__ import annotations

from collections import deque

from .graph import KnowledgeGraph

Hop = tuple[str, str, str, str]  # (from_node, relation, to_node, direction)


def multi_hop_search(
    graph: KnowledgeGraph, start_node: str, target_relation: str, max_hops: int = 4
) -> list[Hop] | None:
    # BFS over both outgoing and incoming edges (undirected traversal, direction-labeled),
    # returning the first path that ends in an edge carrying `target_relation`
    visited = {start_node}
    queue: deque[tuple[str, list[Hop]]] = deque([(start_node, [])])
    while queue:
        node, path = queue.popleft()
        if len(path) >= max_hops:
            continue
        for target, relation in graph.out_edges(node):
            hop: Hop = (node, relation, target, "out")
            if relation == target_relation:
                return path + [hop]
            if target not in visited:
                visited.add(target)
                queue.append((target, path + [hop]))
        for source, relation in graph.in_edges(node):
            hop = (node, relation, source, "in")
            if relation == target_relation:
                return path + [hop]
            if source not in visited:
                visited.add(source)
                queue.append((source, path + [hop]))
    return None


def explain_path(path: list[Hop]) -> str:
    parts = []
    for from_node, relation, to_node, direction in path:
        arrow = f"{from_node} --{relation}--> {to_node}" if direction == "out" else f"{to_node} --{relation}--> {from_node}"
        parts.append(arrow)
    return " ; ".join(parts)
