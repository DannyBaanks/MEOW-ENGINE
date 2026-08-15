"""Brainfuck interpreter. Public-domain language, written from scratch."""
from __future__ import annotations

TAPE_SIZE = 30000


def _jumps(src: str) -> dict[int, int] | None:
    stack: list[int] = []
    table: dict[int, int] = {}
    for i, ch in enumerate(src):
        if ch == "[":
            stack.append(i)
        elif ch == "]":
            if not stack:
                return None
            j = stack.pop()
            table[j] = i
            table[i] = j
    return None if stack else table


def run(source: str, max_steps: int = 200000, stdin_data: str = ""):
    src = "".join(c for c in source if c in "><+-.,[]")
    table = _jumps(src)
    if table is None:
        return "", 0, "UNBALANCED"

    tape = bytearray(TAPE_SIZE)
    ptr = ip = steps = stdin_pos = 0
    out: list[str] = []

    while ip < len(src):
        if steps >= max_steps:
            return "".join(out), steps, "MAX_STEPS"
        c = src[ip]
        if c == ">":
            ptr = (ptr + 1) % TAPE_SIZE
        elif c == "<":
            ptr = (ptr - 1) % TAPE_SIZE
        elif c == "+":
            tape[ptr] = (tape[ptr] + 1) & 0xFF
        elif c == "-":
            tape[ptr] = (tape[ptr] - 1) & 0xFF
        elif c == ".":
            out.append(chr(tape[ptr]))
        elif c == ",":
            if stdin_pos < len(stdin_data):
                tape[ptr] = ord(stdin_data[stdin_pos]) & 0xFF
                stdin_pos += 1
            else:
                tape[ptr] = 0
        elif c == "[":
            if tape[ptr] == 0:
                ip = table[ip]
        elif c == "]":
            if tape[ptr] != 0:
                ip = table[ip]
        ip += 1
        steps += 1

    return "".join(out), steps, "HALTED"
