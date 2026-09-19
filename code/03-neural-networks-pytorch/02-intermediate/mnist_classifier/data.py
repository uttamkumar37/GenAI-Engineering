from __future__ import annotations

from pathlib import Path

import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms

DATA_DIR = Path(__file__).parent / "data"

TRANSFORM = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])


def get_mnist_datasets() -> tuple[Dataset, Dataset]:
    train_set = datasets.MNIST(root=str(DATA_DIR), train=True, download=True, transform=TRANSFORM)
    test_set = datasets.MNIST(root=str(DATA_DIR), train=False, download=True, transform=TRANSFORM)
    return train_set, test_set


def get_dataloaders(batch_size: int = 64) -> tuple[DataLoader, DataLoader]:
    train_set, test_set = get_mnist_datasets()
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader


class SyntheticDigitsDataset(Dataset):
    def __init__(self, n_samples: int = 512, seed: int = 0) -> None:
        generator = torch.Generator().manual_seed(seed)
        self.images = torch.rand((n_samples, 1, 28, 28), generator=generator)
        self.labels = torch.randint(0, 10, (n_samples,), generator=generator)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.images[index], self.labels[index]
