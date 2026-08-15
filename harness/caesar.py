# harness/caesar.py
"""El Cesar. Preside el torneo y podia haberlo hecho todo solo."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from interpreters.jajaja import run  # noqa: E402

_LANGS = Path(__file__).resolve().parent.parent / "languages" / "jajaja"
_CAT_JAJA = _LANGS / "cat.jaja"
_LAUGH_JAJA = _LANGS / "laugh.jaja"


def run_caesar() -> dict:
    source = _CAT_JAJA.read_text(encoding="utf-8")
    output, steps, status = run(source, max_steps=200000)
    return {"cat": output.rstrip("\n"), "steps": steps, "status": status}


def laugh() -> str:
    """La risa NO es un literal: sale de tres reescrituras del Cesar."""
    output, _steps, _status = run(_LAUGH_JAJA.read_text(encoding="utf-8"), max_steps=1000)
    return output