from __future__ import annotations

import torch
from torch import nn, optim


class TinyMLP(nn.Module):
    def __init__(self, input_dim: int = 128, hidden_dim: int = 256, output_dim: int = 10) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def train_with_mixed_precision(
    model: nn.Module,
    x: torch.Tensor,
    y: torch.Tensor,
    device: torch.device,
    epochs: int = 5,
) -> list[float]:
    model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    scaler = torch.amp.GradScaler(device.type, enabled=device.type == "cuda")
    losses = []

    for _ in range(epochs):
        optimizer.zero_grad()
        with torch.amp.autocast(device_type=device.type, enabled=device.type == "cuda"):
            logits = model(x)
            loss = loss_fn(logits, y)
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        losses.append(loss.item())
    return losses


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    generator = torch.Generator().manual_seed(0)
    x = torch.randn((64, 128), generator=generator).to(device)
    y = torch.randint(0, 10, (64,), generator=generator).to(device)

    model = TinyMLP()
    losses = train_with_mixed_precision(model, x, y, device)
    print(f"device: {device}")
    print(f"losses: {[round(loss, 4) for loss in losses]}")
