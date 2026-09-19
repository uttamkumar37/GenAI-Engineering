from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

D_MODEL = 16
N_LAYERS = 4


def softmax(x: NDArray[np.float64]) -> NDArray[np.float64]:
    shifted = x - np.max(x, axis=-1, keepdims=True)
    exp_values = np.exp(shifted)
    return exp_values / np.sum(exp_values, axis=-1, keepdims=True)


def project(x: NDArray[np.float64], weight: NDArray[np.float64]) -> NDArray[np.float64]:
    return x @ weight


@dataclass
class OpCounter:
    matmul_flops: int = 0

    def add_matmul(self, m: int, k: int, n: int) -> None:
        self.matmul_flops += 2 * m * k * n


@dataclass
class LayerWeights:
    w_q: NDArray[np.float64]
    w_k: NDArray[np.float64]
    w_v: NDArray[np.float64]


def make_layers(seed: int = 0) -> list[LayerWeights]:
    rng = np.random.default_rng(seed)
    return [
        LayerWeights(
            w_q=rng.normal(size=(D_MODEL, D_MODEL)),
            w_k=rng.normal(size=(D_MODEL, D_MODEL)),
            w_v=rng.normal(size=(D_MODEL, D_MODEL)),
        )
        for _ in range(N_LAYERS)
    ]


def attend(query: NDArray[np.float64], keys: NDArray[np.float64], values: NDArray[np.float64]) -> NDArray[np.float64]:
    scores = query @ keys.T / np.sqrt(D_MODEL)
    weights = softmax(scores)
    return weights @ values


def decode_naive_recompute(embeddings: NDArray[np.float64], layers: list[LayerWeights]) -> OpCounter:
    counter = OpCounter()
    seq_len = embeddings.shape[0]
    for step in range(1, seq_len + 1):
        context = embeddings[:step]
        hidden = context
        for layer in layers:
            queries = project(hidden, layer.w_q)
            keys = project(hidden, layer.w_k)
            values = project(hidden, layer.w_v)
            counter.add_matmul(step, D_MODEL, D_MODEL)
            counter.add_matmul(step, D_MODEL, D_MODEL)
            counter.add_matmul(step, D_MODEL, D_MODEL)
            output = attend(queries[-1:], keys, values)
            counter.add_matmul(1, D_MODEL, step)
            counter.add_matmul(1, step, D_MODEL)
            hidden = np.vstack([context[:-1], output]) if step > 1 else output
    return counter


@dataclass
class KVCache:
    keys: list[NDArray[np.float64]] = field(default_factory=list)
    values: list[NDArray[np.float64]] = field(default_factory=list)

    def append(self, key: NDArray[np.float64], value: NDArray[np.float64]) -> None:
        self.keys.append(key)
        self.values.append(value)

    def stacked(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        return np.vstack(self.keys), np.vstack(self.values)


def decode_with_kv_cache(embeddings: NDArray[np.float64], layers: list[LayerWeights]) -> OpCounter:
    counter = OpCounter()
    seq_len = embeddings.shape[0]
    caches = [KVCache() for _ in layers]

    for step in range(seq_len):
        token_embedding = embeddings[step : step + 1]
        hidden = token_embedding
        for layer, cache in zip(layers, caches):
            query = project(hidden, layer.w_q)
            new_key = project(hidden, layer.w_k)
            new_value = project(hidden, layer.w_v)
            counter.add_matmul(1, D_MODEL, D_MODEL)
            counter.add_matmul(1, D_MODEL, D_MODEL)
            counter.add_matmul(1, D_MODEL, D_MODEL)

            cache.append(new_key, new_value)
            all_keys, all_values = cache.stacked()

            output = attend(query, all_keys, all_values)
            counter.add_matmul(1, D_MODEL, all_keys.shape[0])
            counter.add_matmul(1, all_keys.shape[0], D_MODEL)
            hidden = output
    return counter


if __name__ == "__main__":
    rng = np.random.default_rng(seed=1)
    seq_len = 20
    embeddings = rng.normal(size=(seq_len, D_MODEL))
    layers = make_layers()

    naive = decode_naive_recompute(embeddings, layers)
    cached = decode_with_kv_cache(embeddings, layers)

    print(f"sequence length: {seq_len}, layers: {N_LAYERS}, d_model: {D_MODEL}")
    print(f"naive recompute matmul FLOPs: {naive.matmul_flops:,}")
    print(f"KV-cached matmul FLOPs:       {cached.matmul_flops:,}")
    print(f"speedup factor: {naive.matmul_flops / cached.matmul_flops:.2f}x")
