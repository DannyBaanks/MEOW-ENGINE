# tests/test_gladiator_rust.py
import pytest
from harness.frontier import cross
from harness.roster import discover

CAT = " /\\_/\\\n( o.o )\n > ^ <"


def _rust():
    gs = [g for g in discover() if g.language == "rust"]
    if not gs:
        pytest.skip("gladiador rust no descubierto")
    return gs[0]


def test_rust_builds_ears():
    c = cross(list(_rust().cmd), "rust", "construct", "ears", {}, timeout_s=60)
    assert c.verdict == "OK"
    assert c.output == "/\\/\\"


def test_rust_accepts_a_real_cat():
    c = cross(list(_rust().cmd), "rust", "validate", "ears",
              {"candidate": CAT}, timeout_s=60)
    assert c.verdict == "OK"
    assert c.ok is True


def test_rust_rejects_a_one_eyed_cat():
    maimed = CAT.replace("( o.o )", "( o.  )")
    c = cross(list(_rust().cmd), "rust", "validate", "ears",
              {"candidate": maimed}, timeout_s=60)
    assert c.ok is False