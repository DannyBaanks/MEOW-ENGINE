# tests/test_the_joke.py
from harness.ablation import run_without
from harness.caesar import run_caesar
from harness.tournament import run_tournament


def test_the_whole_thing_was_unnecessary():
    """EL REMATE. 3 gladiadores, un juez y una arena entera producen
    exactamente lo mismo que el Cesar solo."""
    assert run_tournament()["cat"] == run_caesar()["cat"]


def test_ablation_changes_the_artifact():
    full = run_tournament()
    without = run_without("brainfuck")
    assert without["digest"] != full["digest"]


def test_ablation_of_the_only_builder_breaks_the_cat():
    """Regla 1: sin constructores, no hay gato. La ablacion quita a TODOS los
    gladiadores que declaran "construct" (sean 3 o 40) y exige el agujero."""
    from pathlib import Path
    from harness.roster import discover
    from harness.tournament import run_tournament
    gladiators = discover()
    builders = [g for g in gladiators if "construct" in g.disciplines]
    hidden = {}
    try:
        for g in builders:
            c = (g.root / "contract.json")
            h = c.with_suffix(".json.ablated")
            c.rename(h)
            hidden[c] = h
        cat = run_tournament()["cat"]
    finally:
        for c, h in hidden.items():
            if h.exists():
                h.rename(c)
    assert "\x00" in cat


def test_ablation_restores_the_roster():
    from harness.roster import discover
    before = [g.language for g in discover()]
    run_without("brainfuck")
    assert [g.language for g in discover()] == before