from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

rng = np.random.default_rng(seed=42)

N_SAMPLES = 200
TRUE_W, TRUE_B = 3.0, -1.5
X = rng.uniform(-5, 5, size=N_SAMPLES)
NOISE = rng.normal(0, 1.0, size=N_SAMPLES)
Y = TRUE_W * X + TRUE_B + NOISE


def mse_loss(w: float, b: float, x: NDArray[np.float64], y: NDArray[np.float64]) -> float:
    predictions = w * x + b
    return float(np.mean((predictions - y) ** 2))


def gradients(w: float, b: float, x: NDArray[np.float64], y: NDArray[np.float64]) -> tuple[float, float]:
    predictions = w * x + b
    error = predictions - y
    grad_w = float(np.mean(2 * error * x))
    grad_b = float(np.mean(2 * error))
    return grad_w, grad_b


def batch_gradient_descent(lr: float = 0.01, epochs: int = 100) -> list[float]:
    w, b = 0.0, 0.0
    losses = []
    for _ in range(epochs):
        grad_w, grad_b = gradients(w, b, X, Y)
        w -= lr * grad_w
        b -= lr * grad_b
        losses.append(mse_loss(w, b, X, Y))
    return losses


def stochastic_gradient_descent(lr: float = 0.01, epochs: int = 100) -> list[float]:
    w, b = 0.0, 0.0
    losses = []
    for _ in range(epochs):
        indices = rng.permutation(N_SAMPLES)
        for i in indices:
            x_i, y_i = X[i : i + 1], Y[i : i + 1]
            grad_w, grad_b = gradients(w, b, x_i, y_i)
            w -= lr * grad_w
            b -= lr * grad_b
        losses.append(mse_loss(w, b, X, Y))
    return losses


def mini_batch_gradient_descent(lr: float = 0.01, epochs: int = 100, batch_size: int = 16) -> list[float]:
    w, b = 0.0, 0.0
    losses = []
    for _ in range(epochs):
        indices = rng.permutation(N_SAMPLES)
        for start in range(0, N_SAMPLES, batch_size):
            batch_idx = indices[start : start + batch_size]
            grad_w, grad_b = gradients(w, b, X[batch_idx], Y[batch_idx])
            w -= lr * grad_w
            b -= lr * grad_b
        losses.append(mse_loss(w, b, X, Y))
    return losses


if __name__ == "__main__":
    batch_losses = batch_gradient_descent()
    sgd_losses = stochastic_gradient_descent()
    mini_batch_losses = mini_batch_gradient_descent()

    print(f"batch gd final loss:      {batch_losses[-1]:.4f}")
    print(f"sgd final loss:           {sgd_losses[-1]:.4f}")
    print(f"mini-batch gd final loss: {mini_batch_losses[-1]:.4f}")
    print(f"true w={TRUE_W}, b={TRUE_B}")
