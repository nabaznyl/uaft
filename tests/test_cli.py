import sys
import pytest
from unittest.mock import patch, MagicMock
from uaft.cli import main


def test_help(capsys):
    with patch.object(sys, "argv", ["uaft", "--help"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert "Usage: uaft <command>" in captured.out


def test_version(capsys):
    with patch.object(sys, "argv", ["uaft", "version"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert "UAFT v" in captured.out


def test_hooks_help(capsys):
    with patch.object(sys, "argv", ["uaft", "hooks", "--help"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert "Usage: uaft hooks" in captured.out


def test_fix_help(capsys):
    with patch.object(sys, "argv", ["uaft", "fix", "--help"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert "Usage: uaft fix" in captured.out


def test_track_test_help(capsys):
    with patch.object(sys, "argv", ["uaft", "track-test", "--help"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert "Usage: uaft track-test" in captured.out
