"""Compatibility entry point for writing the current audited corpus documentation."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name("write_status.py")),run_name="__main__")
