# tests/test_provenance.py
from harness.frontier import Crossing
from harness.provenance import Provenance


def _c(lang, ok=True):
    return Crossing(lang, "validate", "ears", ok, "es un gato", "OK", 5)


def test_digest_is_stable_across_instances():
    a, b = Provenance(), Provenance()
    for p in (a, b):
        p.record(_c("python"), decisive=True)
        p.record(_c("rust"), decisive=False)
    assert a.digest() == b.digest()


def test_non_decisive_vote_still_changes_the_digest():
    """El corazon de la mitigacion de `majority`."""
    a, b = Provenance(), Provenance()
    a.record(_c("python"), decisive=True)
    b.record(_c("python"), decisive=True)
    b.record(_c("brainfuck"), decisive=False)
    assert a.digest() != b.digest()


def test_record_order_does_not_matter():
    a, b = Provenance(), Provenance()
    a.record(_c("python"), True); a.record(_c("rust"), False)
    b.record(_c("rust"), False); b.record(_c("python"), True)
    assert a.digest() == b.digest()


def test_elapsed_time_does_not_leak_into_digest():
    a, b = Provenance(), Provenance()
    a.record(Crossing("python", "validate", "ears", True, "x", "OK", 5), True)
    b.record(Crossing("python", "validate", "ears", True, "x", "OK", 999), True)
    assert a.digest() == b.digest()