from __future__ import annotations

from .extraction import Triple

try:
    import networkx as nx

    _HAS_NETWORKX = True
except ImportError:
    _HAS_NETWORKX = False


class KnowledgeGraph:
    """Thin wrapper: uses networkx.MultiDiGraph when available, else a plain dict adjacency list."""

    def __init__(self) -> None:
        if _HAS_NETWORKX:
            self._graph = nx.MultiDiGraph()
        else:
            self._out: dict[str, list[tuple[str, str]]] = {}
            self._in: dict[str, list[tuple[str, str]]] = {}

    def add_edge(self, subject: str, relation: str, obj: str) -> None:
        if _HAS_NETWORKX:
            self._graph.add_edge(subject, obj, relation=relation)
        else:
            self._out.setdefault(subject, []).append((obj, relation))
            self._in.setdefault(obj, []).append((subject, relation))
            self._out.setdefault(obj, [])
            self._in.setdefault(subject, [])

    def out_edges(self, node: str) -> list[tuple[str, str]]:
        if _HAS_NETWORKX:
            if node not in self._graph:
                return []
            return [(v, data["relation"]) for _, v, data in self._graph.out_edges(node, data=True)]
        return self._out.get(node, [])

    def in_edges(self, node: str) -> list[tuple[str, str]]:
        if _HAS_NETWORKX:
            if node not in self._graph:
                return []
            return [(u, data["relation"]) for u, _, data in self._graph.in_edges(node, data=True)]
        return self._in.get(node, [])

    @property
    def nodes(self) -> list[str]:
        if _HAS_NETWORKX:
            return list(self._graph.nodes)
        return list(set(self._out) | set(self._in))


def build_graph(triples: list[Triple]) -> KnowledgeGraph:
    graph = KnowledgeGraph()
    for triple in triples:
        graph.add_edge(triple.subject, triple.relation, triple.obj)
    return graph
