from __future__ import annotations

import tiktoken

SAMPLES: list[tuple[str, str]] = [
    ("english", "The quick brown fox jumps over the lazy dog."),
    ("numbers", "The invoice total is 1234567.89 dollars, due on 2026-09-20."),
    ("hindi", "आर्टिफिशियल इंटेलिजेंस तेजी से बदल रहा है।"),
    ("chinese", "人工智能正在迅速改变世界。"),
    ("whitespace", "word1     word2\tword3\nword4"),
    ("code", "def add(a: int, b: int) -> int:\n    return a + b"),
]


def compare_char_vs_token_counts(encoding_name: str = "cl100k_base") -> None:
    encoding = tiktoken.get_encoding(encoding_name)
    print(f"encoding: {encoding_name}\n")
    for label, text in SAMPLES:
        tokens = encoding.encode(text)
        char_count = len(text)
        token_count = len(tokens)
        ratio = char_count / token_count if token_count else 0.0
        print(f"[{label}] chars={char_count:>4} tokens={token_count:>4} chars/token={ratio:.2f}")
        decoded_pieces = [encoding.decode([token]) for token in tokens[:10]]
        print(f"  first pieces: {decoded_pieces}")


if __name__ == "__main__":
    compare_char_vs_token_counts()
