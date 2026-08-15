# tests/test_dataflow.py
"""El bus y el motor dataflow: el torneo ya no llama, publica."""
import os
import tempfile

import pytest

from harness import bus
from harness.dataflow import run_pipeline, wait_for
from harness.caesar import run_caesar

CAT = " /\\_/\\\n( o.o )\n > ^ <"


def test_bus_publish_and_read_roundtrip():
    path = os.path.join(tempfile.mkdtemp(), "bus.jsonl")
    bus.publish(path, "done:test", {"x": 1})
    entries = bus.read_all(path)
    assert entries[0]["node"] == "done:test"
    assert entries[0]["value"] == {"x": 1}


def test_wait_for_collects_done_tokens():
    path = os.path.join(tempfile.mkdtemp(), "bus.jsonl")
    bus.publish(path, "done:cat", {"cat": "x"})
    collected = wait_for(path, ["cat"], timeout_s=5.0)
    assert collected == {"cat": {"cat": "x"}}


def test_wait_for_raises_on_error_token():
    path = os.path.join(tempfile.mkdtemp(), "bus.jsonl")
    bus.publish(path, "error:ears", {"error": "se rompio"})
    with pytest.raises(RuntimeError):
        wait_for(path, ["cat"], timeout_s=5.0)


def test_pipeline_produces_the_cat_through_the_bus():
    assert run_pipeline()["cat"] == CAT


def test_pipeline_digest_is_reproducible():
    assert run_pipeline()["digest"] == run_pipeline()["digest"]


def test_pipeline_agrees_with_the_caesar():
    assert run_pipeline()["cat"] == run_caesar()["cat"]