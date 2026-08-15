import shutil, os
from harness.frontier import cross
from harness.judge import attack_validator
from harness.roster import convoke, discover, discover
from harness.tournament import run_tournament

cat = run_tournament()["cat"]
print("CAT repr:", repr(cat))
guards = convoke(discover(), "validate", "ears")
print("Guards:", [g.language for g in guards])
fails = []
for g in guards:
    r = attack_validator(g, cat, "ears")
    print(g.language, r)
    if r["false_positives"] != 0:
        fails.append(g.language)
print("FAILS (fp!=0):", fails)
