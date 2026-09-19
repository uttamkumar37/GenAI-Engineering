from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

VOCAB = ["the", "cat", "dog", "sat", "ran", "quickly", "banana", "sky"]
MOCK_LOGITS = np.array([4.0, 3.5, 3.0, 2.0, 1.8, 1.0, -1.0, -2.0])


def softmax(x: NDArray[np.float64]) -> NDArray[np.float64]:
    shifted = x - np.max(x)
    exp_values = np.exp(shifted)
    return exp_values / np.sum(exp_values)


def apply_temperature(logits: NDArray[np.float64], temperature: float) -> NDArray[np.float64]:
    if temperature <= 0:
        raise ValueError("temperature must be > 0")
    return logits / temperature


def top_k_filter(probs: NDArray[np.float64], k: int) -> NDArray[np.float64]:
    if k >= len(probs):
        return probs
    top_k_indices = np.argsort(probs)[-k:]
    filtered = np.zeros_like(probs)
    filtered[top_k_indices] = probs[top_k_indices]
    return filtered / filtered.sum()


def top_p_filter(probs: NDArray[np.float64], p: float) -> NDArray[np.float64]:
    sorted_indices = np.argsort(probs)[::-1]
    sorted_probs = probs[sorted_indices]
    cumulative = np.cumsum(sorted_probs)
    cutoff = np.searchsorted(cumulative, p) + 1
    kept_indices = sorted_indices[:cutoff]
    filtered = np.zeros_like(probs)
    filtered[kept_indices] = probs[kept_indices]
    return filtered / filtered.sum()


def describe_distribution(label: str, probs: NDArray[np.float64]) -> None:
    ranked = sorted(zip(VOCAB, probs), key=lambda pair: -pair[1])
    nonzero = [(token, round(float(prob), 4)) for token, prob in ranked if prob > 1e-6]
    print(f"{label}: {nonzero}")


if __name__ == "__main__":
    base_probs = softmax(MOCK_LOGITS)
    describe_distribution("base (temp=1.0)", base_probs)

    for temperature in [0.2, 1.0, 2.0]:
        scaled_logits = apply_temperature(MOCK_LOGITS, temperature)
        probs = softmax(scaled_logits)
        describe_distribution(f"temperature={temperature}", probs)

    for k in [1, 3, 5]:
        probs = top_k_filter(base_probs, k)
        describe_distribution(f"top_k={k}", probs)

    for p in [0.5, 0.8, 0.95]:
        probs = top_p_filter(base_probs, p)
        describe_distribution(f"top_p={p}", probs)

    combined_logits = apply_temperature(MOCK_LOGITS, 0.7)
    combined_probs = top_p_filter(softmax(combined_logits), 0.9)
    describe_distribution("temperature=0.7 + top_p=0.9", combined_probs)
