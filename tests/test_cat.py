# tests/test_cat.py
import pytest
from harness.cat import arena_names, assemble, load_spec

CAT = " /\\_/\\\n( o.o )\n > ^ <"


def test_spec_has_ten_arenas():
    assert len(arena_names()) == 10
    assert arena_names() == sorted(arena_names())


def test_assemble_full_cat():
    spec = load_spec()
    pieces = {name: spec["pieces"][name]["chars"] for name in arena_names()}
    assert assemble(pieces) == CAT


def test_missing_arena_leaves_a_hole():
    spec = load_spec()
    pieces = {name: spec["pieces"][name]["chars"] for name in arena_names()}
    del pieces["eyes"]
    result = assemble(pieces)
    assert result != CAT
    assert "\x00" in result


def test_row_widths():
    assert [len(r) for r in CAT.split("\n")] == [6, 7, 6]


def test_invalid_spec_is_rejected(tmp_path):
    path = tmp_path / "spec.json"
    path.write_text(
        '{"rows": 1, "widths": [1], "pieces": '
        '{"bad": {"cells": [[0, 0]], "chars": "XX"}}}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="cells/chars"):
        load_spec(str(path))
