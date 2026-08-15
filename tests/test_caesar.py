# tests/test_caesar.py
from harness.caesar import laugh, run_caesar

CAT = " /\\_/\\\n( o.o )\n > ^ <"


def test_caesar_halts():
    assert run_caesar()["status"] == "HALTED"


def test_caesar_produces_the_cat_alone():
    assert run_caesar()["cat"] == CAT


def test_caesar_is_deterministic():
    assert run_caesar()["cat"] == run_caesar()["cat"]


def test_the_laugh_is_generated_not_hardcoded():
    """Regla 3 del spec: la risa la produce el pipeline, no un literal."""
    import inspect
    import harness.caesar as mod
    assert "JAJAJA" not in inspect.getsource(mod)
    assert laugh().strip() == "JAJAJA"