# harness/tournament.py
"""El torneo. El pipeline completo corre como dataflow sobre el bus."""
from __future__ import annotations

from harness.arena import load_policy, reach_consensus
from harness.cat import arena_names, assemble, load_spec
from harness.dataflow import run_pipeline
from harness.frontier import cross
from harness.judge import attack_validator, score
from harness.provenance import Provenance
from harness.roster import convoke, discover

_TIMEOUT = 60.0


def run_arena(arena: str, gladiators, prov: Provenance) -> dict:
    policy = load_policy(arena)
    builders = convoke(gladiators, "construct", arena)
    spec = load_spec()
    expected = spec["pieces"][arena]["chars"]

    ranking = []
    for g in builders:
        c = cross(list(g.cmd), g.language, "construct", arena, {}, timeout_s=_TIMEOUT)
        prov.record(c, decisive=False)
        survived = 1 if (c.verdict == "OK" and c.output == expected) else 0
        ranking.append({"language": g.language, "score": survived, "output": c.output})

    ranking.sort(key=lambda r: (-r["score"], r["language"]))
    winner = ranking[0] if ranking and ranking[0]["score"] > 0 else None

    return {
        "winner": winner["language"] if winner else None,
        "output": winner["output"] if winner else None,
        "ranking": ranking,
        "consensus": policy.consensus,
    }


def run_tournament() -> dict:
    """El torneo completo, ejecutado como dataflow sobre el bus del coliseo."""
    return run_pipeline()