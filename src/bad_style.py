# NOTE: This file is intentionally written with poor style for the exam.
# Your task: refactor to be PEP 8-friendly while keeping behavior unchanged.

import math
import os
import sys


def calc(arr, mode="mean", round_to=2, allow_negative=False):
    """Compute a summary statistic for a sequence of numbers.

    Supported modes:
      - "mean": arithmetic mean
      - "median": median
      - "std": population standard deviation

    Args:
        arr: Sequence of numeric values. If None or empty, returns None.
        mode: Statistic to compute ("mean", "median", or "std").
        round_to: Number of decimal digits for rounding.
        allow_negative: If False, raises an Exception when a negative value
            is present.

    Returns:
        The computed statistic rounded to `round_to` digits, or None if
        `arr` is None or empty.
    """
    if arr is None or len(arr) == 0:
        return None
    for x in arr:
        if (not allow_negative) and x < 0:
            raise Exception("negative not allowed: " + str(x))

    if mode == "mean":
        total = 0
        for x in arr:
            total += x
        result = total / len(arr)
    elif mode == "median":
        sorted_values = sorted(arr)
        n = len(sorted_values)
        mid = n // 2
        result = (
            sorted_values[mid]
            if n % 2 == 1
            else (sorted_values[mid - 1] + sorted_values[mid]) / 2
        )
    elif mode == "std":
        m = calc(arr, "mean", round_to, allow_negative)
        total = 0
        for x in arr:
            total += (x - m) ** 2
        result = math.sqrt(total / len(arr))
    else:
        raise ValueError("Unknown mode:" + mode)

    return round(result, round_to)


def parse_numbers(text):
    """Parse a string into a list of floats.

    Accepts inputs like:
      - "1,2,3"
      - "1 2 3"
      - "1\t2\t3"

    Args:
        text: Input string. If None, returns an empty list.

    Returns:
        A list of parsed float values.
    """
    if text is None:
        return []
    t = text.replace(",", " ").replace("\t", " ")
    parts = t.split(" ")
    out = []
    for p in parts:
        if p.strip() == "":
            continue
        out.append(float(p))
    return out


def read_file(path):
    """Read and return the first line of a file."""
    with open(path) as f:
        line = f.readline()
    return line


def main(argv=None):
    """Entry point for command-line usage.

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
    is_file = False
    if len(argv) > 3 and argv[3] == "--file":
        is_file = True

    if is_file:
        if not os.path.exists(value):
            print("file not found:" + value)
            return 2
        value = read_file(value)

    nums = parse_numbers(value)
    r = calc(nums, mode=mode)
    print(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
