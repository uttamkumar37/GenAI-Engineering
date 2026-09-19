from __future__ import annotations

# assumes: torch, transformers, peft installed, plus a trained adapter/merged model from
# train.py or merge.py; reuses the Topic 16 eval harness's EvalCase/EvalResult contract
import os
import sys

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from train import MODEL_NAME, OUTPUT_DIR

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "16-evaluation", "01-fresher")
)
from simple_eval_harness import EvalCase, EvalResult  # noqa: E402

EVAL_CASES: list[EvalCase] = [
    EvalCase("Classify sentiment: I absolutely love this new phone.", must_include=["positive"]),
    EvalCase("Classify sentiment: The battery life is terrible.", must_include=["negative"]),
    EvalCase("Answer briefly. Capital of Japan?", must_include=["Tokyo"]),
    # general-instruction-following probe, to catch catastrophic forgetting of non-target skills
    EvalCase("What is 9 + 10?", must_include=["19"]),
]


def generate(model, tokenizer, prompt: str, max_new_tokens: int = 20) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    return tokenizer.decode(output_ids[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True).strip()


def run_case_against_model(case: EvalCase, model, tokenizer) -> EvalResult:
    answer = generate(model, tokenizer, case.question)
    reasons: list[str] = []
    passed = True
    for phrase in case.must_include:
        if phrase.lower() not in answer.lower():
            passed = False
            reasons.append(f"missing expected phrase: {phrase!r}")
    for phrase in case.must_not_include:
        if phrase.lower() in answer.lower():
            passed = False
            reasons.append(f"contains forbidden phrase: {phrase!r}")
    return EvalResult(case=case, answer=answer, passed=passed, reasons=reasons)


def run_suite_against_model(cases: list[EvalCase], model, tokenizer, label: str) -> None:
    results = [run_case_against_model(c, model, tokenizer) for c in cases]
    passed_count = sum(r.passed for r in results)
    print(f"\n[{label}] {passed_count}/{len(results)} cases passed")
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"  {status}  {result.case.question} -> {result.answer!r}")


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    run_suite_against_model(EVAL_CASES, base_model, tokenizer, label="base model (before QLoRA)")

    fine_tuned = PeftModel.from_pretrained(base_model, OUTPUT_DIR)
    run_suite_against_model(EVAL_CASES, fine_tuned, tokenizer, label="QLoRA fine-tuned (after)")


if __name__ == "__main__":
    main()
