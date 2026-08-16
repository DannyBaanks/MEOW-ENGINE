# languages/brainfuck/adapter.py
"""Brainfuck adapter: runs the massive Brainfuck engine (engine.bf)."""
import json
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve()
ENGINE_RUNNER = ROOT.parents[2] / "run_bf_engine.py"


def main():
    req = json.loads(sys.stdin.read())

    discipline = req.get("discipline", "construct")
    arena = req.get("arena", "ears")

    # Call the Python wrapper that executes the massive Brainfuck engine
    result = subprocess.run(
        [sys.executable, str(ENGINE_RUNNER), discipline, arena],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        print(json.dumps({"ok": False, "output": f"runner failed: {result.stderr}"}))
        return

    try:
        response = json.loads(result.stdout.strip())
        print(json.dumps(response))
    except json.JSONDecodeError:
        print(json.dumps({"ok": False, "output": f"invalid JSON from runner: {result.stdout[:100]}"}))


if __name__ == "__main__":
    main()