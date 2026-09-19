from __future__ import annotations

# assumes: torch, transformers, peft installed, plus the base model / adapter downloaded or
# trained locally (see train.py) — CPU inference works for a 0.5B model, just slowly
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from dataset import EVAL_EXAMPLES, format_prompt
from train import MODEL_NAME, OUTPUT_DIR


def generate(model, tokenizer, prompt: str, max_new_tokens: int = 20) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    generated = tokenizer.decode(output_ids[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True)
    return generated.strip()


def exact_match_score(predictions: list[str], references: list[str]) -> float:
    correct = sum(1 for p, r in zip(predictions, references) if p.strip().lower() == r.strip().lower())
    return correct / len(references) if references else 0.0


def evaluate_model(model, tokenizer, label: str) -> None:
    predictions = []
    for ex in EVAL_EXAMPLES:
        prompt = format_prompt(ex["instruction"], ex["input"])
        predictions.append(generate(model, tokenizer, prompt))

    references = [ex["output"] for ex in EVAL_EXAMPLES]
    score = exact_match_score(predictions, references)
    print(f"\n[{label}] exact-match score: {score:.2f}")
    for ex, pred in zip(EVAL_EXAMPLES, predictions):
        print(f"  instruction={ex['instruction']!r} input={ex['input']!r} -> pred={pred!r} expected={ex['output']!r}")


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    evaluate_model(base_model, tokenizer, label="base model (before fine-tuning)")

    fine_tuned_model = PeftModel.from_pretrained(base_model, OUTPUT_DIR)
    evaluate_model(fine_tuned_model, tokenizer, label="LoRA fine-tuned (after)")


if __name__ == "__main__":
    main()
