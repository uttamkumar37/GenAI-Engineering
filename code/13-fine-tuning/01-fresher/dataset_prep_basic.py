from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass

RAW_EXAMPLES = [
    {"instruction": "Summarize the following text in one sentence.", "input": "The quick brown fox jumps over the lazy dog near the riverbank.", "response": "A fox jumps over a dog by the river."},
    {"instruction": "Translate to French.", "input": "Good morning", "response": "Bonjour"},
    {"instruction": "Classify the sentiment of this review.", "input": "This product exceeded my expectations!", "response": "positive"},
    {"instruction": "Write a one-line docstring for a function that adds two numbers.", "input": "", "response": "Return the sum of two numbers."},
    {"instruction": "Correct the grammar in this sentence.", "input": "She go to the market yesterday.", "response": "She went to the market yesterday."},
    {"instruction": "Extract the named entity from the sentence.", "input": "Apple announced a new product in Cupertino.", "response": "Apple, Cupertino"},
]


@dataclass(frozen=True)
class InstructionExample:
    instruction: str
    input: str
    output: str


def to_standard_format(raw: list[dict]) -> list[InstructionExample]:
    return [InstructionExample(instruction=r["instruction"], input=r["input"], output=r["response"]) for r in raw]


def write_jsonl(examples: list[InstructionExample], path: str) -> None:
    with open(path, "w") as f:
        for example in examples:
            f.write(json.dumps(asdict(example)) + "\n")


def validate_dataset(examples: list[InstructionExample]) -> list[str]:
    issues = []
    for i, ex in enumerate(examples):
        if not ex.instruction.strip():
            issues.append(f"example {i}: empty instruction")
        if not ex.output.strip():
            issues.append(f"example {i}: empty output")
    return issues


if __name__ == "__main__":
    examples = to_standard_format(RAW_EXAMPLES)
    issues = validate_dataset(examples)
    if issues:
        print("Validation issues found:", issues)
    else:
        print(f"Validated {len(examples)} examples, no issues found.")

    out_path = os.path.join(os.path.dirname(__file__), "instructions.jsonl")
    write_jsonl(examples, out_path)
    print(f"Wrote {len(examples)} examples to {out_path}")

    with open(out_path) as f:
        print("\nFirst line:", f.readline().strip())
