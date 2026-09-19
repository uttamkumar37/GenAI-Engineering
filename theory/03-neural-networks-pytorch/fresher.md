# 03 — Neural Networks & PyTorch — Fresher

**Concepts**: tensors, `nn.Module`, forward pass, `nn.Linear`, activation functions (ReLU, GELU), `loss.backward()`, `optimizer.step()`.

**Resources**:
- [PyTorch — 60 Minute Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)

**Code** (`code/03-neural-networks-pytorch/01-fresher/`):
- `first_nn.py` — 2-layer MLP classifying synthetic 2D data, training loop from scratch

**Interview questions**:
- What does `.backward()` actually compute? (Gradients of loss w.r.t. every parameter via autograd/reverse-mode differentiation.)
