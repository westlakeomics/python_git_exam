"""CLI tool for simple statistics (exam task).

This module is intentionally included in the exam with poor style in the
starter version. The candidate should refactor it to be PEP 8 friendly
without changing its observable behavior.
"""

from __future__ import annotations

import math
import os
import sys
from collections.abc import Iterable


def calc(
    arr: Iterable[float] | None,
    mode: str = "mean",
    round_to: int = 2,
    allow_negative: bool = False,
) -> float | None:
    """Calculate mean/median/std for a sequence.

    Args:
        arr: Input numbers. If None or empty, return None.
        mode: One of "mean", "median", "std".
        round_to: Number of decimal digits to round to.
        allow_negative: If False, raise Exception when encountering negative value.

    Returns:
        Rounded statistic value, or None if arr is None/empty.

    Raises:
        Exception: When allow_negative is False and a negative value appears.
        ValueError: When mode is unknown.
    """
    if arr is None:
        return None

    values = list(arr)
    if not values:
        return None

    if not allow_negative:
        for x in values:
            if x < 0:
                # Keep behavior compatible with the original tests.
                raise Exception(f"negative not allowed: {x}")

    if mode == "mean":
        value = sum(values) / len(values)
    elif mode == "median":
        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2
        if n % 2 == 1:
            value = sorted_values[mid]
        else:
            value = (sorted_values[mid - 1] + sorted_values[mid]) / 2
    elif mode == "std":
        mean_value = calc(values, "mean", round_to, allow_negative)
        assert mean_value is not None
        value = math.sqrt(sum((x - mean_value) ** 2 for x in values) / len(values))
    else:
        raise ValueError(f"Unknown mode:{mode}")

    return round(value, round_to)


def parse_numbers(text: str | None) -> list[float]:
    """Parse numbers from a string.

    Accept input like:
    - "1,2,3"
    - "1 2 3"
    - "1\\t2\\t3"
    """
    if text is None:
        return []

    normalized = text.replace(",", " ").replace("\t", " ")
    return [float(p) for p in normalized.split()]


def read_file(path: str) -> str:
    """Read the first line from the file."""
    with open(path, encoding="utf-8") as f:
        return f.readline()


def main(argv: list[str] | None = None) -> int:
    """Entry point for CLI.

    Usage:
        python -m src.bad_style <mode> <numbers_or_file_path> [--file]
    """
    if argv is None:
        argv = sys.argv

    if len(argv) < 3:
        print("Usage: python -m src.bad_style <mode> <numbers_or_file_path> [--file]")
        return 2

    mode = argv[1]
    value = argv[2]
    is_file = len(argv) > 3 and argv[3] == "--file"

    if is_file:
        if not os.path.exists(value):
            print(f"file not found:{value}")
            return 2
        value = read_file(value)

    nums = parse_numbers(value)
    result = calc(nums, mode=mode)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
