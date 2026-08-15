# harness/arena.py
"""La arena declara su politica. El arnes solo la ejecuta."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_ARENAS = Path(__file__).resolve().parent.parent / "arenas"


@dataclass(frozen=True)
class ArenaPolicy:
    name: str
    validators: int
    consensus: str
    adversarial: bool
    scoring: str


def load_policy(name: str, arenas_dir: Path | None = None) -> ArenaPolicy:
    base = Path(arenas_dir or _ARENAS)
    data = yaml.safe_load((base / "default.yaml").read_text(encoding="utf-8"))

    specific = base / ("%s.yaml" % name)
    if specific.exists():
        data.update(yaml.safe_load(specific.read_text(encoding="utf-8")) or {})

    return ArenaPolicy(
        name=name,
        validators=int(data["validators"]),
        consensus=str(data["consensus"]),
        adversarial=bool(data["adversarial"]),
        scoring=str(data["scoring"]),
    )


def reach_consensus(policy: ArenaPolicy, votes: list[bool]) -> bool:
    if not votes:
        return False
    if policy.consensus == "unanimous":
        return all(votes)
    if policy.consensus == "strict":
        return all(votes) and len(votes) == policy.validators
    if policy.consensus == "majority":
        return sum(1 for v in votes if v) * 2 > len(votes)
    raise ValueError("consenso desconocido: %s" % policy.consensus)