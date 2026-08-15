# tests/test_arena.py
import pytest
from harness.arena import ArenaPolicy, load_policy, reach_consensus


def test_ears_declares_unanimous():
    p = load_policy("ears")
    assert p.consensus == "unanimous"


def test_unknown_arena_falls_back_to_default():
    p = load_policy("mouth")
    assert p.name == "mouth"
    assert p.consensus == "majority"


def test_unanimous_needs_everyone():
    p = ArenaPolicy("x", validators=3, consensus="unanimous", adversarial=False, scoring="default")
    assert reach_consensus(p, [True, True, True]) is True
    assert reach_consensus(p, [True, True, False]) is False


def test_majority_tolerates_one_dissenter():
    p = ArenaPolicy("x", validators=3, consensus="majority", adversarial=False, scoring="default")
    assert reach_consensus(p, [True, True, False]) is True
    assert reach_consensus(p, [True, False, False]) is False


def test_strict_rejects_abstentions():
    p = ArenaPolicy("x", validators=3, consensus="strict", adversarial=True, scoring="default")
    assert reach_consensus(p, [True, True, True]) is True
    assert reach_consensus(p, [True, True]) is False


def test_empty_votes_never_pass():
    for mode in ("unanimous", "majority", "strict"):
        p = ArenaPolicy("x", validators=3, consensus=mode, adversarial=False, scoring="default")
        assert reach_consensus(p, []) is False