from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Document:
    doc_id: str
    content: str
    allowed_groups: set[str]  # ACL metadata attached at index time


@dataclass
class User:
    user_id: str
    groups: set[str] = field(default_factory=set)


# Simulated vector index: each document carries ACL metadata alongside its embedding (here, just
# a keyword-overlap score standing in for cosine similarity, since there's no real embedding model).
DOCUMENT_STORE: list[Document] = [
    Document("d1", "Public onboarding guide: how to set up your account.", allowed_groups={"all"}),
    Document("d2", "Engineering runbook: production database credentials rotation steps.", allowed_groups={"eng"}),
    Document(
        "d3",
        "Executive compensation report Q3: salary bands for leadership.",
        allowed_groups={"hr", "exec"},
    ),
    Document("d4", "Customer support macros for common billing questions.", allowed_groups={"support", "all"}),
]

USERS: dict[str, User] = {
    "alice_eng": User("alice_eng", groups={"eng"}),
    "bob_support": User("bob_support", groups={"support"}),
    "carol_hr": User("carol_hr", groups={"hr"}),
}


def _relevance_score(query: str, doc: Document) -> int:
    query_words = set(query.lower().split())
    doc_words = set(doc.content.lower().split())
    return len(query_words & doc_words)


def retrieve(query: str, user: User, k: int = 3) -> list[Document]:
    # Permission filtering happens HERE, at retrieval time, against the index's ACL metadata —
    # never as a post-hoc filter on an already-generated answer, since by then the model has
    # already "seen" any unauthorized content that leaked into its context window.
    accessible = [
        doc
        for doc in DOCUMENT_STORE
        if "all" in doc.allowed_groups or (doc.allowed_groups & user.groups)
    ]
    scored = sorted(accessible, key=lambda d: _relevance_score(query, d), reverse=True)
    return [d for d in scored if _relevance_score(query, d) > 0][:k]


def rag_answer(query: str, user: User) -> str:
    docs = retrieve(query, user)
    if not docs:
        return "No relevant documents found (or none you're authorized to view)."
    context = " ".join(d.content for d in docs)
    return f"Answer for {user.user_id} based on {len(docs)} doc(s): {context[:150]}"


if __name__ == "__main__":
    query = "database credentials rotation"

    for user_id in ("alice_eng", "bob_support", "carol_hr"):
        user = USERS[user_id]
        docs = retrieve(query, user)
        doc_ids = [d.doc_id for d in docs]
        print(f"{user_id} (groups={user.groups}) retrieves: {doc_ids}")
        print(f"  -> {rag_answer(query, user)}\n")

    print("Note: 'd2' (eng-only credentials runbook) is retrieved for alice_eng but never")
    print("appears in bob_support's or carol_hr's retrieved set — filtering happens before")
    print("the content ever reaches the generation step.")
