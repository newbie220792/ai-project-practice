from .imou_utils import _mask_string, _unix_to_iso_compact_tz, decrypt, encrypt

"""Utility helpers for the ai-project-practice package."""

def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b

__all__ = ["greet", "add", "multiply", "decrypt", "encrypt", "_mask_string", "_unix_to_iso_compact_tz"]
