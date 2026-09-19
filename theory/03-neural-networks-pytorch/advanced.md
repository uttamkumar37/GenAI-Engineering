# 03 — Neural Networks & PyTorch — Advanced / Senior

**Concepts**: mixed precision training (`torch.cuda.amp`), gradient accumulation (simulating large batch sizes on limited GPU memory — directly relevant to fine-tuning), `torch.compile`, custom autograd functions, model parallelism concepts (conceptual only).

**Resources**:
- [PyTorch — Automatic Mixed Precision](https://pytorch.org/docs/stable/amp.html)

**Code** (`code/03-neural-networks-pytorch/03-advanced/`):
- `mixed_precision_training.py`
- `gradient_accumulation.py` — train with effective batch size 64 using accumulation over batch size 8 (this exact pattern reappears verbatim in Topic 13 LoRA training)

**Interview questions**:
- You have a 24GB GPU but need an effective batch size of 128 for stable fine-tuning. How? (Gradient accumulation + mixed precision; explain the memory/throughput tradeoff.)
