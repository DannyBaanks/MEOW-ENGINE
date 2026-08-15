# harness/tournament.py
"""El torneo. Una sola pasada produce el ranking y certifica la guardia."""
from __future__ import annotations

from harness.arena import load_policy, reach_consensus
from harness.cat import arena_names, assemble, load_spec
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
    gladiators = discover()
    prov = Provenance()
    arenas: dict[str, dict] = {}
    pieces: dict[str, str] = {}

    for name in arena_names():
        result = run_arena(name, gladiators, prov)
        arenas[name] = result
        if result["output"] is not None:
            pieces[name] = result["output"]

    cat = assemble(pieces)

    for g in convoke(gladiators, "validate", "ears"):
        r = attack_validator(g, cat, "ears")
        arenas["ears"].setdefault("guard", {})[g.language] = r

    return {"cat": cat, "digest": prov.digest(), "arenas": arenas}