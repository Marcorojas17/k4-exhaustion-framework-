# src/experimental/__init__.py
from .dynamic_loader import discover_experimental_engines
from .vic_cipher import VicFractionalEngine

__all__ = ["discover_experimental_engines", "VicFractionalEngine"]
