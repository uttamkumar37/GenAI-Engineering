from __future__ import annotations

import hashlib
import json
import os

# tiny synthetic "raw" pool with intentional duplicates/low-quality rows, to exercise
# curation logic (dedup, length filtering, quality filtering) without needing a real dataset
RAW_POOL: list[dict[str, str]] = [
    {"instruction": "Summarize this.", "input": "AI is transforming how software is built.", "output": "AI is changing software development."},
    {"instruction": "Summarize this.", "input": "AI is transforming how software is built.", "output": "AI is changing software development."},  # exact dup
    {"instruction": "Translate to Spanish.", "input": "Good night", "output": "Buenas noches"},
    {"instruction": "n/a", "input": "", "output": "ok"},  # low quality: near-empty
    {"instruction": "Classify sentiment.", "input": "I absolutely love this new phone.", "output": "positive"},
    {"instruction": "Classify sentiment.", "input": "The battery life is terrible and it overheats.", "output": "negative"},
    {"instruction": "Fix grammar.", "input": "He don't know nothing about it.", "output": "He doesn't know anything about it."},
    {"instruction": "Write a haiku about autumn.", "input": "", "output": "Leaves drift to the ground / cool wind hums through empty trees / autumn settles in"},
    {"instruction": "Answer briefly.", "input": "Capital of Japan?", "output": "Tokyo"},
    {"instruction": "Answer briefly.", "input": "Capital of Japan?", "output": "Tokyo"},  # exact dup
    {"instruction": "General instruction following.", "input": "List three primary colors.", "output": "Red, blue, and yellow."},
    {"instruction": "General instruction following.", "input": "Explain what a variable is in programming.", "output": "A variable is a named storage location that holds a value which can change during program execution."},
]

MIN_OUTPUT_LENGTH = 5


def hash_example(example: dict[str, str]) -> str:
    key = f"{example['instruction']}|{example['input']}|{example['output']}"
    return hashlib.sha256(key.encode()).hexdigest()


def deduplicate(examples: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    unique = []
    for ex in examples:
        h = hash_example(ex)
        if h not in seen:
            seen.add(h)
            unique.append(ex)
    return unique


def quality_filter(examples: list[dict[str, str]]) -> list[dict[str, str]]:
    return [ex for ex in examples if len(ex["output"].strip()) >= MIN_OUTPUT_LENGTH and ex["instruction"].strip().lower() != "n/a"]


def curate(raw: list[dict[str, str]]) -> list[dict[str, str]]:
    deduped = deduplicate(raw)
    filtered = quality_filter(deduped)
    return filtered


def write_jsonl(examples: list[dict[str, str]], path: str) -> None:
    with open(path, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")


if __name__ == "__main__":
    curated = curate(RAW_POOL)
    print(f"raw pool: {len(RAW_POOL)} examples")
    print(f"after dedup+quality filter: {len(curated)} examples")

    out_path = os.path.join(os.path.dirname(__file__), "curated_dataset.jsonl")
    write_jsonl(curated, out_path)
    print(f"wrote curated dataset to {out_path}")
