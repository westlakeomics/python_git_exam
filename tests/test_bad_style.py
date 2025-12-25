import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def run_cmd(args, cwd=PROJECT_ROOT):
    return subprocess.run(
        args,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize(
    ("mode", "numbers", "expected"),
    [
        ("mean", "1,2,3", "2.0\n"),
        ("median", "1 2 3 4", "2.5\n"),
        ("std", "2 2 2 2", "0.0\n"),
    ],
)
def test_cli_outputs_expected(mode, numbers, expected):
    cmd = [sys.executable, "-m", "src.bad_style", mode, numbers]
    r = run_cmd(cmd)
    assert r.returncode == 0
    assert r.stdout == expected


def test_cli_file_flag(tmp_path: Path):
    p = tmp_path / "nums.txt"
    p.write_text("1,2,3\n", encoding="utf-8")
    cmd = [sys.executable, "-m", "src.bad_style", "mean", str(p), "--file"]
    r = run_cmd(cmd)
    assert r.returncode == 0
    assert r.stdout == "2.0\n"


def test_negative_not_allowed():
    from src.bad_style import calc

    with pytest.raises(Exception):  # noqa: B017 - required by exam starter behavior
        calc([1, -1, 2], mode="mean", allow_negative=False)


def test_negative_allowed():
    from src.bad_style import calc

    assert calc([1, -1, 2], mode="mean", allow_negative=True) == 0.67
