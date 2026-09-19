# 13 — Fine-Tuning — Fresher

**Concepts**: what fine-tuning is and isn't (adapting weights vs prompting), when fine-tuning is even necessary, dataset format basics (instruction-response pairs).

**Resources**:
- [Hugging Face — Fine-tuning overview](https://huggingface.co/docs/transformers/training)

**Code** (`code/13-fine-tuning/01-fresher/`):
- `dataset_prep_basic.py` — format a small instruction dataset into the standard JSONL structure

**Interview questions**:
- A stakeholder asks you to fine-tune a model to "make it know about our product." Is that the right approach? (Usually no — that's a RAG problem; fine-tuning is for behavior/style/format, not injecting facts that change often.)
