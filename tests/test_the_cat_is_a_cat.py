# tests/test_the_cat_is_a_cat.py
"""Los tests que el spec nombra. Sobre el gato, no sobre los modulos."""
from harness.arena import load_policy, reach_consensus
from harness.judge import attack_validator, mutations
from harness.roster import convoke, discover
from harness.tournament import run_tournament


def test_cat_has_two_ears():
    cat = run_tournament()["cat"]
    top = cat.split("\n")[0]
    assert top.count("/") == 2 and top.count("\\") == 2


def test_cat_has_two_eyes():
    cat = run_tournament()["cat"]
    assert cat.split("\n")[1].count("o") == 2


def test_cat_is_deterministic():
    assert run_tournament()["cat"] == run_tournament()["cat"]


def test_meow_is_reproducible():
    assert run_tournament()["digest"] == run_tournament()["digest"]


def test_malbolge_survived():
    """El juez atacó y el gato aguantó: ningún ataque colo un gato falso."""
    cat = run_tournament()["cat"]
    guards = convoke(discover(), "validate", "ears")
    assert guards, "no hay guardia que certificar"
    for g in guards:
        r = attack_validator(g, cat, "ears")
        assert r["false_negatives"] == 0, "%s dejo pasar un gato mutilado" % g.language


def test_n_languages_agree_that_cat_is_cat():
    cat = run_tournament()["cat"]
    policy = load_policy("ears")
    votes = []
    for g in convoke(discover(), "validate", "ears"):
        r = attack_validator(g, cat, "ears")
        votes.append(r["false_positives"] == 0)
    assert reach_consensus(policy, votes) is True


def test_ablation_breaks_the_cat():
    """Alias con el nombre del spec. Se verifica quitando de verdad."""
    from harness.ablation import run_without
    assert run_without("brainfuck")["digest"] != run_tournament()["digest"]