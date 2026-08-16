#!/usr/bin/env python3
"""Debug validator MARKER matching."""
import sys
sys.path.insert(0, '.')
from harness.tournament import run_tournament
from harness.protocol import encode_request

cat = run_tournament()["cat"]
print("CAT repr:", repr(cat))
req = encode_request("validate", "ears", {"candidate": cat})
print("REQ:", req)

# The MARKER we search for
marker = '"candidate":"' + cat.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
print("MARKER:", repr(marker))
print("MARKER in REQ:", marker in req)

# Also check what the gladiators actually receive
for lang in ["coffeescript", "elixir", "groovy", "kotlin", "scala", "swift"]:
    print(f"\n--- {lang} ---")
    from harness.frontier import cross
    from harness.roster import discover
    gs = [g for g in discover() if g.language == lang]
    if gs:
        r = cross(list(gs[0].cmd), lang, "validate", "ears", {"candidate": cat}, timeout_s=30)
        print(f"  verdict: {r.verdict}, ok: {r.ok}, output: {repr(r.output)[:80]}")