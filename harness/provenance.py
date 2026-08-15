# harness/provenance.py
"""Registro de todo cruce de la frontera.

Cada voto entra en el digest, sea decisivo o no: es lo que impide que un
gladiador convocado a una arena `majority` se vuelva prescindible.
"""
from __future__ import annotations

import hashlib
import json

from harness.frontier import Crossing


class Provenance:
    def __init__(self) -> None:
        self._entries: list[dict] = []

    def record(self, crossing: Crossing, decisive: bool) -> None:
        self._entries.append(
            {
                "language": crossing.language,
                "discipline": crossing.discipline,
                "arena": crossing.arena,
                "ok": crossing.ok,
                "output": crossing.output,
                "verdict": crossing.verdict,
                "decisive": decisive,
            }
        )

    def to_dict(self) -> dict:
        ordered = sorted(
            self._entries,
            key=lambda e: (e["arena"], e["discipline"], e["language"], e["output"]),
        )
        return {"entries": ordered}

    def digest(self) -> str:
        canonical = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()