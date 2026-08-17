# languages/python/gladiator.py
"""Gladiador Python. Construye cualquier pieza y valida invariantes del gato."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve()
SPEC = json.loads(
    (ROOT.parents[2] / "cat" / "spec.json").read_text(encoding="utf-8")
)


def construct(arena):
    return SPEC["pieces"][arena]["chars"]


def validate(candidate):
    rows = candidate.split("\n")
    if len(rows) != SPEC["rows"]:
        return False, "filas != %d" % SPEC["rows"]
    if [len(r) for r in rows] != SPEC["widths"]:
        return False, "anchos != %s" % SPEC["widths"]
    if "\x00" in candidate:
        return False, "hay un agujero en el gato"
    if rows[1].count("o") != 2:
        return False, "el gato no tiene dos ojos"
    if rows[0].count("/") != 2 or rows[0].count("\\") != 2:
        return False, "el gato no tiene dos orejas"
    if rows[2].count(">") != 1 or rows[2].count("<") != 1:
        return False, "el gato no tiene bigotes"
    return True, "es un gato"


def main():
    req = json.loads(sys.stdin.read())

    cap, arena = req["discipline"], req["arena"]

    if cap == "construct":
        print(json.dumps({"ok": True, "output": construct(arena)}))
    elif cap == "validate":
        ok, reason = validate(req["payload"].get("candidate", ""))
        print(json.dumps({"ok": ok, "output": reason}))
    else:
        print(json.dumps({"ok": False, "output": "disciplina desconocida"}))


if __name__ == "__main__":
    main()
