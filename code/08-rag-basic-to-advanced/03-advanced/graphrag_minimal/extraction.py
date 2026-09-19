from __future__ import annotations

import re
from dataclasses import dataclass

DOCUMENTS = [
    "Alice founded Acme Corp in 2010.",
    "Acme Corp acquired Widgets Inc in 2015.",
    "Bob works at Widgets Inc as a senior engineer.",
    "Acme Corp is headquartered in Seattle.",
]

# (regex, relation, subject_group, object_group) - a from-scratch heuristic extractor,
# not a full NLP pipeline: good enough to demonstrate graph construction, not production NER
_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^(?P<subj>[\w\s]+?) founded (?P<obj>[\w\s]+?) in \d{4}\.?$"), "founded"),
    (re.compile(r"^(?P<subj>[\w\s]+?) acquired (?P<obj>[\w\s]+?) in \d{4}\.?$"), "acquired"),
    (re.compile(r"^(?P<subj>[\w\s]+?) works at (?P<obj>[\w\s]+?) as .+\.?$"), "works_at"),
    (re.compile(r"^(?P<subj>[\w\s]+?) is headquartered in (?P<obj>[\w\s]+?)\.?$"), "headquartered_in"),
]


@dataclass
class Triple:
    subject: str
    relation: str
    obj: str
    source_text: str


def extract_triples(documents: list[str] = DOCUMENTS) -> list[Triple]:
    triples = []
    for doc in documents:
        text = doc.strip()
        for pattern, relation in _PATTERNS:
            match = pattern.match(text)
            if match:
                triples.append(
                    Triple(
                        subject=match.group("subj").strip(),
                        relation=relation,
                        obj=match.group("obj").strip(),
                        source_text=doc,
                    )
                )
                break
    return triples


if __name__ == "__main__":
    for triple in extract_triples():
        print(f"{triple.subject!r} --{triple.relation}--> {triple.obj!r}   (from: {triple.source_text})")
