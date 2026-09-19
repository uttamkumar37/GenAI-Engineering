from __future__ import annotations

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

EFFECTIVE_BATCH_SIZE = 64
MICRO_BATCH_SIZE = 8
ACCUMULATION_STEPS = EFFECTIVE_BATCH_SIZE // MICRO_BATCH_SIZE


class TinyMLP(nn.Module):
    def __init__(self, input_dim: int = 32, hidden_dim: int = 64, output_dim: int = 2) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def make_dataloader(n_samples: int = 512, seed: int = 0) -> DataLoader:
    generator = torch.Generator().manual_seed(seed)
    x = torch.randn((n_samples, 32), generator=generator)
    y = torch.randint(0, 2, (n_samples,), generator=generator)
    dataset = TensorDataset(x, y)
    return DataLoader(dataset, batch_size=MICRO_BATCH_SIZE, shuffle=True)


def train_with_gradient_accumulation(model: nn.Module, loader: DataLoader, epochs: int = 3) -> list[float]:
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    epoch_losses = []

    for _ in range(epochs):
        optimizer.zero_grad()
        running_loss = 0.0
        n_micro_batches = 0
        for step, (images, labels) in enumerate(loader):
            logits = model(images)
            loss = loss_fn(logits, labels) / ACCUMULATION_STEPS
            loss.backward()
            running_loss += loss.item() * ACCUMULATION_STEPS
            n_micro_batches += 1

            if (step + 1) % ACCUMULATION_STEPS == 0:
                optimizer.step()
                optimizer.zero_grad()

        epoch_losses.append(running_loss / n_micro_batches)
    return epoch_losses


if __name__ == "__main__":
    model = TinyMLP()
    loader = make_dataloader()
    losses = train_with_gradient_accumulation(model, loader)
    print(f"effective batch size: {EFFECTIVE_BATCH_SIZE} (micro batch {MICRO_BATCH_SIZE} x {ACCUMULATION_STEPS} steps)")
    print(f"epoch losses: {[round(loss, 4) for loss in losses]}")
