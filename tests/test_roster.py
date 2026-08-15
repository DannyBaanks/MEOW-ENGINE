# tests/test_roster.py
from harness.roster import convoke, discover


def test_discovers_python_gladiator():
    langs = [g.language for g in discover()]
    assert "python" in langs


def test_discovery_is_deterministic():
    assert [g.language for g in discover()] == sorted(g.language for g in discover())


def test_convoke_filters_by_discipline_and_arena():
    gs = discover()
    called = convoke(gs, "construct", "ears")
    assert all("construct" in g.disciplines for g in called)
    assert all("ears" in g.arenas for g in called)


def test_convoke_excludes_unknown_arena():
    assert convoke(discover(), "construct", "no_existe_esta_arena") == []


def test_cmd_root_is_absolute():
    g = next(g for g in discover() if g.language == "python")
    assert "{root}" not in " ".join(g.cmd)