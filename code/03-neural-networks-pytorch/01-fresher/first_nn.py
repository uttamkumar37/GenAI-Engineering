from __future__ import annotations

import torch
from torch import nn, optim


def make_synthetic_data(n_samples: int = 500, seed: int = 0) -> tuple[torch.Tensor, torch.Tensor]:
    generator = torch.Generator().manual_seed(seed)
    x = torch.rand((n_samples, 2), generator=generator) * 4 - 2
    labels = (x[:, 0] ** 2 + x[:, 1] ** 2 < 1.5).long()
    return x, labels


class TwoLayerMLP(nn.Module):
    def __init__(self, input_dim: int = 2, hidden_dim: int = 16, output_dim: int = 2) -> None:
        super().__init__()
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.activation = nn.ReLU()
        self.layer2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        hidden = self.activation(self.layer1(x))
        return self.layer2(hidden)


def train(model: nn.Module, x: torch.Tensor, y: torch.Tensor, epochs: int = 200, lr: float = 0.05) -> list[float]:
    optimizer = optim.SGD(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    losses = []
    for _ in range(epochs):
        optimizer.zero_grad()
        logits = model(x)
        loss = loss_fn(logits, y)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    return losses


def accuracy(model: nn.Module, x: torch.Tensor, y: torch.Tensor) -> float:
    with torch.no_grad():
        predictions = model(x).argmax(dim=1)
        return float((predictions == y).float().mean().item())


if __name__ == "__main__":
    x, y = make_synthetic_data()
    model = TwoLayerMLP()
    losses = train(model, x, y)
    print(f"initial loss: {losses[0]:.4f}")
    print(f"final loss: {losses[-1]:.4f}")
    print(f"final accuracy: {accuracy(model, x, y):.4f}")
