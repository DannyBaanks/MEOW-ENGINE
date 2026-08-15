# tests/test_frontier.py
import sys
from harness.frontier import cross

PY = sys.executable


def _inline(code: str) -> list[str]:
    return [PY, "-c", code]


def test_good_gladiator_crosses():
    c = cross(
        _inline('import sys,json; sys.stdin.read(); print(json.dumps({"ok":True,"output":"/"}))'),
        language="fake", discipline="construct", arena="ears", payload={},
    )
    assert c.verdict == "OK"
    assert c.ok is True
    assert c.output == "/"


def test_infinite_loop_is_a_timeout_not_a_hang():
    c = cross(
        _inline("while True: pass"),
        language="fake", discipline="construct", arena="ears", payload={},
        timeout_s=0.5,
    )
    assert c.verdict == "TIMEOUT"
    assert c.ok is False


def test_garbage_output_is_bad_schema():
    c = cross(
        _inline('print("JAJAJA no soy json")'),
        language="fake", discipline="construct", arena="ears", payload={},
    )
    assert c.verdict == "BAD_SCHEMA"
    assert c.ok is False


def test_flood_is_overflow():
    c = cross(
        _inline('print("x" * 200000)'),
        language="fake", discipline="construct", arena="ears", payload={},
        max_output_bytes=1024,
    )
    assert c.verdict == "OVERFLOW"
    assert c.ok is False


def test_crash_is_survived():
    c = cross(
        _inline("raise SystemExit(3)"),
        language="fake", discipline="construct", arena="ears", payload={},
    )
    assert c.verdict in ("CRASH", "BAD_SCHEMA")
    assert c.ok is False