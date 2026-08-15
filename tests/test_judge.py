# tests/test_judge.py
from harness.judge import attack_validator, mutations, score
from harness.roster import discover

CAT = " /\\_/\\\n( o.o )\n > ^ <"


def test_mutations_are_deterministic():
    assert mutations(CAT) == mutations(CAT)


def test_every_mutation_actually_mutilates():
    for name, m in mutations(CAT):
        assert m != CAT, "el ataque %s no cambio nada" % name


def test_there_are_several_attacks():
    assert len(mutations(CAT)) >= 4


def test_python_gladiator_detects_the_attacks():
    g = next(g for g in discover() if g.language == "python")
    r = attack_validator(g, CAT, "ears")
    assert r["false_positives"] == 0
    assert r["detected"] >= 1


def test_score_punishes_lying_about_the_cat():
    honest = score(None, crossings_ok=5, false_positives=0, false_negatives=0)
    liar = score(None, crossings_ok=5, false_positives=0, false_negatives=3)
    assert honest > liar