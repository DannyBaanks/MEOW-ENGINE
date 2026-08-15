# harness/judge.py
"""Malbolge, el Judge. No mata al gato por maldad: lo mata para certificar
que aguanta. Quien dice "sigue siendo un gato" sobre un gato mutilado,
no quiere al gato.
"""
from __future__ import annotations

from harness.frontier import cross
from harness.roster import Gladiator


def mutations(cat: str) -> list[tuple[str, str]]:
    rows = cat.split("\n")
    out: list[tuple[str, str]] = []

    out.append(("gouge_eye", cat.replace("o.o", "o. ", 1)))
    out.append(("clip_ear", cat.replace("/\\_/\\", " \\_/\\", 1)))
    out.append(("shave_whiskers", cat.replace(">", " ", 1)))
    out.append(("punch_hole", cat.replace(".", "\x00", 1)))
    out.append(("squash_row", "\n".join(rows[:2])))
    out.append(("widen_row", rows[0] + " \n" + rows[1] + "\n" + rows[2]))

    return sorted(out, key=lambda p: p[0])


def score(gladiator, crossings_ok: int, false_positives: int, false_negatives: int) -> int:
    return crossings_ok - false_positives - false_negatives


def attack_validator(gladiator: Gladiator, cat: str, arena: str) -> dict:
    false_positives = 0
    false_negatives = 0
    detected = 0

    intact = cross(list(gladiator.cmd), gladiator.language, "validate", arena,
                   {"candidate": cat}, timeout_s=60)
    if intact.verdict == "OK" and not intact.ok:
        false_positives += 1

    for _name, maimed in mutations(cat):
        r = cross(list(gladiator.cmd), gladiator.language, "validate", arena,
                  {"candidate": maimed}, timeout_s=60)
        if r.verdict != "OK":
            continue
        if r.ok:
            false_negatives += 1
        else:
            detected += 1

    return {
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "detected": detected,
    }