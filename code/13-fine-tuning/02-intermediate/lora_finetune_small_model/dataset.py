from __future__ import annotations

# tiny synthetic instruction dataset, kept inline so this example needs no external data file

TRAIN_EXAMPLES: list[dict[str, str]] = [
    {"instruction": "Summarize this sentence.", "input": "The stock market rallied today after strong earnings reports.", "output": "Stocks rose on strong earnings."},
    {"instruction": "Convert to past tense.", "input": "I walk to the store.", "output": "I walked to the store."},
    {"instruction": "Answer in one word.", "input": "What color is the sky on a clear day?", "output": "Blue."},
    {"instruction": "Classify as spam or not spam.", "input": "Congratulations! You won a free prize, click here!", "output": "spam"},
    {"instruction": "Classify as spam or not spam.", "input": "Let's meet for lunch tomorrow at noon.", "output": "not spam"},
    {"instruction": "Rewrite formally.", "input": "hey can u send the file asap", "output": "Could you please send the file as soon as possible?"},
    {"instruction": "Extract the number from the text.", "input": "There are 42 apples in the basket.", "output": "42"},
    {"instruction": "Complete the analogy.", "input": "Cat is to kitten as dog is to ___.", "output": "puppy"},
    {"instruction": "Summarize this sentence.", "input": "The new policy reduces carbon emissions by 30 percent over five years.", "output": "The policy cuts emissions by 30% in five years."},
    {"instruction": "Classify as spam or not spam.", "input": "Your invoice #4521 is attached for review.", "output": "not spam"},
    {"instruction": "Convert to past tense.", "input": "She writes a letter every week.", "output": "She wrote a letter every week."},
    {"instruction": "Answer in one word.", "input": "What is the opposite of hot?", "output": "Cold."},
]

EVAL_EXAMPLES: list[dict[str, str]] = [
    {"instruction": "Classify as spam or not spam.", "input": "Click now to claim your free vacation!!!", "output": "spam"},
    {"instruction": "Convert to past tense.", "input": "He runs every morning.", "output": "He ran every morning."},
    {"instruction": "Answer in one word.", "input": "What is the opposite of up?", "output": "Down."},
]


def format_prompt(instruction: str, input_text: str) -> str:
    if input_text:
        return f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n"
    return f"### Instruction:\n{instruction}\n\n### Response:\n"


def to_text_field(example: dict[str, str]) -> str:
    return format_prompt(example["instruction"], example["input"]) + example["output"]
