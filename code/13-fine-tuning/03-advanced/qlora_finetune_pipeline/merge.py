from __future__ import annotations

# assumes: torch, transformers, peft installed; merging a 4-bit-trained adapter requires
# reloading the base model in full precision (fp16/bf16) since merged weights can't stay 4-bit
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from train import MODEL_NAME, OUTPUT_DIR

MERGED_OUTPUT_DIR = "./qlora-merged-model"


def merge_and_save() -> None:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # reload base model in bf16 (not 4-bit) — you cannot merge LoRA deltas into quantized weights
    base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype="bfloat16")
    peft_model = PeftModel.from_pretrained(base_model, OUTPUT_DIR)

    merged_model = peft_model.merge_and_unload()
    merged_model.save_pretrained(MERGED_OUTPUT_DIR)
    tokenizer.save_pretrained(MERGED_OUTPUT_DIR)
    print(f"Merged model saved to {MERGED_OUTPUT_DIR}")
    print("Note: serving the adapter separately (base + LoRA) instead of merging saves disk")
    print("space when running many task-specific adapters off one shared base model.")


if __name__ == "__main__":
    merge_and_save()
