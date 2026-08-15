import subprocess as s, shutil, os
from harness.roster import discover
from harness.tournament import run_tournament

cat = run_tournament()["cat"]
req = '{"arena":"ears","discipline":"validate","payload":{"candidate":"' + cat.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n') + '"}}'
print("REQ:", req)
print("CAT:", repr(cat))
for g in discover():
    if g.language in ('groovy','kotlin','scala','coffeescript','elixir'):
        cmd = list(g.cmd)
        if not os.path.exists(cmd[0]):
            full = shutil.which(cmd[0])
            if full:
                cmd[0] = full
        p = s.run(cmd, input=req, capture_output=True, text=True, timeout=30)
        print(g.language, ':', p.stdout[:120], '| ERR:', p.stderr[-200:])
