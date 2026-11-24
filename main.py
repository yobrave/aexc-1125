"""aexc-1125: one-line AI excuse, deadline voice; gate 200 chars."""

import json
import os
import pathlib
import sys

LIMIT = 200


def load_source_file():
    bench = pathlib.Path(__file__).resolve().parent
    raw = (bench / "entry.txt").read_text(encoding="utf-8")
    return bench, [chunk for chunk in (part.strip() for part in raw.splitlines()) if chunk]


def audit(line):
    if not line:
        sys.exit("audit failed: empty excuse")
    if len(line) > LIMIT:
        sys.exit("audit failed: %d chars over %d" % (len(line), LIMIT))
    return line


def emit(bench, line):
    target = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or bench)
    target.mkdir(parents=True, exist_ok=True)
    out = target / "entry.txt"
    out.write_text(line + "\n", encoding="utf-8", newline="\n")
    return out


bench, parts = load_source_file()
line = audit(parts[0] if parts else "")
out = emit(bench, line)
print(json.dumps({"file": out.as_posix(), "chars": len(line), "within_limit": len(line) <= LIMIT, "voice": "deadline-excuse", "audited": True}))
