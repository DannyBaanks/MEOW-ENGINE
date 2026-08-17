# harness/cat.py
"""El gato como datos, nunca como literal."""
from __future__ import annotations

import json
from pathlib import Path

_SPEC_PATH = Path(__file__).resolve().parent.parent / "cat" / "spec.json"
_HOLE = "\x00"


def load_spec(path: str | None = None) -> dict:
    source = Path(path or _SPEC_PATH)
    data = json.loads(source.read_text(encoding="utf-8"))
    _validate_spec(data, source)
    return data


def _validate_spec(spec: dict, source: Path) -> None:
    if not isinstance(spec, dict):
        raise ValueError("spec %s debe ser un objeto JSON" % source)
    rows = spec.get("rows")
    widths = spec.get("widths")
    pieces = spec.get("pieces")
    if type(rows) is not int or rows <= 0:
        raise ValueError("spec %s tiene rows invalido" % source)
    if not isinstance(widths, list) or len(widths) != rows:
        raise ValueError("spec %s tiene widths inconsistente" % source)
    if any(type(width) is not int or width <= 0 for width in widths):
        raise ValueError("spec %s tiene anchos invalidos" % source)
    if not isinstance(pieces, dict):
        raise ValueError("spec %s debe declarar pieces" % source)

    occupied: set[tuple[int, int]] = set()
    for name, piece in pieces.items():
        if not isinstance(piece, dict):
            raise ValueError("pieza %s invalida en %s" % (name, source))
        cells = piece.get("cells")
        chars = piece.get("chars")
        if not isinstance(cells, list) or not isinstance(chars, str):
            raise ValueError("pieza %s invalida en %s" % (name, source))
        if len(cells) != len(chars):
            raise ValueError("pieza %s no coincide en cells/chars" % name)
        for cell in cells:
            if (not isinstance(cell, list) or len(cell) != 2 or
                    any(type(coord) is not int for coord in cell)):
                raise ValueError("celda invalida en pieza %s" % name)
            row, col = cell
            if row < 0 or row >= rows or col < 0 or col >= widths[row]:
                raise ValueError("celda fuera de rango en pieza %s" % name)
            coordinate = (row, col)
            if coordinate in occupied:
                raise ValueError("celda duplicada en pieza %s" % name)
            occupied.add(coordinate)


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
