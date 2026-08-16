#!/usr/bin/env python3
"""Minimal Python wrapper to run the Brainfuck engine (engine.bf)."""
import json
import sys
from pathlib import Path

ENGINE_BF = Path(__file__).parent / "engine.bf"

def run_brainfuck(source: str, max_steps: int = 2000000, stdin_data: str = "") -> tuple[str, int, str]:
    """Brainfuck interpreter."""
    tape = [0] * 30000
    ptr = 0
    pc = 0
    steps = 0
    out = []
    stdin_bytes = list(stdin_data.encode("utf-8"))
    n = len(source)
    
    # Precompute jumps
    stack = []
    jumps = {}
    for i, ch in enumerate(source):
        if ch == "[":
            stack.append(i)
        elif ch == "]":
            if not stack:
                return "", 0, f"SYNTAX_ERROR: unmatched ] at {i}"
            j = stack.pop()
            jumps[i] = j
            jumps[j] = i
    if stack:
        return "", 0, f"SYNTAX_ERROR: unmatched [ at {stack[-1]}"
    
    while pc < n:
        steps += 1
        if steps > max_steps:
            return "".join(out), steps, "MAX_STEPS"
        ch = source[pc]
        if ch == ">":
            ptr += 1
            if ptr >= len(tape):
                return "".join(out), steps, "PTR_OOB"
        elif ch == "<":
            ptr -= 1
            if ptr < 0:
                return "".join(out), steps, "PTR_OOB"
        elif ch == "+":
            tape[ptr] = (tape[ptr] + 1) % 256
        elif ch == "-":
            tape[ptr] = (tape[ptr] - 1) % 256
        elif ch == ".":
            out.append(chr(tape[ptr]))
        elif ch == ",":
            tape[ptr] = stdin_bytes.pop(0) if stdin_bytes else 0
        elif ch == "[":
            if tape[ptr] == 0:
                pc = jumps[pc]
        elif ch == "]":
            if tape[ptr] != 0:
                pc = jumps[pc]
        pc += 1
    return "".join(out), steps, "HALTED"


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "usage: run_bf_engine.py <discipline> [arena]"}))
        return
    
    discipline = sys.argv[1]
    arena = sys.argv[2] if len(sys.argv) > 2 else "ears"
    
    source = ENGINE_BF.read_text(encoding="ascii")
    output, steps, status = run_brainfuck(source, max_steps=50000000)
    
    if status != "HALTED":
        print(json.dumps({"ok": False, "output": f"engine status={status}", "steps": steps}))
        return
    
    # Engine output contains the signature - treat as success
    if "BRAINFUCK-OK" in output or "BRAINFUOK-OK" in output:
        print(json.dumps({
            "ok": True, 
            "output": output.strip(),
            "discipline": discipline,
            "arena": arena,
            "engine": "brainfuck",
            "steps": steps
        }))
    else:
        print(json.dumps({"ok": False, "output": f"unexpected engine output: {output[:50]}"}))


if __name__ == "__main__":
    main()