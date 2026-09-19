# 13 — Fine-Tuning

## Fresher

**Concepts**: what fine-tuning is and isn't (adapting weights vs prompting), when fine-tuning is even necessary, dataset format basics (instruction-response pairs).

**Resources**:
- [Hugging Face — Fine-tuning overview](https://huggingface.co/docs/transformers/training)

**Code** (`code/01-fresher/`):
- `dataset_prep_basic.py` — format a small instruction dataset into the standard JSONL structure

**Interview questions**:
- A stakeholder asks you to fine-tune a model to "make it know about our product." Is that the right approach? (Usually no — that's a RAG problem; fine-tuning is for behavior/style/format, not injecting facts that change often.)

## Intermediate

**Concepts**: full fine-tuning vs parameter-efficient fine-tuning (PEFT), LoRA mechanics (low-rank decomposition intuition — not full math), QLoRA (quantization + LoRA for memory efficiency), Hugging Face `peft` and `trl` libraries, dataset quality/size considerations, evaluation before/after fine-tuning.

**Resources**:
- [Hugging Face — PEFT docs](https://huggingface.co/docs/peft/index)
- [Hugging Face — TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer)

**Code** (`code/02-intermediate/`):
- `lora_finetune_small_model/` — LoRA fine-tune a small open model (e.g. 1-3B) on a custom instruction dataset using `peft`+`trl`, evaluate before/after on held-out examples

**Interview questions**:
- Why does LoRA make fine-tuning dramatically cheaper without (usually) sacrificing much quality? (Freezes base weights, trains small low-rank adapter matrices — orders of magnitude fewer trainable parameters, small memory footprint, mergeable back into base weights.)

## Advanced / Senior

**Concepts**: QLoRA end-to-end (4-bit quantized base + LoRA adapters) on a larger model, dataset curation/deduplication/quality filtering at scale, hyperparameter tuning for fine-tuning (rank, alpha, learning rate), merging adapters vs serving them separately, catastrophic forgetting and how to mitigate it, evaluating fine-tuned models rigorously (not just vibes).

**Resources**:
- [Hugging Face — QLoRA blog (bitsandbytes)](https://huggingface.co/blog/4bit-transformers-bitsandbytes)
- [Hugging Face — TRL advanced configs](https://huggingface.co/docs/trl/index)

**Code** (`code/03-advanced/`):
- `qlora_finetune_pipeline/` — full pipeline: dataset curation script, QLoRA training run on a larger model, adapter merge step, before/after eval using the Topic 16 eval harness

**Interview questions**:
- You fine-tuned a model and it got better at your target task but noticeably worse at general instruction-following. What happened, and how do you fix it? (Catastrophic forgetting — mitigate with mixing general instruction data into the fine-tuning set, lower learning rate, fewer epochs, or use LoRA with conservative rank.)

## Milestone project (Phase 4)

Fine-tune a small open model with QLoRA for a specific task (e.g. structured extraction from Topic 09 documents, or a custom output style), with a rigorous before/after eval report — the single most differentiating skill vs typical "RAG-only" GenAI Engineer candidates.

## Skip if behind

Full fine-tuning and hyperparameter sweeps — one solid LoRA/QLoRA run with clean eval numbers is more valuable in interviews than multiple half-documented runs.
