"""Tests for CLI adapter evaluation."""

from planninghub.adapters.cli import run_cli


def test_run_cli_conflict(capsys) -> None:
    args = [
        "org-1",
        "res-2",
        "resrc-1",
        "2024-01-01T09:00:00",
        "2024-01-01T11:00:00",
    ]

    code = run_cli(args)

    captured = capsys.readouterr()
    assert code == 0
    assert captured.out.startswith("conflict=true")
    assert "outcome=NEEDS_MANUAL_REVIEW" in captured.out
    assert "overlaps=1" in captured.out


def test_run_cli_no_conflict(capsys) -> None:
    args = [
        "org-1",
        "res-2",
        "resrc-1",
        "2024-01-01T11:00:00",
        "2024-01-01T12:00:00",
    ]

    code = run_cli(args)

    captured = capsys.readouterr()
    assert code == 0
    assert captured.out == "conflict=false\n"


def test_run_cli_bad_args(capsys) -> None:
    code = run_cli([])

    captured = capsys.readouterr()
    assert code == 2
    assert captured.out == "error=bad_args\n"
