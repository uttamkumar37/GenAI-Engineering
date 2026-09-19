from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def dot_product(a: NDArray[np.float64], b: NDArray[np.float64]) -> float:
    return float(np.sum(a * b))


def norm(a: NDArray[np.float64]) -> float:
    return float(np.sqrt(np.sum(a * a)))


def cosine_similarity(a: NDArray[np.float64], b: NDArray[np.float64]) -> float:
    denominator = norm(a) * norm(b)
    if denominator == 0.0:
        return 0.0
    return dot_product(a, b) / denominator


if __name__ == "__main__":
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    print("dot:", dot_product(a, b))
    print("dot (np.dot):", float(np.dot(a, b)))
    print("norm(a):", norm(a))
    print("norm (np.linalg.norm):", float(np.linalg.norm(a)))
    print("cosine similarity:", cosine_similarity(a, b))

    identical = np.array([1.0, 0.0])
    opposite = np.array([-1.0, 0.0])
    orthogonal = np.array([0.0, 1.0])
    print("cos(identical, identical):", cosine_similarity(identical, identical))
    print("cos(identical, opposite):", cosine_similarity(identical, opposite))
    print("cos(identical, orthogonal):", cosine_similarity(identical, orthogonal))
