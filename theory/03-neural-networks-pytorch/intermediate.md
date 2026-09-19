# 03 — Neural Networks & PyTorch — Intermediate

**Concepts**: DataLoader/Dataset, batching, GPU/device management (`.to(device)`), custom loss functions, saving/loading checkpoints, basic CNN or RNN (context, not depth — heading to transformers next).

**Resources**:
- [PyTorch — Datasets & DataLoaders](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)

**Code** (`code/03-neural-networks-pytorch/02-intermediate/`):
- `mnist_classifier/` — full training pipeline (Dataset, DataLoader, train/eval loop, checkpoint save/load, device-agnostic)

**Interview questions**:
- Why do we zero gradients before each backward pass? (PyTorch accumulates gradients by default — needed for gradient accumulation patterns used in LLM fine-tuning.)
