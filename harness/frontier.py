# harness/frontier.py
"""La frontera. El gladiador no sabe quien lo ejecuta; solo recibe su contrato.

Windows no tiene resource.setrlimit, asi que el cap de recursos es
timeout + limite de bytes de salida.
"""
from __future__ import annotations

import subprocess
import os
import signal
import threading
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


def _popen_kwargs() -> dict:
    if os.name == "nt":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def _terminate_tree(proc: subprocess.Popen) -> None:
    """Termina el proceso y sus descendientes en Windows y POSIX."""
    if proc.poll() is not None:
        return
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        else:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (OSError, subprocess.SubprocessError):
        try:
            proc.kill()
        except OSError:
            pass


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
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            **_popen_kwargs(),
        )
    except (OSError, ValueError):
        return _fail(language, discipline, arena, "CRASH",
                     int((time.monotonic() - started) * 1000))

    output = bytearray()
    overflow = threading.Event()

    def read_stdout() -> None:
        assert proc.stdout is not None
        while True:
            chunk = proc.stdout.read(8192)
            if not chunk:
                return
            output.extend(chunk)
            if len(output) > max_output_bytes:
                overflow.set()
                return

    reader = threading.Thread(target=read_stdout, daemon=True)
    reader.start()
    try:
        assert proc.stdin is not None
        proc.stdin.write(request.encode("utf-8"))
        proc.stdin.close()
    except (BrokenPipeError, OSError):
        pass

    timed_out = False
    while proc.poll() is None:
        if overflow.is_set():
            _terminate_tree(proc)
            break
        if time.monotonic() - started > timeout_s:
            timed_out = True
            _terminate_tree(proc)
            break
        time.sleep(0.005)

    try:
        proc.wait(timeout=2.0)
    except subprocess.TimeoutExpired:
        _terminate_tree(proc)
        proc.wait(timeout=2.0)
    reader.join(timeout=2.0)
    elapsed_ms = int((time.monotonic() - started) * 1000)

    if timed_out:
        return _fail(language, discipline, arena, "TIMEOUT", elapsed_ms)
    if overflow.is_set():
        return _fail(language, discipline, arena, "OVERFLOW", elapsed_ms)

    raw = bytes(output).decode("utf-8", "replace")
    if len(output) > max_output_bytes:
        return _fail(language, discipline, arena, "OVERFLOW", elapsed_ms)
    if proc.returncode != 0:
        return _fail(language, discipline, arena, "CRASH", elapsed_ms)

    try:
        data = decode_response(raw.strip())
    except ProtocolError:
        return _fail(language, discipline, arena, "BAD_SCHEMA", elapsed_ms)

    return Crossing(
        language=language,
        discipline=discipline,
        arena=arena,
        ok=data["ok"],
        output=data.get("output", ""),
        verdict="OK",
        elapsed_ms=elapsed_ms,
    )
