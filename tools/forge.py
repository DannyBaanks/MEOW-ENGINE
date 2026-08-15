# tools/forge.py
"""Forja un gladiador por lenguaje. Un gato, 40 lenguajes.

Diseno uniforme (decisiones del usuario: substring + constantes embebidas):

  1. Lee el pedido JSON por stdin (una linea).
  2. Si contiene `"discipline":"construct"` -> busca `"arena":"<nombre>"` y
     responde {"ok":true,"output":"<pieza>"} (pieza pre-escapada a JSON).
  3. Si no (validate) -> ok si el pedido contiene el gato canonico escapado
     como JSON: `"candidate":" /\\_/\\\n( o.o )\n > ^ <"`.
     Las 6 mutaciones ya difieren -> correcto.

Cada gladiador solo necesita: leer stdin, `contains(s, sub)`, concatenar.
El output se construye SIEMPRE por concatenacion (nunca __OK__/__FAIL__
embebidos dentro de un string literal del lenguaje).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = json.loads((ROOT / "cat" / "spec.json").read_text(encoding="utf-8"))
PIECES_RAW = {k: v["chars"] for k, v in SPEC["pieces"].items()}
CAT = " /\\_/\\\n( o.o )\n > ^ <"
ARENAS = sorted(PIECES_RAW)


def jsesc(s: str) -> str:
    return (s.replace("\\", "\\\\").replace('"', '\\"')
             .replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r"))


PIECE_ESC = {k: jsesc(v) for k, v in PIECES_RAW.items()}
CAT_ESC = jsesc(CAT)
MARKER = '"candidate":"' + CAT_ESC + '"'
DISCIPLINE = '"discipline":"construct"'
OK_OUT = "es un gato"
FAIL_OUT = "no es el gato canonico"


def lit(s: str) -> str:
    """Literal double-quoted generico (C-family). El valor del literal == s."""
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ch == "\r":
            out.append("\\r")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


# ---------------------------------------------------------------------------
# Cadena de contains-ifs (10 arenas).  line_fn(first, arena, needle_lit,
# piece_lit) -> una linea de codigo del lenguaje. Solo un arena coincide.
# ---------------------------------------------------------------------------

def if_chain(line_fn, indent: str = "  ") -> str:
    out = []
    for i, a in enumerate(ARENAS):
        needle = lit('"arena":"' + a + '"')
        piece = lit(PIECE_ESC[a])
        out.append(indent + line_fn(i == 0, a, needle, piece))
    return "\n".join(out)


def if_chain_raw(line_fn, indent: str = "  ") -> str:
    """Como if_chain pero piece = PIECES_RAW (lenguajes que serializan JSON)."""
    out = []
    for i, a in enumerate(ARENAS):
        needle = lit('"arena":"' + a + '"')
        piece = lit(PIECES_RAW[a])
        out.append(indent + line_fn(i == 0, a, needle, piece))
    return "\n".join(out)


def write_lang(name, ext, cmd, src):
    d = ROOT / "languages" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / ("gladiator." + ext)).write_text(src, encoding="utf-8", newline="\n")
    contract = {
        "language": name,
        "runtime": {"cmd": cmd, "native": True},
        "disciplines": ["construct", "validate"],
        "arenas": ARENAS,
    }
    (d / "contract.json").write_text(
        json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def gen(name, ext, cmd, src, ifs):
    s = (src
         .replace("__DISCIPLINE__", lit(DISCIPLINE))
         .replace("__MARKER__", lit(MARKER))
         .replace("__OK__", lit(OK_OUT))
         .replace("__FAIL__", lit(FAIL_OUT))
         .replace("__IFS__", ifs))
    write_lang(name, ext, cmd, s)
    return name, cmd, ROOT / "languages" / name / ("gladiator." + ext)


GENERATED: list[tuple[str, list[str], Path]] = []
def A(name, ext, cmd, src, ifs):
    GENERATED.append(gen(name, ext, cmd, src, ifs))


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------

def smoke_test(name, cmd, path):
    import shutil
    root = str(path.parent.resolve())
    runcmd = [c.replace("{root}", root) for c in cmd]
    if not Path(runcmd[0]).exists():
        full = shutil.which(runcmd[0])
        if full:
            runcmd[0] = full
    req = json.dumps({"discipline": "construct", "arena": "ears", "payload": {}},
                     sort_keys=True, separators=(",", ":"))
    try:
        p = subprocess.run(runcmd, input=req, capture_output=True, text=True, timeout=60)
    except (FileNotFoundError, OSError) as e:
        return name, "SKIP", "runtime ausente: %s" % e, ""
    try:
        resp = json.loads(p.stdout.strip())
    except Exception:
        return name, "CONSTRUCT-CRASH", p.stdout[:80], p.stderr[:120]
    if not resp.get("ok") or resp.get("output") != PIECES_RAW["ears"]:
        return name, "CONSTRUCT-WRONG", resp, ""
    req2 = json.dumps({"discipline": "validate", "arena": "ears",
                       "payload": {"candidate": CAT}},
                      sort_keys=True, separators=(",", ":"))
    try:
        p2 = subprocess.run(runcmd, input=req2, capture_output=True, text=True, timeout=60)
    except (FileNotFoundError, OSError) as e:
        return name, "SKIP", "runtime ausente: %s" % e, ""
    try:
        r2 = json.loads(p2.stdout.strip())
    except Exception:
        return name, "VALIDATE-CRASH", p2.stdout[:80], p2.stderr[:120]
    if not r2.get("ok"):
        return name, "FALSE-NEGATIVE", r2, ""
    maimed = CAT.replace("o.o", "o. ", 1)
    req3 = json.dumps({"discipline": "validate", "arena": "ears",
                       "payload": {"candidate": maimed}},
                      sort_keys=True, separators=(",", ":"))
    try:
        p3 = subprocess.run(runcmd, input=req3, capture_output=True, text=True, timeout=60)
    except (FileNotFoundError, OSError) as e:
        return name, "SKIP", "runtime ausente: %s" % e, ""
    try:
        r3 = json.loads(p3.stdout.strip())
    except Exception:
        return name, "VALIDATE-FAIL-CRASH", p3.stdout[:80], p3.stderr[:120]
    if r3.get("ok"):
        return name, "FALSE-POSITIVE", r3, ""
    return name, "OK", "", ""


# ---------------------------------------------------------------------------
# Gladiadores (24 reales construct+validate)
# ---------------------------------------------------------------------------

# --- javascript ---
_I = if_chain(lambda f, a, n, p: "%s (s.indexOf(%s) >= 0) out = %s;"
               % ("if" if f else "else if", n, p))
A("javascript", "js", ["node", "{root}/gladiator.js"], """const fs = require('fs');
const s = fs.readFileSync(0, 'utf8').toString();
let out = '';
if (s.indexOf(__DISCIPLINE__) >= 0) {
__IFS__
  process.stdout.write('{"ok":true,"output":"' + out + '"}');
} else {
  const ok = s.indexOf(__MARKER__) >= 0;
  process.stdout.write('{"ok":' + (ok ? 'true' : 'false') + ',"output":"' + (ok ? __OK__ : __FAIL__) + '"}');
}
""", _I)

# --- coffeescript ---
_I = if_chain(lambda f, a, n, p: "out = %s if 0 <= s.indexOf(%s)" % (p, n))
A("coffeescript", "coffee", ["coffee", "{root}/gladiator.coffee"], """fs = require 'fs'
s = fs.readFileSync(0, 'utf8').toString()
out = ''
if 0 <= s.indexOf(__DISCIPLINE__)
__IFS__
  process.stdout.write '{"ok":true,"output":"' + out + '"}'
else
  ok = 0 <= s.indexOf(__MARKER__)
  process.stdout.write '{"ok":' + (if ok then 'true' else 'false') + ',"output":"' + (if ok then __OK__ else __FAIL__) + '"}'
""", _I)

# --- ruby ---
_I = if_chain(lambda f, a, n, p: "out = %s if s.include?(%s)" % (p, n))
A("ruby", "rb", ["ruby", "{root}/gladiator.rb"], """s = STDIN.read
out = ""
if s.include?(__DISCIPLINE__)
__IFS__
  print '{"ok":true,"output":"' + out + '"}'
else
  ok = s.include?(__MARKER__)
  print '{"ok":' + (ok ? 'true' : 'false') + ',"output":"' + (ok ? __OK__ : __FAIL__) + '"}'
end
""", _I)

# --- php ---
_I = if_chain(lambda f, a, n, p: "%s (strpos($s, %s) !== false) $out = %s;"
               % ("if" if f else "elseif", n, p))
A("php", "php", ["php", "{root}/gladiator.php"], """<?php
$s = stream_get_contents(STDIN);
$out = "";
if (strpos($s, __DISCIPLINE__) !== false) {
__IFS__
  echo '{"ok":true,"output":"' . $out . '"}';
} else {
  $ok = strpos($s, __MARKER__) !== false;
  echo '{"ok":' . ($ok ? 'true' : 'false') . ',"output":"' . ($ok ? __OK__ : __FAIL__) . '"}';
}
""", _I)

# --- perl ---
_I = if_chain(lambda f, a, n, p: "if (index($s, %s) >= 0) { $out = %s; }" % (n, p))
A("perl", "pl", ["perl", "{root}/gladiator.pl"], """my $s = <STDIN>;
my $out = "";
if (index($s, __DISCIPLINE__) >= 0) {
__IFS__
  print "{\\"ok\\":true,\\"output\\":\\"$out\\"}";
} else {
  my $ok = index($s, __MARKER__) >= 0;
  print $ok ? "{\\"ok\\":true,\\"output\\":\\"".__OK__."\\"}"
            : "{\\"ok\\":false,\\"output\\":\\"".__FAIL__."\\"}";
}
""", _I)

# --- lua ---
_I = if_chain(lambda f, a, n, p: "%s s:find(%s, 1, true) then out = %s"
               % ("if" if f else "elseif", n, p))
A("lua", "lua", ["lua", "{root}/gladiator.lua"], """local s = io.read('*a')
local out = ""
if s:find(__DISCIPLINE__, 1, true) then
__IFS__
  end
  io.write('{"ok":true,"output":"' .. out .. '"}')
else
  if s:find(__MARKER__, 1, true) then
    io.write('{"ok":true,"output":"' .. __OK__ .. '"}')
  else
    io.write('{"ok":false,"output":"' .. __FAIL__ .. '"}')
  end
end
""", _I)

# --- golang ---
_I = if_chain(lambda f, a, n, p: 'if strings.Contains(s, %s) {\n        out = %s\n        }' % (n, p))
A("golang", "go", ["go", "run", "{root}/gladiator.go"], """package main

import (
    "io"
    "os"
    "strings"
)

func main() {
    b, _ := io.ReadAll(os.Stdin)
    var s = string(b)
    var out string
    if strings.Contains(s, __DISCIPLINE__) {
__IFS__
        os.Stdout.WriteString("{\\"ok\\":true,\\"output\\":\\"" + out + "\\"}")
    } else {
        ok := strings.Contains(s, __MARKER__)
        if ok {
            os.Stdout.WriteString("{\\"ok\\":true,\\"output\\":\\"" + __OK__ + "\\"}")
        } else {
            os.Stdout.WriteString("{\\"ok\\":false,\\"output\\":\\"" + __FAIL__ + "\\"}")
        }
    }
}
""", _I)

# --- java ---
_I = if_chain(lambda f, a, n, p: "%s (s.contains(%s)) out = %s;"
               % ("if" if f else "else if", n, p))
A("java", "java", ["java", "{root}/gladiator.java"], """import java.io.*;
public class gladiator {
    public static void main(String[] a) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        String out = "";
        if (s.contains(__DISCIPLINE__)) {
__IFS__
            System.out.print("{\\"ok\\":true,\\"output\\":\\"" + out + "\\"}");
        } else {
            boolean ok = s.contains(__MARKER__);
            System.out.print(ok ? "{\\"ok\\":true,\\"output\\":\\"" + __OK__ + "\\"}"
                                : "{\\"ok\\":false,\\"output\\":\\"" + __FAIL__ + "\\"}");
        }
    }
}
""", _I)

# --- groovy ---
_I = if_chain(lambda f, a, n, p: "if (s.contains(%s)) { output = %s }" % (n, p))
A("groovy", "groovy", ["groovy", "{root}/gladiator.groovy"], """def s = System.in.text
def output = ""
if (s.contains(__DISCIPLINE__)) {
__IFS__
  print "{\\"ok\\":true,\\"output\\":\\"${output}\\"}"
} else {
  def ok = s.contains(__MARKER__)
  print ok ? "{\\"ok\\":true,\\"output\\":\\""+__OK__+"\\"}"
           : "{\\"ok\\":false,\\"output\\":\\""+__FAIL__+"\\"}"
}
""", _I)

# --- kotlin ---
_I = if_chain(lambda f, a, n, p: "if (s.contains(%s)) { output = %s }" % (n, p))
A("kotlin", "kts", ["kotlin", "{root}/gladiator.kts"], """val s = readLine().orEmpty()
var output = ""
if (s.contains(__DISCIPLINE__)) {
__IFS__
  print("{\\"ok\\":true,\\"output\\":\\"$output\\"}")
} else {
  if (s.contains(__MARKER__)) print("{\\"ok\\":true,\\"output\\":\\""+__OK__+"\\"}")
  else print("{\\"ok\\":false,\\"output\\":\\""+__FAIL__+"\\"}")
}
""", _I)

# --- scala ---
_I = if_chain(lambda f, a, n, p: "if (s.contains(%s)) { output = %s }" % (n, p))
A("scala", "scala", ["scala", "{root}/gladiator.scala"], """object gladiator {
  def main(args: Array[String]): Unit = {
    val s = scala.io.Source.stdin.getLines().mkString(" ")
    var output = ""
    if (s.contains(__DISCIPLINE__)) {
__IFS__
      print("{\\"ok\\":true,\\"output\\":\\"" + output + "\\"}")
    } else {
      if (s.contains(__MARKER__)) print("{\\"ok\\":true,\\"output\\":\\""+__OK__+"\\"}")
      else print("{\\"ok\\":false,\\"output\\":\\""+__FAIL__+"\\"}")
    }
  }
}
""", _I)

# --- tcl ---
_I = if_chain(lambda f, a, n, p: 'if {[string first %s $s] >= 0} { set out %s }' % (n, p))
A("tcl", "tcl", ["tclsh", "{root}/gladiator.tcl"], """set s [gets stdin]
set out ""
if {[string first __DISCIPLINE__ $s] >= 0} {
__IFS__
  puts -nonewline "{\\"ok\\":true,\\"output\\":\\"$out\\"}"
} else {
  if {[string first __MARKER__ $s] >= 0} {
    set v __OK__
    set ok true
  } else {
    set v __FAIL__
    set ok false
  }
  puts -nonewline "{\\"ok\\":$ok,\\"output\\":\\"$v\\"}"
}
""", _I)

# --- swift ---
_I = if_chain(lambda f, a, n, p: "if s.contains(%s) { out = %s }" % (n, p))
A("swift", "swift", ["swift", "{root}/gladiator.swift"], """let s = readLine() ?? ""
var out = ""
if s.contains(__DISCIPLINE__) {
__IFS__
  print("{\\"ok\\":true,\\"output\\":\\"" + out + "\\"}", terminator: "")
} else {
  let ok = s.contains(__MARKER__)
  let v = ok ? __OK__ : __FAIL__
  print("{\\"ok\\":" + (ok ? "true" : "false") + ",\\"output\\":\\"" + v + "\\"}", terminator: "")
}
""", _I)

# --- haskell ---
_I = if_chain(lambda f, a, n, p: '  (%s, %s),' % (n, p), indent="    ")
A("haskell", "hs", ["runghc", "{root}/gladiator.hs"], """import Data.List (isInfixOf)
main :: IO ()
main = do
  s <- getLine
  if isInfixOf __DISCIPLINE__ s
    then putStrLn ("{\\"ok\\":true,\\"output\\":\\"" ++ piece s ++ "\\"}")
    else
      let ok = isInfixOf __MARKER__ s
          v = if ok then __OK__ else __FAIL__
      in putStrLn ("{\\"ok\\":" ++ (if ok then "true" else "false") ++ ",\\"output\\":\\"" ++ v ++ "\\"}")
piece :: String -> String
piece s = case [v | (k, v) <- table, isInfixOf k s] of
  (v:_) -> v
  []    -> ""
table :: [(String, String)]
table = [
__IFS__
    ("", "")
  ]
""", _I)

# --- julia ---
_I = if_chain(lambda f, a, n, p: "if occursin(%s, s) out = %s end" % (n, p))
A("julia", "jl", ["julia", "{root}/gladiator.jl"], """s = read(stdin, String)
out = ""
if occursin(__DISCIPLINE__, s)
__IFS__
  print("{\\"ok\\":true,\\"output\\":\\"$out\\"}")
else
  local ok = occursin(__MARKER__, s)
  local v = ok ? __OK__ : __FAIL__
  print("{\\"ok\\":", ok, ",\\"output\\":\\"$v\\"}")
end
""", _I)

# --- dart ---
_I = if_chain(lambda f, a, n, p: "if (s.contains(%s)) { out = %s; }" % (n, p))
A("dart", "dart", ["dart", "{root}/gladiator.dart"], """import 'dart:io';
void main() {
  final s = stdin.readLineSync() ?? '';
  var out = '';
  if (s.contains(__DISCIPLINE__)) {
__IFS__
    stdout.write('{\\"ok\\":true,\\"output\\":\\"$out\\"}');
  } else {
    final ok = s.contains(__MARKER__);
    final v = ok ? __OK__ : __FAIL__;
    stdout.write('{\\"ok\\":$ok,\\"output\\":\\"$v\\"}');
  }
}
""", _I)

# --- powershell ---
def lit_ps(s):
    return "'" + s.replace("'", "''") + "'"

def _ifs_ps():
    out = []
    for _i, a in enumerate(ARENAS):
        n = lit_ps('"arena":"' + a + '"')
        p = lit_ps(PIECE_ESC[a])
        out.append("  if ($s.Contains(%s)) { $out = %s }" % (n, p))
    return "\n".join(out)

PS_SRC = '''$s = [Console]::In.ReadToEnd()
$out = ""
if ($s.Contains(%s)) {
%s
  Write-Output ('{"ok":true,"output":"' + $out + '"}')
} else {
  $ok = $s.Contains(%s)
  $v = if ($ok) { %s } else { %s }
  Write-Output ('{"ok":' + $ok.ToString().ToLower() + ',"output":"' + $v + '"}')
}
''' % (lit_ps(DISCIPLINE), _ifs_ps(), lit_ps(MARKER), lit_ps(OK_OUT), lit_ps(FAIL_OUT))
write_lang("powershell", "ps1", ["powershell", "-NoProfile", "-File", "{root}/gladiator.ps1"], PS_SRC)
GENERATED.append(("powershell", ["powershell", "-NoProfile", "-File", "{root}/gladiator.ps1"],
                  ROOT / "languages" / "powershell" / "gladiator.ps1"))

# --- erlang (escript) ---
_I = if_chain(lambda f, a, n, p: '    {%s, %s},' % (n, p))
A("erlang", "escript", ["escript", "{root}/gladiator.escript"], """#!/usr/bin/env escript
main(_) ->
  S = io:get_line(""),
  case string:str(S, __DISCIPLINE__) > 0 of
    true  ->
      Out = piece(S),
      io:format("{\\"ok\\":true,\\"output\\":\\"~s\\"}", [Out]);
    false ->
      OK = string:str(S, __MARKER__) > 0,
      V = if OK -> __OK__; true -> __FAIL__ end,
      BO = if OK -> "true"; true -> "false" end,
      io:format("{\\"ok\\":~s,\\"output\\":\\"~s\\"}", [BO, V])
  end,
  init:stop().
piece(S) ->
  L = [
__IFS__
    {"", ""}
  ],
  case [V || {K, V} <- L, K =/= "", string:str(S, K) > 0] of
    [V | _] -> V;
    [] -> ""
  end.
""", _I)

# --- elixir ---
_I = if_chain(lambda f, a, n, p: "out = if String.contains?(s, %s), do: %s, else: out" % (n, p))
A("elixir", "exs", ["elixir", "{root}/gladiator.exs"], """s = IO.read(:stdio, :line)
out = ""
if String.contains?(s, __DISCIPLINE__) do
__IFS__
  IO.write("{\\"ok\\":true,\\"output\\":\\"" <> out <> "\\"}")
else
  ok = String.contains?(s, __MARKER__)
  v = if ok, do: __OK__, else: __FAIL__
  bo = if ok, do: "true", else: "false"
  IO.write("{\\"ok\\":" <> bo <> ",\\"output\\":\\"" <> v <> "\\"}")
end
""", _I)

# --- racket ---
_I = if_chain(lambda f, a, n, p: "(when (string-contains? s %s) (set! out %s))" % (n, p))
A("racket", "rkt", ["racket", "{root}/gladiator.rkt"], """#lang racket
(define s (read-line (current-input-port) 'any))
(define out "")
(if (string-contains? s __DISCIPLINE__)
  (begin
__IFS__
    (printf "{\\"ok\\":true,\\"output\\":\\"~a\\"}" out))
  (let* ([ok (string-contains? s __MARKER__)]
         [v (if ok __OK__ __FAIL__)]
         [bo (if ok "true" "false")])
    (printf "{\\"ok\\":~a,\\"output\\":\\"~a\\"}" bo v)))
""", _I)

# --- prolog (swipl) ---
_I = if_chain(lambda f, a, n, p: 'piece_table(%s, %s).' % (n, p), indent="")
A("prolog", "pl", ["swipl", "-q", "-g", "main", "-t", "halt", "{root}/gladiator.pl"], """__IFS__
piece_of(S, Out) :-
  findall(V, ( piece_table(K, V), sub_string(S, _, _, _, K) ), Vs),
  ( Vs = [V|_] -> Out = V ; Out = "" ).
main :-
  read_line_to_string(user_input, S),
  (   sub_string(S, _, _, _, __DISCIPLINE__)
  ->  piece_of(S, Out),
      format("{\\"ok\\":true,\\"output\\":\\"~w\\"}", [Out])
  ;   (   sub_string(S, _, _, _, __MARKER__)
      ->  format("{\\"ok\\":true,\\"output\\":\\"~s\\"}", [__OK__])
      ;   format("{\\"ok\\":false,\\"output\\":\\"~s\\"}", [__FAIL__])
      )
  ).
""", _I)

# --- sbcl (common lisp) ---
_I = if_chain(lambda f, a, n, p: "(when (search %s s) (setf out %s))" % (n, p))
A("sbcl", "lisp", ["sbcl", "--script", "{root}/gladiator.lisp"], """(let ((s (read-line nil nil ""))
      (out ""))
  (if (search __DISCIPLINE__ s)
      (progn
__IFS__
        (format t "{\\"ok\\":true,\\"output\\":\\"~a\\"}" out))
      (let* ((ok (search __MARKER__ s))
             (v (if ok __OK__ __FAIL__))
             (bo (if ok "true" "false")))
        (format t "{\\"ok\\":~a,\\"output\\":\\"~a\\"}" bo v))))
""", _I)

# --- fsharp (dotnet fsi) ---
_II = if_chain(lambda f, a, n, p: "if s.Contains(%s) then out <- %s" % (n, p), indent="    ")
A("fsharp", "fsx", ["dotnet", "fsi", "--quiet", "{root}/gladiator.fsx"], """let s = stdin.ReadLine()
let mutable out = ""
if s.Contains(__DISCIPLINE__) then
__IFS__
    let body = "{\\"ok\\":true,\\"output\\":\\"" + out + "\\"}"
    printf "%s" body
else
    let ok = s.Contains(__MARKER__)
    let v = if ok then __OK__ else __FAIL__
    let b = if ok then "true" else "false"
    let body2 = "{\\"ok\\":" + b + ",\\"output\\":\\"" + v + "\\"}"
    printf "%s" body2
""", _II)

# --- jq ---
_I = if_chain_raw(lambda f, a, n, p: '      %s ($s | contains(%s)) then {ok: true, output: %s}'
               % ("if" if f else "elif", n, p), indent="      ")
A("jq", "jq", ["jq", "-Rr", "-f", "{root}/gladiator.jq"], """
. as $s
| if ($s | contains(__DISCIPLINE__)) then
    ( __IFS__
      else {ok: true, output: ""} end )
  elif ($s | contains(__MARKER__)) then {ok: true, output: __OK__}
  else {ok: false, output: __FAIL__}
  end
""", _I)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    print("Generados: %d gladiadores" % len(GENERATED))
    failures = []
    for name, cmd, path in GENERATED:
        res = smoke_test(name, cmd, path)
        name, status, info, err = res
        mark = "OK " if status == "OK" else "XX "
        print("%s %-14s %s" % (mark, name, status))
        if status not in ("OK", "SKIP"):
            failures.append(res)
            if err:
                print("    stderr: %s" % err)
            if info:
                print("    info: %s" % str(info)[:120])
    if failures:
        print("\nFALLARON: %d" % len(failures))
        return 1
    print("\nTodos verdes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
