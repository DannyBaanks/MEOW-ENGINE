# harness/roster.py
"""Descubrimiento de gladiadores. Un contrato, cero suposiciones."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_LANGS = Path(__file__).resolve().parent.parent / "languages"


@dataclass(frozen=True)
class Gladiator:
    language: str
    cmd: tuple[str, ...]
    disciplines: tuple[str, ...]
    arenas: tuple[str, ...]
    root: Path


def discover(languages_dir: Path | None = None) -> list[Gladiator]:
    base = Path(languages_dir or _LANGS)
    found: list[Gladiator] = []

    for contract_path in sorted(base.glob("*/contract.json")):
        data = json.loads(contract_path.read_text(encoding="utf-8"))
        root = contract_path.parent.resolve()
        cmd = tuple(part.replace("{root}", str(root)) for part in data["runtime"]["cmd"])
        found.append(
            Gladiator(
                language=data["language"],
                cmd=cmd,
                disciplines=tuple(sorted(data["disciplines"])),
                arenas=tuple(sorted(data["arenas"])),
                root=root,
            )
        )

    return sorted(found, key=lambda g: g.language)


def convoke(gladiators: list[Gladiator], discipline: str, arena: str) -> list[Gladiator]:
    return [g for g in gladiators if discipline in g.disciplines and arena in g.arenas]