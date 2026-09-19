# 13 — Fine-Tuning — Intermediate

**Concepts**: full fine-tuning vs parameter-efficient fine-tuning (PEFT), LoRA mechanics (low-rank decomposition intuition — not full math), QLoRA (quantization + LoRA for memory efficiency), Hugging Face `peft` and `trl` libraries, dataset quality/size considerations, evaluation before/after fine-tuning.

**Resources**:
- [Hugging Face — PEFT docs](https://huggingface.co/docs/peft/index)
- [Hugging Face — TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer)

**Code** (`code/13-fine-tuning/02-intermediate/`):
- `lora_finetune_small_model/` — LoRA fine-tune a small open model (e.g. 1-3B) on a custom instruction dataset using `peft`+`trl`, evaluate before/after on held-out examples

**Interview questions**:
- Why does LoRA make fine-tuning dramatically cheaper without (usually) sacrificing much quality? (Freezes base weights, trains small low-rank adapter matrices — orders of magnitude fewer trainable parameters, small memory footprint, mergeable back into base weights.)
