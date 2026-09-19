from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np


def warmup_cosine_decay_lr(step: int, warmup_steps: int, total_steps: int, max_lr: float, min_lr: float = 0.0) -> float:
    if step < warmup_steps:
        return max_lr * (step + 1) / warmup_steps
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    progress = min(progress, 1.0)
    cosine_factor = 0.5 * (1 + math.cos(math.pi * progress))
    return min_lr + (max_lr - min_lr) * cosine_factor


def build_schedule(total_steps: int, warmup_steps: int, max_lr: float, min_lr: float = 1e-6) -> list[float]:
    return [warmup_cosine_decay_lr(step, warmup_steps, total_steps, max_lr, min_lr) for step in range(total_steps)]


if __name__ == "__main__":
    total_steps = 1000
    warmup_steps = 100
    max_lr = 3e-4

    schedule = build_schedule(total_steps, warmup_steps, max_lr)
    steps = np.arange(total_steps)

    plt.figure(figsize=(8, 4))
    plt.plot(steps, schedule)
    plt.axvline(warmup_steps, linestyle="--", color="gray", label="end of warmup")
    plt.xlabel("step")
    plt.ylabel("learning rate")
    plt.title("Warmup + Cosine Decay LR Schedule")
    plt.legend()
    plt.tight_layout()
    plt.savefig("lr_schedule.png")
    print(f"peak lr: {max(schedule):.6f} at step {int(np.argmax(schedule))}")
    print(f"final lr: {schedule[-1]:.6f}")
    print("saved plot to lr_schedule.png")
