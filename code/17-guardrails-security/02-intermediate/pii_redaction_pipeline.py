from __future__ import annotations

import re
from dataclasses import dataclass

# Regex-based PII detection (no `presidio`/spaCy dependency needed). Presidio would add NER-based
# detection for names/locations; this covers the common structured-PII cases with plain regex.

_PATTERNS: dict[str, re.Pattern[str]] = {
    "EMAIL": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "PHONE": re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "IP_ADDRESS": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}


@dataclass
class PIIMatch:
    label: str
    value: str
    start: int
    end: int


def detect_pii(text: str) -> list[PIIMatch]:
    matches: list[PIIMatch] = []
    for label, pattern in _PATTERNS.items():
        for m in pattern.finditer(text):
            matches.append(PIIMatch(label=label, value=m.group(), start=m.start(), end=m.end()))
    matches.sort(key=lambda m: m.start)
    return _drop_overlapping(matches)


def _drop_overlapping(matches: list[PIIMatch]) -> list[PIIMatch]:
    # Some patterns overlap (e.g. a phone-shaped substring inside a longer credit-card match);
    # keep the longest match at each position.
    kept: list[PIIMatch] = []
    for m in matches:
        if any(m.start < k.end and m.end > k.start for k in kept):
            continue
        kept.append(m)
    return kept


def redact(text: str, matches: list[PIIMatch] | None = None) -> str:
    matches = matches if matches is not None else detect_pii(text)
    result = text
    for m in sorted(matches, key=lambda m: m.start, reverse=True):
        result = result[: m.start] + f"[REDACTED_{m.label}]" + result[m.end :]
    return result


if __name__ == "__main__":
    sample = (
        "Hi, please update my account. My email is jane.doe@example.com and my "
        "phone is (555) 123-4567. SSN on file: 123-45-6789. Server IP: 10.0.0.42."
    )

    found = detect_pii(sample)
    print("Detected PII:")
    for match in found:
        print(f"  {match.label}: {match.value!r} at [{match.start}:{match.end}]")

    print("\nRedacted text:")
    print(redact(sample, found))
