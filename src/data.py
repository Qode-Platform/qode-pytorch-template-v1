"""Dataset and DataLoader construction."""

from torch.utils.data import DataLoader
from torchvision import datasets, transforms

TRANSFORM = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])


def loaders(data_dir: str, batch_size: int) -> tuple[DataLoader, DataLoader]:
    train = datasets.MNIST(data_dir, train=True, download=True, transform=TRANSFORM)
    test = datasets.MNIST(data_dir, train=False, download=True, transform=TRANSFORM)
    return (
        DataLoader(train, batch_size=batch_size, shuffle=True, num_workers=2),
        DataLoader(test, batch_size=batch_size, num_workers=2),
    )
