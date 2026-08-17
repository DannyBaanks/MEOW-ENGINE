# tests/test_cli.py
import json
from meow import main

CAT = " /\\_/\\\n( o.o )\n > ^ <"


def test_tournament_prints_cat_and_laugh(capsys):
    assert main(["--tournament"]) == 0
    out = capsys.readouterr().out
    assert CAT in out
    assert "JAJAJA" in out


def test_caesar_prints_cat(capsys):
    assert main(["--caesar"]) == 0
    assert CAT in capsys.readouterr().out


def test_list_gladiators_lists_gladiators(capsys):
    assert main(["--list-gladiators"]) == 0
    out = capsys.readouterr().out
    assert "python" in out and "brainfuck" in out


def test_single_arena_runs_alone(capsys):
    assert main(["--arena", "ears"]) == 0
    out = capsys.readouterr().out
    assert json.dumps("/\\/\\") in out


def test_unknown_flag_is_an_error():
    assert main(["--gato"]) != 0


def test_help_is_success(capsys):
    assert main(["--help"]) == 0
    assert "usage:" in capsys.readouterr().out
