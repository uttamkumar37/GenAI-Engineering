# 03 — Neural Networks & PyTorch

## Fresher

**Concepts**: tensors, `nn.Module`, forward pass, `nn.Linear`, activation functions (ReLU, GELU), `loss.backward()`, `optimizer.step()`.

**Resources**:
- [PyTorch — 60 Minute Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)

**Code** (`code/01-fresher/`):
- `first_nn.py` — 2-layer MLP classifying synthetic 2D data, training loop from scratch

**Interview questions**:
- What does `.backward()` actually compute? (Gradients of loss w.r.t. every parameter via autograd/reverse-mode differentiation.)

## Intermediate

**Concepts**: DataLoader/Dataset, batching, GPU/device management (`.to(device)`), custom loss functions, saving/loading checkpoints, basic CNN or RNN (context, not depth — heading to transformers next).

**Resources**:
- [PyTorch — Datasets & DataLoaders](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)

**Code** (`code/02-intermediate/`):
- `mnist_classifier/` — full training pipeline (Dataset, DataLoader, train/eval loop, checkpoint save/load, device-agnostic)

**Interview questions**:
- Why do we zero gradients before each backward pass? (PyTorch accumulates gradients by default — needed for gradient accumulation patterns used in LLM fine-tuning.)

## Advanced / Senior

**Concepts**: mixed precision training (`torch.cuda.amp`), gradient accumulation (simulating large batch sizes on limited GPU memory — directly relevant to fine-tuning), `torch.compile`, custom autograd functions, model parallelism concepts (conceptual only).

**Resources**:
- [PyTorch — Automatic Mixed Precision](https://pytorch.org/docs/stable/amp.html)

**Code** (`code/03-advanced/`):
- `mixed_precision_training.py`
- `gradient_accumulation.py` — train with effective batch size 64 using accumulation over batch size 8 (this exact pattern reappears verbatim in Topic 13 LoRA training)

**Interview questions**:
- You have a 24GB GPU but need an effective batch size of 128 for stable fine-tuning. How? (Gradient accumulation + mixed precision; explain the memory/throughput tradeoff.)

## Milestone

Train and checkpoint a small classifier end-to-end with a GPU-agnostic pipeline — this is the exact skeleton reused for LoRA fine-tuning in Topic 13.
