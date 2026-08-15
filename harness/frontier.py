# harness/frontier.py
"""La frontera. El gladiador no sabe quien lo ejecuta; solo recibe su contrato.

Windows no tiene resource.setrlimit, asi que el cap de recursos es
timeout + limite de bytes de salida.
"""
from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass

from harness.protocol import ProtocolError, decode_response, encode_request


@dataclass(frozen=True)
class Crossing:
    language: str
    discipline: str
    arena: str
    ok: bool
    output: str
    verdict: str
    elapsed_ms: int


def _fail(language, discipline, arena, verdict, elapsed_ms) -> Crossing:
    return Crossing(language, discipline, arena, False, "", verdict, elapsed_ms)


def cross(
    cmd: list[str],
    language: str,
    discipline: str,
    arena: str,
    payload: dict,
    timeout_s: float = 5.0,
    max_output_bytes: int = 65536,
) -> Crossing:
    request = encode_request(discipline, arena, payload)
    started = time.monotonic()

    try:
        proc = subprocess.run(
            cmd,
            input=request,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        return _fail(language, discipline, arena, "TIMEOUT",
                     int((time.monotonic() - started) * 1000))
    except (OSError, ValueError):
        return _fail(language, discipline, arena, "CRASH",
                     int((time.monotonic() - started) * 1000))

    elapsed_ms = int((time.monotonic() - started) * 1000)
    raw = proc.stdout or ""

    if len(raw.encode("utf-8", "replace")) > max_output_bytes:
        return _fail(language, discipline, arena, "OVERFLOW", elapsed_ms)

    try:
        data = decode_response(raw.strip())
    except ProtocolError:
        verdict = "CRASH" if proc.returncode != 0 else "BAD_SCHEMA"
        return _fail(language, discipline, arena, verdict, elapsed_ms)

    return Crossing(
        language=language,
        discipline=discipline,
        arena=arena,
        ok=bool(data.get("ok")),
        output=str(data.get("output", "")),
        verdict="OK",
        elapsed_ms=elapsed_ms,
    )