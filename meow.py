# meow.py
"""The world's most unnecessarily engineered cat."""
from __future__ import annotations

import argparse
import json
import sys

from harness.caesar import laugh, run_caesar
from harness.judge import mutations
from harness.provenance import Provenance
from harness.roster import discover
from harness.tournament import run_arena, run_tournament


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="meow", description="hace un gato")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-gladiators", action="store_true")
    group.add_argument("--arena", metavar="NAME")
    group.add_argument("--tournament", action="store_true")
    group.add_argument("--judge", action="store_true")
    group.add_argument("--caesar", action="store_true")

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2

    if args.list_gladiators:
        for g in discover():
            print("%-12s %-24s %s" % (
                g.language, ",".join(g.disciplines) or "-", ",".join(g.arenas) or "-"))
        return 0

    if args.arena:
        result = run_arena(args.arena, discover(), Provenance())
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    if args.tournament:
        result = run_tournament()
        print(result["cat"])
        print(laugh().strip())
        return 0

    if args.judge:
        result = run_tournament()
        for name, maimed in mutations(result["cat"]):
            print("=== %s ===" % name)
            print(maimed)
        return 0

    if args.caesar:
        print(run_caesar()["cat"])
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())