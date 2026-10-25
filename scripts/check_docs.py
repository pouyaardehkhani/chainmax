"""Verify local Markdown links and execute documented Python examples quietly."""
import contextlib
import io
from pathlib import Path
import re
import yaml

root=Path.cwd()
errors=[]
files=[*root.glob("*.md"),*(root/"docs").glob("*.md")]
for file in files:
    text=file.read_text(encoding="utf-8")
    for link in re.findall(r"\]\(([^)]+)\)",text):
        if "://" in link or link.startswith("#"): continue
        if not (file.parent/link.split("#")[0]).exists(): errors.append(f"{file.name}: {link}")
for file in [root/"README.md",root/"docs/reproduction.md"]:
    for snippet in re.findall(r"```python\n(.*?)\n```",file.read_text(),flags=re.S):
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(snippet,str(file),"exec"),{})
citation=yaml.safe_load((root/"CITATION.cff").read_text())
assert citation["title"]=="ChainMax-1K" and citation["authors"][0]["name"]=="pouyaardehkhani"
if errors: raise SystemExit("Broken links: "+str(errors))
print(f"Checked local links in {len(files)} documents and executed README/reproduction Python examples.")
