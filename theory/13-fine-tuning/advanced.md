# 13 — Fine-Tuning — Advanced / Senior

**Concepts**: QLoRA end-to-end (4-bit quantized base + LoRA adapters) on a larger model, dataset curation/deduplication/quality filtering at scale, hyperparameter tuning for fine-tuning (rank, alpha, learning rate), merging adapters vs serving them separately, catastrophic forgetting and how to mitigate it, evaluating fine-tuned models rigorously (not just vibes).

**Resources**:
- [Hugging Face — QLoRA blog (bitsandbytes)](https://huggingface.co/blog/4bit-transformers-bitsandbytes)
- [Hugging Face — TRL advanced configs](https://huggingface.co/docs/trl/index)

**Code** (`code/13-fine-tuning/03-advanced/`):
- `qlora_finetune_pipeline/` — full pipeline: dataset curation script, QLoRA training run on a larger model, adapter merge step, before/after eval using the Topic 16 eval harness

**Interview questions**:
- You fine-tuned a model and it got better at your target task but noticeably worse at general instruction-following. What happened, and how do you fix it? (Catastrophic forgetting — mitigate with mixing general instruction data into the fine-tuning set, lower learning rate, fewer epochs, or use LoRA with conservative rank.)
