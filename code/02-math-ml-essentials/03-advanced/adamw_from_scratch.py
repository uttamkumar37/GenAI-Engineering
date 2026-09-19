from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


class AdamW:
    def __init__(
        self,
        n_params: int,
        lr: float = 0.001,
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8,
        weight_decay: float = 0.01,
    ) -> None:
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.weight_decay = weight_decay
        self.m = np.zeros(n_params)
        self.v = np.zeros(n_params)
        self.t = 0

    def step(self, params: NDArray[np.float64], grads: NDArray[np.float64]) -> NDArray[np.float64]:
        self.t += 1
        self.m = self.beta1 * self.m + (1 - self.beta1) * grads
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grads**2)

        m_hat = self.m / (1 - self.beta1**self.t)
        v_hat = self.v / (1 - self.beta2**self.t)

        decoupled_decay = self.lr * self.weight_decay * params
        adaptive_update = self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
        return params - adaptive_update - decoupled_decay


def rosenbrock_grad(params: NDArray[np.float64]) -> NDArray[np.float64]:
    x, y = params
    dx = -2 * (1 - x) - 400 * x * (y - x**2)
    dy = 200 * (y - x**2)
    return np.array([dx, dy])


if __name__ == "__main__":
    params = np.array([-1.5, 2.0])
    optimizer = AdamW(n_params=2, lr=0.05, weight_decay=0.001)

    for step in range(500):
        grads = rosenbrock_grad(params)
        params = optimizer.step(params, grads)
        if step % 100 == 0:
            print(f"step {step}: params={params}, loss={(1 - params[0]) ** 2 + 100 * (params[1] - params[0] ** 2) ** 2:.6f}")

    print(f"final params: {params} (target: [1.0, 1.0])")
