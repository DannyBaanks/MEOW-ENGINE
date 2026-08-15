# harness/cat.py
"""El gato como datos, nunca como literal."""
from __future__ import annotations

import json
from pathlib import Path

_SPEC_PATH = Path(__file__).resolve().parent.parent / "cat" / "spec.json"
_HOLE = "\x00"


def load_spec(path: str | None = None) -> dict:
    return json.loads(Path(path or _SPEC_PATH).read_text(encoding="utf-8"))


def arena_names() -> list[str]:
    return sorted(load_spec()["pieces"].keys())


PIECE_ORDER = arena_names()


def assemble(pieces: dict[str, str]) -> str:
    spec = load_spec()
    grid = [[_HOLE] * w for w in spec["widths"]]

    for name in PIECE_ORDER:
        cells = spec["pieces"][name]["cells"]
        if not cells:
            continue
        chars = pieces.get(name)
        if chars is None:
            continue
        for (row, col), ch in zip(cells, chars):
            grid[row][col] = ch

    return "\n".join("".join(row) for row in grid)