# tests/test_interpreters.py
from interpreters.brainfuck import run as bf
from interpreters.jajaja import run as ja


def test_brainfuck_hello():
    out, _steps, status = bf("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.")
    assert status == "HALTED"
    assert out == "Hello"


def test_brainfuck_rejects_unbalanced():
    assert bf("[[[")[2] == "UNBALANCED"


def test_brainfuck_respects_the_step_budget():
    assert bf("+[]", max_steps=50)[2] == "MAX_STEPS"


def test_jajaja_rewrites():
    out, _steps, status = ja("X::=~JA\n\n::=\n\nXXX\n")
    assert status == "HALTED"
    assert out == "JAJAJA"


def test_no_isyco_anywhere():
    """El repo es publico: nada puede referirse al repo privado."""
    from pathlib import Path
    banned = ["workspace/assembly", "IsycoLangs", "bridge_core", "Capability",
              "Systembility", "Sentinel", "Supreme Court", "ExecutionContext",
              "Representation Registry", "Agnostic Substrate", "Internal Engine"]
    root = Path(__file__).resolve().parent.parent
    me = Path(__file__).resolve()
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "target" in path.parts:
            continue
        if path.resolve() == me:
            continue  # este archivo lista los terminos para poder prohibirlos
        if path.suffix not in (".py", ".md", ".json", ".yaml", ".toml", ".rs", ".bf", ".jaja"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in banned:
            assert term not in text, "%s menciona '%s'" % (path.name, term)
