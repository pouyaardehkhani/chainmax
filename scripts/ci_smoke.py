"""Exercise a fresh four-record build without overwriting the committed corpus."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="chainmax-ci-") as temp:
    target=Path(temp)
    shutil.copytree(root/"configs",target/"configs")
    env={**os.environ,"PYTHONPATH":str(root/"src")}
    subprocess.run([sys.executable,"-m","chainmax","build","--accepted-limit","4"],cwd=target,env=env,check=True)
    subprocess.run([sys.executable,"-m","chainmax","audit","--all"],cwd=target,env=env,check=True,stdout=subprocess.DEVNULL)
print("Fresh four-record build and artifact audit passed.")
