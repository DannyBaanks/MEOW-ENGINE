# languages/brainfuck/adapter.py
"""Brainfuck adapter: translates the harness protocol to the interpreter."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve()
sys.path.insert(0, str(ROOT.parents[2]))

from interpreters.brainfuck import run  # noqa: E402

PROGRAMS = {"ears": "construct_ears.bf", "padding": "construct_padding.bf"}


def main():
    req = json.loads(sys.stdin.read())

    if req["discipline"] != "construct" or req["arena"] not in PROGRAMS:
        print(json.dumps({"ok": False, "output": "no compito en eso"}))
        return

    source = (ROOT.parent / PROGRAMS[req["arena"]]).read_text(encoding="utf-8")
    output, _steps, status = run(source, max_steps=200000)

    if status != "HALTED":
        print(json.dumps({"ok": False, "output": "status=%s" % status}))
        return

    print(json.dumps({"ok": True, "output": output}))


if __name__ == "__main__":
    main()
