# harness/protocol.py
"""Protocolo JSON stdin/stdout. El unico dialecto que hablan los 40 gladiadores."""
from __future__ import annotations

import json


class ProtocolError(Exception):
    """La respuesta del gladiador no cumple el contrato."""


def encode_request(discipline: str, arena: str, payload: dict) -> str:
    return json.dumps(
        {"discipline": discipline, "arena": arena, "payload": payload},
        sort_keys=True,
        separators=(",", ":"),
    )


def decode_response(raw: str) -> dict:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ProtocolError("respuesta no es JSON: %s" % e) from e
    if not isinstance(data, dict):
        raise ProtocolError("respuesta no es un objeto JSON")
    if "ok" not in data:
        raise ProtocolError("respuesta sin campo 'ok'")
    return data