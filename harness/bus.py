# harness/bus.py
"""El bus de datos del coliseo: un log append-only que varios procesos de SO
independientes observan en pasivo.

Nadie llama a nadie y nadie tiene el telefono de nadie: cada nodo publica
un token `{node, value, ts, pid}` y quienes necesitan ese dato hacen polling
de `read_all`. El lock de archivo protege el append entre procesos.

No es memoria Von Neumann compartida: es el patron de dataflow real, donde
productor y consumidor estan desacoplados en el tiempo.
"""
from __future__ import annotations

import json
import os
import time

_LOCK_SUFFIX = ".lock"


def _lock(path: str, timeout: float = 10.0) -> None:
    """Crea el archivo lock con O_EXCL. En Windows, cuando el lock ya existe
    la llamada puede fallar con PermissionError (no FileExistsError) por una
    carrera del sistema de archivos: ambos se tratan igual y se reintenta.
    """
    lock_path = path + _LOCK_SUFFIX
    start = time.time()
    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return
        except (FileExistsError, PermissionError):
            if time.time() - start > timeout:
                raise TimeoutError("no pude tomar el lock de %s" % path)
            time.sleep(0.005)


def _unlock(path: str) -> None:
    try:
        os.remove(path + _LOCK_SUFFIX)
    except (FileNotFoundError, PermissionError):
        pass


def publish(path: str, node: str, value) -> None:
    """Publica un dato en el bus. No sabe ni le importa quien lo va a leer,
    ni cuando, ni en que orden respecto a otros eventos."""
    entry = {"node": node, "value": value, "ts": time.time(), "pid": os.getpid()}
    _lock(path)
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    finally:
        _unlock(path)


def read_all(path: str) -> list[dict]:
    """Lee todo lo publicado hasta ahora. Cada nodo llama esto en un loop de
    polling -- nadie le avisa activamente "ya llego tu dato"."""
    if not os.path.exists(path):
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out