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


def test_no_private_project_references():
    """El repo es publico: nada puede referirse al repo privado.

    Los terminos prohibidos se guardan como hashes truncados de SHA-256, nunca
    en claro: un guard que lista lo que prohibe publica exactamente aquello que
    intenta proteger. Se escanea *todo* el arbol (saltando binarios), no una
    allowlist de extensiones -- este repo tiene 40 lenguajes y una allowlist
    deja fuera la mayoria de ellos.
    """
    import hashlib
    import re
    from pathlib import Path

    BANNED_HASHES = {
        "070ae1d335d10a91", "222c720814e04274", "2536399e751d567c",
        "2b7847b7b705781d", "2ff690372a383758", "38a5be91af79d7e5",
        "488990162b3ea4ef", "4ed641dc6bfea6b5", "5c4c1964340aca5b",
        "64eed452db9bc876", "6a2b172f371c3020", "872491a30d60d598",
        "93962b8e2d9b27cf", "9b05efadc93ea96c", "9e406320fc2d4a8a",
        "a14c8abe8e497276", "ae310cd245d0896d", "be4291d9639fea8d",
        "c75c6c8704a2ebe5", "cf9b0fce9a46cb21", "d155b475992fe457",
        "d637c040a633c96c", "e21e9986e45822d8", "e81ec5400961dcf2",
        "ef3ce5685e884fbe", "fcb3b49543442c45",
    }
    MAX_NGRAM = 3

    def digest(s):
        return hashlib.sha256(s.encode()).hexdigest()[:16]

    root = Path(__file__).resolve().parent.parent
    skip_dirs = {".git", "target", "__pycache__", "node_modules", ".pytest_cache"}

    for path in root.rglob("*"):
        if not path.is_file() or skip_dirs & set(path.parts):
            continue
        raw = path.read_bytes()
        if 0 in raw[:8192]:
            continue  # binario
        text = raw.decode("utf-8", errors="ignore")
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        for n in range(1, MAX_NGRAM + 1):
            for i in range(len(tokens) - n + 1):
                window = tokens[i:i + n]
                for form in (" ".join(window), "".join(window)):
                    if digest(form) in BANNED_HASHES:
                        # No se incluye el termino en el mensaje: un fallo en CI
                        # publico filtraria justo lo que este test protege.
                        raise AssertionError(
                            "%s expone un termino interno prohibido "
                            "(n-grama de %d token(s) en la posicion %d)"
                            % (path.relative_to(root), n, i)
                        )
