from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


def softmax(x: NDArray[np.float64], axis: int = -1) -> NDArray[np.float64]:
    shifted = x - np.max(x, axis=axis, keepdims=True)
    exp_values = np.exp(shifted)
    return exp_values / np.sum(exp_values, axis=axis, keepdims=True)


def scaled_dot_product_attention(
    query: NDArray[np.float64],
    key: NDArray[np.float64],
    value: NDArray[np.float64],
    mask: NDArray[np.bool_] | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    d_k = query.shape[-1]
    scores = query @ key.T / np.sqrt(d_k)
    if mask is not None:
        scores = np.where(mask, scores, -np.inf)
    weights = softmax(scores, axis=-1)
    output = weights @ value
    return output, weights


def causal_mask(seq_len: int) -> NDArray[np.bool_]:
    return np.tril(np.ones((seq_len, seq_len), dtype=bool))


def plot_attention_heatmap(weights: NDArray[np.float64], tokens: list[str], path: str = "attention_heatmap.png") -> None:
    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(weights, cmap="viridis")
    ax.set_xticks(range(len(tokens)))
    ax.set_yticks(range(len(tokens)))
    ax.set_xticklabels(tokens, rotation=45, ha="right")
    ax.set_yticklabels(tokens)
    ax.set_xlabel("key/value position")
    ax.set_ylabel("query position")
    ax.set_title("Scaled Dot-Product Attention Weights")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path)


if __name__ == "__main__":
    rng = np.random.default_rng(seed=0)
    tokens = ["the", "cat", "sat", "on", "mat"]
    seq_len, d_model = len(tokens), 8

    embeddings = rng.normal(size=(seq_len, d_model))
    query = embeddings
    key = embeddings
    value = embeddings

    output, weights = scaled_dot_product_attention(query, key, value)
    print("attention weights (no mask):\n", np.round(weights, 3))

    masked_output, masked_weights = scaled_dot_product_attention(query, key, value, mask=causal_mask(seq_len))
    print("\nattention weights (causal mask):\n", np.round(masked_weights, 3))

    plot_attention_heatmap(weights, tokens)
    print("\nsaved heatmap to attention_heatmap.png")
