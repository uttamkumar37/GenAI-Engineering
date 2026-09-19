from __future__ import annotations

# assumes: torch, transformers, peft, trl, datasets, accelerate installed, plus a GPU with
# enough VRAM for a ~0.5B model (a CPU can run this for a smoke test at tiny batch size only)
# API written against peft>=0.11 / trl>=0.9 — verify exact kwarg names against installed versions
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer

from dataset import TRAIN_EXAMPLES, to_text_field

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
OUTPUT_DIR = "./lora-adapter-output"


def build_dataset() -> Dataset:
    texts = [{"text": to_text_field(ex)} for ex in TRAIN_EXAMPLES]
    return Dataset.from_list(texts)


def build_lora_config() -> LoraConfig:
    return LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "v_proj"],
    )


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    lora_config = build_lora_config()
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    train_dataset = build_dataset()

    sft_config = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=1,
        save_strategy="epoch",
        max_seq_length=256,
        dataset_text_field="text",
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
    print(f"LoRA adapter saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
