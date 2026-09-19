from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def naive_softmax(logits: NDArray[np.float64]) -> NDArray[np.float64]:
    exp_values = np.exp(logits)
    return exp_values / np.sum(exp_values)


def stable_softmax(logits: NDArray[np.float64]) -> NDArray[np.float64]:
    shifted = logits - np.max(logits)
    exp_values = np.exp(shifted)
    return exp_values / np.sum(exp_values)


def naive_log_sum_exp(logits: NDArray[np.float64]) -> float:
    return float(np.log(np.sum(np.exp(logits))))


def stable_log_sum_exp(logits: NDArray[np.float64]) -> float:
    max_val = np.max(logits)
    return float(max_val + np.log(np.sum(np.exp(logits - max_val))))


if __name__ == "__main__":
    safe_logits = np.array([1.0, 2.0, 3.0])
    print("safe logits, naive softmax:", naive_softmax(safe_logits))
    print("safe logits, stable softmax:", stable_softmax(safe_logits))

    large_logits = np.array([1000.0, 1001.0, 1002.0])
    with np.errstate(over="ignore", invalid="ignore"):
        naive_result = naive_softmax(large_logits)
    print("\nlarge logits, naive softmax (overflows to nan):", naive_result)
    print("large logits, stable softmax:", stable_softmax(large_logits))

    print("\nnaive log-sum-exp (large logits):")
    with np.errstate(over="ignore"):
        print(naive_log_sum_exp(large_logits))
    print("stable log-sum-exp (large logits):", stable_log_sum_exp(large_logits))
