# harness/dataflow.py
"""El torneo como dataflow, no como llamadas en serie.

El arnes no llama a los gladiadores uno tras otro: los siembra como nodos.
Cada nodo es un proceso de SO con PID propio que espera en el bus a que sus
dependencias hayan publicado su token `done`, corre su trabajo real y
publica el suyo. El driver no orquesta el orden: siembra todo de golpe
(10 construct + 1 assemble + 2 guard + 1 caesar, barajados por run_id) y
lee del bus que de verdad paso.

Grafo (nadie llama a nadie, cada uno observa el bus en pasivo):
  construct:<arena>  x10  ->  sin dependencias; publica  done:arena:<arena>
  caesar                    ->  sin dependencias; publica  done:caesar
  assemble                  ->  espera los 10 done:arena; publica done:cat
  guard:<lang>        x2   ->  espera done:cat; publica   done:guard:<lang>

El bus es un log append-only (harness/bus.py): productor y consumidor estan
desacoplados en el tiempo.
"""
from __future__ import annotations

import os
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from harness import bus
from harness.arena import load_policy
from harness.cat import arena_names, assemble, load_spec
from harness.frontier import Crossing, cross
from harness.judge import attack_validator
from harness.provenance import Provenance
from harness.roster import convoke, discover

_TIMEOUT = 60.0
_NODE_WAIT_S = 600.0
_DRIVER_WAIT_S = 900.0

_REPO_ROOT = Path(__file__).resolve().parent.parent


def wait_for(bus_path: str, deps: list[str], timeout_s: float = _NODE_WAIT_S) -> dict:
    """Espera pasiva (polling, sin que nadie lo llame) a que TODAS las deps
    hayan publicado su token `done` en el bus."""
    start = time.monotonic()
    wanted = set(deps)
    collected: dict[str, dict] = {}
    while not wanted.issubset(collected):
        for entry in bus.read_all(bus_path):
            node = entry.get("node", "")
            if node.startswith("error:"):
                raise RuntimeError("nodo fallo: %s" % (entry.get("value"),))
            if node.startswith("done:"):
                name = node[len("done:"):]
                if name in wanted and name not in collected:
                    collected[name] = entry["value"]
        if time.monotonic() - start > timeout_s:
            raise TimeoutError("espera dataflow agotada: %s"
                               % sorted(wanted - set(collected)))
        time.sleep(0.02)
    return collected


# ---------------------------------------------------------------------------
# Nodos. Cada uno es un proceso de SO separado (PID propio).
# ---------------------------------------------------------------------------

def _work_construct(arena: str, bus_path: str) -> None:
    policy = load_policy(arena)
    builders = convoke(discover(), "construct", arena)
    expected = load_spec()["pieces"][arena]["chars"]

    ranking = []
    crossings = []
    for g in builders:
        c = cross(list(g.cmd), g.language, "construct", arena, {}, timeout_s=_TIMEOUT)
        crossings.append({
            "language": g.language, "discipline": "construct", "arena": arena,
            "ok": c.ok, "output": c.output, "verdict": c.verdict, "decisive": False,
        })
        survived = 1 if (c.verdict == "OK" and c.output == expected) else 0
        ranking.append({"language": g.language, "score": survived, "output": c.output})

    ranking.sort(key=lambda r: (-r["score"], r["language"]))
    winner = ranking[0] if ranking and ranking[0]["score"] > 0 else None

    bus.publish(bus_path, "done:arena:%s" % arena, {
        "winner": winner["language"] if winner else None,
        "output": winner["output"] if winner else None,
        "ranking": ranking,
        "consensus": policy.consensus,
        "crossings": crossings,
    })


def _work_assemble(bus_path: str) -> None:
    deps = ["arena:%s" % a for a in arena_names()]
    results = wait_for(bus_path, deps)

    pieces = {}
    crossings = []
    arenas = {}
    for a in arena_names():
        payload = results["arena:%s" % a]
        arenas[a] = payload
        if payload["output"] is not None:
            pieces[a] = payload["output"]
        crossings.extend(payload["crossings"])

    cat = assemble(pieces)

    prov = Provenance()
    for c in crossings:
        prov.record(
            Crossing(c["language"], c["discipline"], c["arena"], c["ok"],
                     c["output"], c["verdict"], 0),
            c["decisive"],
        )

    bus.publish(bus_path, "done:cat", {
        "cat": cat, "digest": prov.digest(), "pieces": pieces, "arenas": arenas,
    })


def _work_guard(language: str, bus_path: str) -> None:
    g = next(x for x in discover() if x.language == language)
    cat = wait_for(bus_path, ["cat"])["cat"]["cat"]
    result = attack_validator(g, cat, "ears")
    bus.publish(bus_path, "done:guard:%s" % language, result)


def _work_caesar(bus_path: str) -> None:
    from harness.caesar import laugh, run_caesar
    c = run_caesar()
    bus.publish(bus_path, "done:caesar", {"cat": c["cat"], "laugh": laugh().strip()})


# ---------------------------------------------------------------------------
# Entrypoint del nodo: python -m harness.dataflow <tipo> <args...>
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    if not argv:
        return 1
    kind = argv[0]
    try:
        if kind == "construct":
            _work_construct(argv[1], argv[2])
        elif kind == "assemble":
            _work_assemble(argv[1])
        elif kind == "guard":
            _work_guard(argv[1], argv[2])
        elif kind == "caesar":
            _work_caesar(argv[1])
        else:
            return 1
        return 0
    except Exception as e:  # noqa: BLE001 -- el fallo del nodo va al bus
        name = kind + (":%s" % argv[1] if kind in ("construct", "guard") else "")
        try:
            import traceback
            bus.publish(argv[-1], "error:%s" % name,
                        {"error": repr(e), "tb": traceback.format_exc()})
        except Exception:  # noqa: BLE001
            pass
        return 1


# ---------------------------------------------------------------------------
# Driver. Siembra todo de golpe y lee del bus que de verdad paso.
# ---------------------------------------------------------------------------

def run_pipeline() -> dict:
    run_id = os.urandom(4).hex()
    bus_path = os.path.join(tempfile.gettempdir(), "meow_bus_%s.jsonl" % run_id)
    for suffix in ("", ".lock"):
        try:
            os.remove(bus_path + suffix)
        except (FileNotFoundError, PermissionError):
            pass

    cmd = [sys.executable, "-m", "harness.dataflow"]
    jobs = []
    for a in arena_names():
        jobs.append(("construct:%s" % a, ["construct", a, bus_path]))
    jobs.append(("assemble", ["assemble", bus_path]))
    for g in convoke(discover(), "validate", "ears"):
        jobs.append(("guard:%s" % g.language, ["guard", g.language, bus_path]))
    jobs.append(("caesar", ["caesar", bus_path]))

    rng = random.Random(run_id)
    rng.shuffle(jobs)

    procs = []
    try:
        for name, argv in jobs:
            procs.append((name, subprocess.Popen(cmd + argv, cwd=str(_REPO_ROOT))))

        deadline = time.monotonic() + _DRIVER_WAIT_S
        for name, p in procs:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("el torneo dataflow agoto su tiempo esperando a %s" % name)
            p.wait(timeout=remaining)

        entries = bus.read_all(bus_path)
        errors = [e for e in entries if e.get("node", "").startswith("error:")]
        if errors:
            raise RuntimeError("tokens de error en el bus: %s" % [e.get("value") for e in errors])

        failed = [(n, p.returncode) for n, p in procs if p.returncode != 0]
        if failed:
            raise RuntimeError("nodos fallaron: %s" % failed)

        cat_payload = wait_for(bus_path, ["cat"])["cat"]
        cat = cat_payload["cat"]
        arenas = cat_payload["arenas"]

        guard = {}
        for g in convoke(discover(), "validate", "ears"):
            guard[g.language] = wait_for(bus_path, ["guard:%s" % g.language])["guard:%s" % g.language]
        if guard:
            arenas["ears"]["guard"] = guard

        return {"cat": cat, "digest": cat_payload["digest"], "arenas": arenas}
    finally:
        for _name, p in procs:
            if p.poll() is None:
                p.kill()
        for suffix in ("", ".lock"):
            try:
                os.remove(bus_path + suffix)
            except (FileNotFoundError, PermissionError):
                pass


if __name__ == "__main__":
    sys.exit(main())