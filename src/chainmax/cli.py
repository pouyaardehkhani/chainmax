import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(prog="chainmax")
    sub = parser.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    p = sub.add_parser("build")
    p.add_argument("--config",default="configs/v1.yaml")
    p.add_argument("--accepted-limit",type=int,default=1000)
    p.add_argument("--resume",action="store_true")
    p = sub.add_parser("audit")
    p.add_argument("--dataset",default="data/chainmax-1k.jsonl")
    p.add_argument("--all",action="store_true",required=True)
    p = sub.add_parser("package")
    p.add_argument("--dataset",default="data/chainmax-1k.jsonl")
    p.add_argument("--output",default="releases/v1.0.0")
    p = sub.add_parser("review-import")
    p.add_argument("--file",required=True)
    args = parser.parse_args()
    root = Path.cwd()
    if args.command == "doctor":
        from .io import versions
        from .domain import fixture
        from .model_builder import build_ir
        from .encoding import compile_wcnf,solve
        from .native_reference import solve as native
        from .checking import check
        d = fixture()
        a = native(d)
        b = solve(*compile_wcnf(build_ir(d)))
        if a["status"] != "OPTIMAL" or b["status"] != "OPTIMAL" or a["cost"] != 9 or b["cost"] != 9 or not check(d,b["assignment"])["valid"]:
            raise SystemExit("fixture failed")
        print(json.dumps({"versions":versions(),"fixture_optimum":9,"status":"OK"},indent=2))
    elif args.command == "build":
        from .pipeline import build
        import os
        lock=root/"audit/build.lock"
        lock.parent.mkdir(parents=True,exist_ok=True)
        try:
            handle=lock.open("x",encoding="utf-8")
        except FileExistsError:
            raise SystemExit("Build lock exists; check the recorded PID before removing a stale audit/build.lock")
        try:
            handle.write(str(os.getpid())); handle.close()
            build(root,root/args.config,args.accepted_limit,args.resume)
        finally:
            lock.unlink(missing_ok=True)
    elif args.command == "audit":
        from .release import audit
        report = audit(root,Path(args.dataset))
        print(json.dumps(report,indent=2))
        if report["errors"]:
            raise SystemExit(1)
    elif args.command == "package":
        from .release import package
        print(json.dumps(package(root,Path(args.dataset),Path(args.output)),indent=2))
    else:
        from .release import import_reviews
        import_reviews(root,Path(args.file))
