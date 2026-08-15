# tests/test_gladiator_brainfuck.py
import pytest
from harness.frontier import cross
from harness.roster import convoke, discover


def _bf():
    gs = [g for g in discover() if g.language == "brainfuck"]
    if not gs:
        pytest.skip("gladiador brainfuck no descubierto")
    return gs[0]


def test_brainfuck_builds_ears():
    c = cross(list(_bf().cmd), "brainfuck", "construct", "ears", {}, timeout_s=30)
    assert c.verdict == "OK"
    assert c.output == "/\\/\\"


def test_brainfuck_builds_padding():
    c = cross(list(_bf().cmd), "brainfuck", "construct", "padding", {}, timeout_s=30)
    assert c.output == "      "


def test_brainfuck_declares_only_what_it_can_do():
    g = _bf()
    assert "validate" not in g.disciplines
    assert convoke([g], "construct", "eyes") == []