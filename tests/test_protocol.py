# tests/test_protocol.py
import json
import pytest
from harness.protocol import encode_request, decode_response, ProtocolError


def test_encode_request_is_single_line_json():
    raw = encode_request("construct", "ears", {"seed": 1})
    assert "\n" not in raw
    assert json.loads(raw) == {
        "discipline": "construct",
        "arena": "ears",
        "payload": {"seed": 1},
    }


def test_decode_response_parses_ok():
    assert decode_response('{"ok": true, "output": "/\\\\"}') == {
        "ok": True,
        "output": "/\\",
    }


def test_decode_response_rejects_garbage():
    with pytest.raises(ProtocolError):
        decode_response("no soy json")


def test_decode_response_rejects_missing_ok():
    with pytest.raises(ProtocolError):
        decode_response('{"output": "x"}')