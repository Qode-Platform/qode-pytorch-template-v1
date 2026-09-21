import torch

from src.model import SmallCNN


def test_forward_shape():
    out = SmallCNN(num_classes=10)(torch.randn(4, 1, 28, 28))
    assert out.shape == (4, 10)


def test_backward_produces_grads():
    model = SmallCNN()
    model(torch.randn(2, 1, 28, 28)).sum().backward()
    assert all(p.grad is not None for p in model.parameters() if p.requires_grad)
