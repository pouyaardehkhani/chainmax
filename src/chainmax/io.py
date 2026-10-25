import hashlib
import json
import os
from pathlib import Path
from importlib.metadata import version


def dumps(x):
    return json.dumps(x, sort_keys=True, indent=2, ensure_ascii=True)+"\n"


def digest(data):
    return hashlib.sha256(data.encode() if isinstance(data,str) else data).hexdigest()


def atomic(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp = path.with_name(path.name+".tmp")
    with tmp.open("w",encoding="utf-8",newline="\n") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp,path)


def versions():
    import platform
    return {"python":platform.python_version(), **{n:version(n) for n in ("chainmax-dataset","ortools","python-sat","pindakaas","jsonschema","PyYAML","psutil")}}


def source_hash(root):
    files = sorted(p for folder in ("src","schemas","configs") for p in (root/folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts and not any(part.endswith(".egg-info") for part in p.parts) and p.suffix not in (".pyc",))
    return digest("\n".join(f'{p.relative_to(root).as_posix()} {digest(p.read_bytes())}' for p in files))
