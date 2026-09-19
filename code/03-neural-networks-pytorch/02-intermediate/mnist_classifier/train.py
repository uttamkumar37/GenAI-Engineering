from __future__ import annotations

from pathlib import Path

import torch
from torch import nn, optim
from torch.utils.data import DataLoader

from .data import SyntheticDigitsDataset, get_dataloaders
from .model import MNISTClassifier

CHECKPOINT_PATH = Path(__file__).parent / "checkpoint.pt"


def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: optim.Optimizer,
    loss_fn: nn.Module,
    device: torch.device,
) -> float:
    model.train()
    running_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        logits = model(images)
        loss = loss_fn(logits, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * images.size(0)
    return running_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader, loss_fn: nn.Module, device: torch.device) -> tuple[float, float]:
    model.eval()
    running_loss = 0.0
    correct = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        logits = model(images)
        loss = loss_fn(logits, labels)
        running_loss += loss.item() * images.size(0)
        correct += (logits.argmax(dim=1) == labels).sum().item()
    n = len(loader.dataset)
    return running_loss / n, correct / n


def save_checkpoint(model: nn.Module, optimizer: optim.Optimizer, epoch: int, path: Path = CHECKPOINT_PATH) -> None:
    torch.save(
        {"epoch": epoch, "model_state": model.state_dict(), "optimizer_state": optimizer.state_dict()},
        path,
    )


def load_checkpoint(model: nn.Module, optimizer: optim.Optimizer, path: Path = CHECKPOINT_PATH) -> int:
    checkpoint = torch.load(path, map_location="cpu")
    model.load_state_dict(checkpoint["model_state"])
    optimizer.load_state_dict(checkpoint["optimizer_state"])
    return checkpoint["epoch"]


def run_training(epochs: int = 3, use_real_mnist: bool = False) -> None:
    device = get_device()
    model = MNISTClassifier().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    if use_real_mnist:
        train_loader, test_loader = get_dataloaders()
    else:
        train_set = SyntheticDigitsDataset(n_samples=512, seed=0)
        test_set = SyntheticDigitsDataset(n_samples=128, seed=1)
        train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
        test_loader = DataLoader(test_set, batch_size=64, shuffle=False)

    for epoch in range(epochs):
        train_loss = train_one_epoch(model, train_loader, optimizer, loss_fn, device)
        val_loss, val_accuracy = evaluate(model, test_loader, loss_fn, device)
        print(f"epoch {epoch + 1}/{epochs}: train_loss={train_loss:.4f} val_loss={val_loss:.4f} val_acc={val_accuracy:.4f}")
        save_checkpoint(model, optimizer, epoch)

    restored_model = MNISTClassifier().to(device)
    restored_optimizer = optim.Adam(restored_model.parameters(), lr=1e-3)
    last_epoch = load_checkpoint(restored_model, restored_optimizer)
    print(f"restored checkpoint from epoch {last_epoch}")


if __name__ == "__main__":
    run_training(epochs=3, use_real_mnist=False)
