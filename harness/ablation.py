# harness/ablation.py
"""Ablacion real. Lo que no se verifica rompiendo, no esta verificado."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from harness.tournament import run_tournament

_LANGS = Path(__file__).resolve().parent.parent / "languages"


def run_without(language: str) -> dict:
    contract = _LANGS / language / "contract.json"
    if not contract.exists():
        raise ValueError("no existe el gladiador %s" % language)

    fd, temporary_name = tempfile.mkstemp(
        prefix=".%s." % contract.stem,
        suffix=".ablation",
        dir=str(contract.parent),
    )
    os.close(fd)
    hidden = Path(temporary_name)
    hidden.unlink()
    contract.rename(hidden)
    try:
        result = run_tournament()
        return {"cat": result["cat"], "digest": result["digest"]}
    finally:
        hidden.rename(contract)
