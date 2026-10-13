#!/usr/bin/env python3
"""Scan the repo for private terms, secrets and real email domains. No third-party dependencies.

Run:  python3 scripts/leak_scan.py            # whole working tree
      python3 scripts/leak_scan.py --staged   # only files staged for commit (pre-commit hook)

Private terms come from the untracked `.private-denylist` at the repo root: one term per line,
matched case-insensitively on word boundaries; a line starting with `re:` is a regex; `#` starts a
comment. The denylist itself is never committed (see .gitignore) and never scanned.

Built-in checks, always on:
  * URLs other than github.com / example.* / claude.com / anthropic.com links in docs
  * the intake signature parameter and automation-host patterns
  * email addresses whose domain is not example.com, example.org or example.invalid

Output names the file, line and which rule matched. It NEVER prints the matched text, so a scan
log cannot itself leak a private term.

Exit 0 when clean, 1 on any hit.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DENYLIST = ROOT / ".private-denylist"
SKIP_DIRS = {".git", "__pycache__", "_private", "results", "runs"}
SKIP_FILES = {".private-denylist"}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".csv", ".py", ".txt", ".sh", ""}

# Assembled from fragments so this file never matches a grep for them.
SECRET_RE = re.compile(
    r"(\bs" r"ig=|logic[.]azure|power" r"automate[.]com|https?://prod-\d+[.]|[?&]sv=\d|[?&]sp=[a-z])",
    re.IGNORECASE)
URL_RE = re.compile(r"https?://([A-Za-z0-9.-]+)", re.IGNORECASE)
URL_ALLOWED = re.compile(
    r"^(github\.com|raw\.githubusercontent\.com|(www\.)?example\.(com|org|invalid)|"
    r"(docs\.|www\.)?claude\.com|(docs\.|www\.)?anthropic\.com|opensource\.org)$", re.IGNORECASE)
EMAIL_RE = re.compile(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)")
EMAIL_ALLOWED = {"example.com", "example.org", "example.invalid", "users.noreply.github.com",
                 "anthropic.com"}


def load_denylist() -> list[tuple[str, re.Pattern]]:
    rules: list[tuple[str, re.Pattern]] = []
    if not DENYLIST.is_file():
        return rules
    for n, raw in enumerate(DENYLIST.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("re:"):
            rules.append((f"denylist line {n} (regex)", re.compile(line[3:], re.IGNORECASE)))
        else:
            rules.append((f"denylist line {n}",
                          re.compile(r"(?<![\w-])" + re.escape(line) + r"(?![\w-])", re.IGNORECASE)))
    return rules


def staged_files() -> list[Path]:
    out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [ROOT / p for p in out.splitlines() if p]


def all_files() -> list[Path]:
    files = []
    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            files.append(p)
    return sorted(files)


def scan(paths: list[Path]) -> int:
    rules = load_denylist()
    hits = 0
    scanned = 0
    for path in paths:
        if path.name in SKIP_FILES or not path.is_file():
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in {"pre-commit"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        rel = path.relative_to(ROOT)
        for number, line in enumerate(text.splitlines(), start=1):
            for label, rx in rules:
                if rx.search(line):
                    print(f"HIT {rel}:{number}: {label}")
                    hits += 1
            if SECRET_RE.search(line):
                print(f"HIT {rel}:{number}: secret or intake-host pattern")
                hits += 1
            for host in URL_RE.findall(line):
                if not URL_ALLOWED.match(host.rstrip(".")):
                    print(f"HIT {rel}:{number}: URL to a host outside the allowlist")
                    hits += 1
            for domain in EMAIL_RE.findall(line):
                if domain.lower() not in EMAIL_ALLOWED:
                    print(f"HIT {rel}:{number}: email address with a non-example domain")
                    hits += 1
    note = f"{len(rules)} denylist rules" if rules else "no .private-denylist found (built-in checks only)"
    print(f"{'CLEAN' if not hits else 'LEAKS'}: {hits} hit(s) across {scanned} files; {note}")
    return 1 if hits else 0


def main() -> int:
    paths = staged_files() if "--staged" in sys.argv[1:] else all_files()
    return scan(paths)


if __name__ == "__main__":
    sys.exit(main())
