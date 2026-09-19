from __future__ import annotations

import torch
from torch import nn


class MNISTClassifier(nn.Module):
    def __init__(self, num_classes: int = 10) -> None:
        super().__init__()
        self.flatten = nn.Flatten()
        self.net = nn.Sequential(
            nn.Linear(28 * 28, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(self.flatten(x))
