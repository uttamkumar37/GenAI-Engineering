from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F
from numpy.typing import NDArray


def softmax(logits: NDArray[np.float64]) -> NDArray[np.float64]:
    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    exp_values = np.exp(shifted)
    return exp_values / np.sum(exp_values, axis=-1, keepdims=True)


def cross_entropy(probs: NDArray[np.float64], targets: NDArray[np.int64]) -> float:
    n = probs.shape[0]
    clipped = np.clip(probs[np.arange(n), targets], 1e-12, 1.0)
    return float(-np.mean(np.log(clipped)))


def softmax_cross_entropy_from_logits(logits: NDArray[np.float64], targets: NDArray[np.int64]) -> float:
    probs = softmax(logits)
    return cross_entropy(probs, targets)


if __name__ == "__main__":
    rng = np.random.default_rng(seed=0)
    logits = rng.normal(size=(4, 5))
    targets = np.array([0, 2, 1, 4])

    numpy_probs = softmax(logits)
    numpy_loss = softmax_cross_entropy_from_logits(logits, targets)

    torch_logits = torch.tensor(logits)
    torch_targets = torch.tensor(targets)
    torch_probs = F.softmax(torch_logits, dim=-1).numpy()
    torch_loss = F.cross_entropy(torch_logits, torch_targets).item()

    print("numpy softmax:\n", numpy_probs)
    print("torch softmax:\n", torch_probs)
    print("max abs diff (softmax):", np.max(np.abs(numpy_probs - torch_probs)))
    print(f"numpy cross-entropy: {numpy_loss:.6f}")
    print(f"torch cross-entropy: {torch_loss:.6f}")
    print(f"abs diff (loss): {abs(numpy_loss - torch_loss):.8f}")
