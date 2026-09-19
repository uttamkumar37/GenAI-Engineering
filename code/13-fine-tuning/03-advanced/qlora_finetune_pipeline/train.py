from __future__ import annotations

# assumes: torch (CUDA build), transformers, peft, trl, datasets, accelerate, bitsandbytes
# installed, plus an actual GPU — 4-bit quantization via bitsandbytes has no CPU/MPS backend
# API written against peft>=0.11 / trl>=0.9 / bitsandbytes>=0.43 — verify against installed versions
import json
import os

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"  # larger model than the intermediate example, per the QLoRA use case
OUTPUT_DIR = "./qlora-adapter-output"
CURATED_DATASET_PATH = os.path.join(os.path.dirname(__file__), "curated_dataset.jsonl")

# a small slice of general-purpose instructions mixed into the target-domain data to
# mitigate catastrophic forgetting (the theory doc's mitigation for narrowing too hard)
GENERAL_INSTRUCTION_MIX: list[dict[str, str]] = [
    {"instruction": "Answer briefly.", "input": "What is 9 + 10?", "output": "19"},
    {"instruction": "General instruction following.", "input": "Name two planets in the solar system.", "output": "Mars and Jupiter."},
    {"instruction": "General instruction following.", "input": "What does HTTP stand for?", "output": "HyperText Transfer Protocol."},
]


def load_curated_dataset() -> list[dict[str, str]]:
    if not os.path.exists(CURATED_DATASET_PATH):
        raise FileNotFoundError("run curate.py first to produce curated_dataset.jsonl")
    with open(CURATED_DATASET_PATH) as f:
        return [json.loads(line) for line in f if line.strip()]


def format_prompt(instruction: str, input_text: str, output_text: str) -> str:
    body = f"### Instruction:\n{instruction}\n\n"
    if input_text:
        body += f"### Input:\n{input_text}\n\n"
    return body + f"### Response:\n{output_text}"


def build_dataset() -> Dataset:
    curated = load_curated_dataset()
    combined = curated + GENERAL_INSTRUCTION_MIX
    texts = [{"text": format_prompt(ex["instruction"], ex["input"], ex["output"])} for ex in combined]
    return Dataset.from_list(texts)


def build_bnb_config() -> BitsAndBytesConfig:
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )


def build_lora_config(rank: int = 16, alpha: int = 32) -> LoraConfig:
    # conservative rank keeps the adapter small and reduces overfitting/forgetting risk
    return LoraConfig(
        r=rank,
        lora_alpha=alpha,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=build_bnb_config(),
        device_map="auto",
    )
    model = prepare_model_for_kbit_training(model)

    lora_config = build_lora_config()
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    train_dataset = build_dataset()

    sft_config = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=2,  # fewer epochs to reduce catastrophic forgetting
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=1e-4,  # lower LR than full fine-tuning for the same reason
        logging_steps=1,
        save_strategy="epoch",
        max_seq_length=512,
        dataset_text_field="text",
        bf16=True,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        args=sft_config,
        train_dataset=train_dataset,
        processing_class=tokenizer,
    )

    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"QLoRA adapter saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
