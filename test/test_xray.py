import torch

from diffdrr import Detector

def test_Detector():
    try:
        detector = Detector(100, 100, 7.5e-2, 7.5e-2, device="cuda")
    except ValueError:
        detector = Detector(100, 100, 7.5e-2, 7.5e-2, device="cpu")
    sdr = torch.tensor([200.0])
    rotations = torch.rand(4, 3)
    translations = torch.rand(4, 3)
    source, target = detector.make_xrays(sdr, rotations, translations)
    assert source.shape == (4, 3)
    assert target.shape == (4, 100, 100, 3)