# tests/test_tournament.py
from harness.tournament import run_arena, run_tournament
from harness.provenance import Provenance
from harness.roster import discover

CAT = " /\\_/\\\n( o.o )\n > ^ <"


def test_arena_produces_a_winner_and_a_piece():
    r = run_arena("ears", discover(), Provenance())
    assert r["winner"] is not None
    assert r["output"] == "/\\/\\"


def test_tournament_produces_the_cat():
    assert run_tournament()["cat"] == CAT


def test_tournament_is_deterministic():
    assert run_tournament()["cat"] == run_tournament()["cat"]


def test_tournament_digest_is_reproducible():
    assert run_tournament()["digest"] == run_tournament()["digest"]


def test_every_arena_has_a_ranking():
    result = run_tournament()
    for name, data in result["arenas"].items():
        assert "ranking" in data, name