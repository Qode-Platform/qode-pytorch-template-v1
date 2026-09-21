"""Training loop: `python -m src.train --config configs/default.yaml`."""

import argparse
from pathlib import Path

import torch
import yaml
from torch import nn

from src.data import loaders
from src.model import SmallCNN


def device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train_one_epoch(model, loader, optimizer, loss_fn, dev) -> float:
    model.train()
    total = 0.0
    for images, targets in loader:
        images, targets = images.to(dev), targets.to(dev)
        optimizer.zero_grad(set_to_none=True)
        loss = loss_fn(model(images), targets)
        loss.backward()
        optimizer.step()
        total += loss.item() * images.size(0)
    return total / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, dev) -> float:
    model.eval()
    correct = 0
    for images, targets in loader:
        images, targets = images.to(dev), targets.to(dev)
        correct += (model(images).argmax(dim=1) == targets).sum().item()
    return correct / len(loader.dataset)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    cfg = yaml.safe_load(Path(parser.parse_args().config).read_text())

    dev = device()
    model = SmallCNN(cfg["num_classes"]).to(dev)
    train_loader, test_loader = loaders(cfg["data_dir"], cfg["batch_size"])
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg["lr"])
    loss_fn = nn.CrossEntropyLoss()

    ckpt_dir = Path(cfg["checkpoint_dir"])
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, cfg["epochs"] + 1):
        loss = train_one_epoch(model, train_loader, optimizer, loss_fn, dev)
        acc = evaluate(model, test_loader, dev)
        print(f"epoch {epoch}: loss={loss:.4f} test_acc={acc:.4f}")
        torch.save(model.state_dict(), ckpt_dir / f"epoch-{epoch}.pt")


if __name__ == "__main__":
    main()
