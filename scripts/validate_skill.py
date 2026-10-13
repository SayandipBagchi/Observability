#!/usr/bin/env python3
"""Validate the observability plugin package. No third-party dependencies.

Run from anywhere:  python3 scripts/validate_skill.py

Checks specific to this package:

  * tenant purity   - no tenant name, alert ID, tenant event name or tenant purity term in any
                      generic file (skills/, agents/, hooks/, settings.json, README.md,
                      CONNECTORS.md, hosts/)
  * secret scan     - no intake URL, signature parameter or tenant email domain anywhere in the
                      package except recipients in tenants/<name>/config.json

Tenant names and email domains are config-driven: they come from the folder names under tenants/,
the recipient domains in each tenant config, and the untracked .private-denylist (one literal term
per line; a line with a dot is also treated as an email domain; lines starting with "re:" are
regexes and are used by scripts/leak_scan.py only). This file names no private term, and a match
that came from the denylist is reported without echoing the matched text.
  * learnings trace - every learning L1-L23, F and G maps to a file that still holds its anchor
  * no commands/    - commands were converted to skills in 0.2.0 and must not return
  * declared extras - hooks/, settings.json and CONNECTORS.md are allowed beyond the reference layout

Secret patterns are assembled from fragments so this file never matches a grep for them.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
FRONTMATTER_KEYS = {"name", "description", "metadata", "allowed-tools", "license"}

MAX_SKILL_DESCRIPTION = 1024
MAX_PLUGIN_DESCRIPTION = 500
MAX_BODY_LINES = 500

ROUTER = "observability"

DENYLIST = ROOT / ".private-denylist"


def denylist_terms() -> list[str]:
    """Literal private terms from the untracked denylist (comments, blanks and re: lines skipped)."""
    if not DENYLIST.is_file():
        return []
    out = []
    for line in DENYLIST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "re:")):
            out.append(line)
    return out


def tenant_names() -> list[str]:
    base = ROOT / "tenants"
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir() and not p.name.startswith("_"))


def _word_re(words: list[str]) -> re.Pattern | None:
    words = [w for w in words if w]
    if not words:
        return None
    return re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in words) + r")(?![\w-])",
                      re.IGNORECASE)


# Programme names: every tenant folder (public, may be echoed) and the denylist (never echoed).
TENANT_WORD_RE = _word_re(tenant_names())
PRIVATE_WORD_RE = _word_re(denylist_terms())
# Alert IDs such as ABC-01 or ABC-L4b. Placeholders use XXX-.
ALERT_ID_RE = re.compile(r"\b[A-Z]{3}-[A-Z]?\d{1,2}[a-z]?\b")
ALERT_ID_ALLOWED_PREFIX = "XXX-"
ALERT_ID_ALLOWED = {"UTF-8"}

SKILLS = {
    ROUTER: {
        "required": [
            "references/gates.md",
            "references/security.md",
            "references/run-protocol.md",
            "references/designer-quirks.md",
            "references/mechanisms.md",
            "references/registry-schema.md",
            "references/evals.md",
            "references/context-engineering.md",
            "references/observability.md",
            "references/portability.md",
            "references/learnings-trace.md",
            "templates/alert-spec.md",
            "templates/change-report.md",
            "templates/context-capsule.md",
            "templates/tenant-profile.md",
            "examples/build-report.md",
        ],
        "markers": ["model gate", "plan mode vs direct", "A0", "A2b", "A6a", "A6b", "A7",
                    "alert-design", "native-alert", "sentinel-flow", "alert-intake",
                    "delivery-verify", "alert-health", "alert-retire", "alert-watchdog", "tenant-onboard",
                    "tenants/<name>/"],
        "anti_markers": ["Parse JSON", "Name box", "/v4/duplicate/flows"],
    },
    "alert-design": {
        "required": ["references/design-rules.md", "references/baselines-and-fire-rate.md"],
        "markers": ["decision rule", "baseline", "fires per week", "Positive enumeration",
                    "approval table", ROUTER],
        "anti_markers": ["/v4/create/flows", "Parse JSON", "Code view"],
    },
    "native-alert": {
        "required": ["references/alert-management.md"],
        "markers": ["Alert Management", "data window", "config.json", "System-alert", ROUTER],
        "anti_markers": ["U+2024", "Parse JSON"],
    },
    "sentinel-flow": {
        "required": ["references/flow-build.md", "references/payload-tokens.md"],
        "markers": ["U+2024", "positive enumeration", "NO branch", "Replace", "uid", "ref",
                    "Body type", ROUTER],
        "anti_markers": ["Parse JSON", "Name box"],
    },
    "alert-intake": {
        "required": ["references/power-automate.md", "references/sheet-sync.md"],
        "markers": ["Parse JSON", "Code view", "ReceivedSerial", "Name box", "trigger card",
                    "saved copy", ROUTER],
        "anti_markers": ["/v4/duplicate/flows", "/v4/create/flows"],
    },
    "delivery-verify": {
        "required": ["references/delivery-proof.md"],
        "markers": ["A6a", "A6b", "TEST", "data window", ROUTER],
        "anti_markers": ["/v4/create/flows"],
    },
    "alert-health": {
        "required": ["references/health-checks.md"],
        "markers": ["A7", "Silent", "Noisy", "NOT CHECKED", "3×", ROUTER],
        "anti_markers": ["/v4/create/flows", "Parse JSON"],
    },
    "alert-retire": {
        "required": ["references/retire-protocol.md"],
        "markers": ["replaced_ids", "All", "Polluted", "Pause the flow", ROUTER],
        "anti_markers": ["/v4/create/flows", "Parse JSON"],
    },
    "alert-watchdog": {
        "required": ["references/watchdog-build.md", "references/watchdog-quirks.md"],
        "markers": ["Layer 1", "Layer 2", "Layer 3", "owner only", "switched off",
                    "Code view", "not delivery", "TEST", "Q35", ROUTER],
        "anti_markers": ["/v4/create/flows", "Parse JSON"],
    },
    "tenant-onboard": {
        "required": ["references/onboarding-checklist.md"],
        "markers": ["_template", "config.json", "no code edits", "not_built", ROUTER],
        "anti_markers": ["/v4/create/flows"],
    },
}

REFERENCE_MARKERS = {
    "skills/observability/references/gates.md": [
        "A0 approval", "A2b positive enumeration", "A3 read-back", "Code view", "saved copy",
        "A6a intake-proven", "A6b inbox-proven", "A7 shadow check", "is approved exactly like a threshold",
    ],
    "skills/observability/references/security.md": [
        "Power Automate trigger card", "slice every JS read from the", "S5", "uid", "ref",
        "No phone", "same turn",
    ],
    "skills/observability/references/registry-schema.md": [
        "## The replace chain", "may be blank, with a reason", "U+2024", "exclusion-approved:",
    ],
    "skills/observability/references/run-protocol.md": [
        "## Polluted rows", "## Pause protocol", "## JS output masking", "## Session hygiene",
    ],
    "skills/observability/references/designer-quirks.md": [
        "Q17", "Q18", "Q19", "Q20", "Q21", "Q22", "Q24", "Q25", "Q26", "Q27", "Q28", "Q29",
        "Q30", "Q31", "Q32", "S3", "S4",
    ],
    "skills/observability/references/context-engineering.md": ["budget", "capsule", "Screenshots"],
    "skills/observability/references/observability.md": ["Triangulation", "Drift", "A7"],
    "skills/observability/references/portability.md": ["SKILL.md", "CLAUDE_PLUGIN_ROOT", "evals"],
}

LEARNINGS_TRACE = ROOT / "skills" / ROUTER / "references" / "learnings-trace.md"
LEARNINGS_EXPECTED = {f"L{n}" for n in range(1, 24)} | {"F", "G"}

AGENTS = (
    "alert-auditor.md",
    "shadow-triangulator.md",
    "eval-runner.md",
    "builders/sentinel-flow-builder.md",
    "builders/native-alert-builder.md",
    "builders/intake-mapper.md",
    "review/approval-gate.md",
    "review/secret-exposure.md",
)

ROOT_FILES = ("README.md", "CHANGELOG.md", "LICENSE", ".gitignore")
DECLARED_EXTRAS = ("hooks/hooks.json", "settings.json", "CONNECTORS.md")
ROOT_ALLOWED = {".claude-plugin", ".gitignore", "CHANGELOG.md", "LICENSE", "README.md", "agents",
                "evals", "hosts", "scripts", "skills", "tenants", "hooks", "settings.json",
                "CONNECTORS.md", "__pycache__", ".DS_Store", ".githooks", ".private-denylist",
                ".git", ".gitattributes"}

TENANT_FILES = ("config.json", "profile.md", "journeys.md", "ref-table.md", "quirk-evidence.md",
                "intake-rules.md", "alert-registry.csv", "inventory.md", "open-items.md", "revisions.md")

EVAL_FIXTURES = ("alertlog.sample.json", "registry-excerpt.sample.csv")
EVAL_LINE = ("Score each item independently. An item that cannot be checked from the output is a "
             "fail, not a pass.")

PLUGIN_ROOT_TOKEN = "${CLAUDE_PLUGIN_ROOT}"

# Secrets: never anywhere. Tenant email domain: only in tenants/<name>/config.json.
SECRET_RE = re.compile(
    r"(\bs" r"ig=|logic[.]azure|power" r"automate[.]com|https?://prod-\d+[.])", re.IGNORECASE)
def tenant_email_domains() -> list[str]:
    domains: set[str] = set()
    for cfg in (ROOT / "tenants").glob("*/config.json"):
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for addr in list(data.get("recipients", [])) + list(data.get("watchdog", {}).get("recipients", [])):
            if "@" in addr:
                domains.add(addr.split("@", 1)[1].lower())
    domains.update(t.lower().lstrip("@") for t in denylist_terms() if "." in t and " " not in t)
    return sorted(domains)


_DOMAINS = tenant_email_domains()
TENANT_EMAIL_RE = (re.compile(r"@(" + "|".join(re.escape(d) for d in _DOMAINS) + r")\b", re.IGNORECASE)
                   if _DOMAINS else None)
ANY_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:[.][\w-]+)+")
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".csv", ".py", ".txt", ""}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def parse_frontmatter(path: Path, errors: list[str]) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{rel(path)}: must start with YAML frontmatter")
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        errors.append(f"{rel(path)}: frontmatter must close with ---")
        return {}, text
    values: dict[str, str] = {}
    for number, line in enumerate(text[4:end].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            errors.append(f"{rel(path)}: frontmatter line {number} is not a key/value pair")
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if value[:1] in {'"', "'"} and value.endswith(value[:1]):
            value = value[1:-1]
        values[key] = value
    return values, text[end + len("\n---\n"):]


def check_manifest(errors: list[str]) -> dict:
    if not MANIFEST.is_file():
        errors.append("missing .claude-plugin/plugin.json")
        return {}
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"plugin.json is not valid JSON: {exc}")
        return {}
    for key in ("name", "version", "description", "author"):
        if not data.get(key):
            errors.append(f"plugin.json is missing {key}")
    if data.get("name") != ROOT.name:
        errors.append(f"plugin.json name must match the folder name: {ROOT.name}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(data.get("version", ""))):
        errors.append("plugin.json version must be semver, for example 0.2.0")
    if len(data.get("description", "")) > MAX_PLUGIN_DESCRIPTION:
        errors.append(f"plugin.json description is over the {MAX_PLUGIN_DESCRIPTION} ceiling")
    return data


def check_skill(slug: str, spec: dict, author: str, errors: list[str]) -> None:
    base = ROOT / "skills" / slug
    skill_md = base / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"missing skills/{slug}/SKILL.md")
        return
    frontmatter, body = parse_frontmatter(skill_md, errors)
    for key in frontmatter:
        if key not in FRONTMATTER_KEYS:
            errors.append(f"skills/{slug}: unsupported core frontmatter key: {key}")
    name = frontmatter.get("name", "")
    if name != slug:
        errors.append(f"skills/{slug}: frontmatter name must match the folder name")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append(f"skills/{slug}: name must be lowercase with single hyphens")
    description = frontmatter.get("description", "").strip()
    if not description:
        errors.append(f"skills/{slug}: description must be non-empty")
    if len(description) > MAX_SKILL_DESCRIPTION:
        errors.append(f"skills/{slug}: description is {len(description)} characters, "
                      f"over the {MAX_SKILL_DESCRIPTION} ceiling")
    if re.search(r"[<>]", description):
        errors.append(f"skills/{slug}: description cannot contain angle brackets (read as XML tags at install)")
    if "Do not use" not in description:
        errors.append(f"skills/{slug}: description must state when NOT to trigger ('Do not use')")
    if slug != ROUTER and ROUTER not in description:
        errors.append(f"skills/{slug}: 'Do not use' clause should name the router for routing and gates")
    if "Use it when" not in description:
        errors.append(f"skills/{slug}: description needs trigger phrasing ('Use it when someone asks…')")
    head = skill_md.read_text(encoding="utf-8").split("\n---\n", 1)[0]
    if f"author: {author}" not in head:
        errors.append(f"skills/{slug}: frontmatter metadata must name the author: {author}")
    if re.search(r"^\s*version:", head, re.MULTILINE):
        errors.append(f"skills/{slug}: version must live only in plugin.json")
    lines = len(body.splitlines())
    if lines > MAX_BODY_LINES:
        errors.append(f"skills/{slug}: SKILL.md body is {lines} lines, over {MAX_BODY_LINES}")
    for marker in spec["markers"]:
        if marker not in body:
            errors.append(f"skills/{slug}: SKILL.md is missing behaviour marker: {marker}")
    for marker in spec["anti_markers"]:
        if marker in body:
            errors.append(f"skills/{slug}: SKILL.md holds content that belongs elsewhere: {marker}")
    for relative in spec["required"]:
        if not (base / relative).is_file():
            errors.append(f"missing skills/{slug}/{relative}")
    refs = base / "references"
    if not refs.is_dir() or not any(p.suffix == ".md" and p.stat().st_size > 400 for p in refs.iterdir()):
        errors.append(f"skills/{slug}: needs at least one substantive file in references/")
    found = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    extra = found - set(SKILLS)
    if extra and slug == ROUTER:
        errors.append(f"skills/: undeclared skill folder(s): {sorted(extra)}")


def check_references(errors: list[str]) -> None:
    for relative, markers in REFERENCE_MARKERS.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative} is missing marker: {marker}")


def check_learnings_trace(errors: list[str]) -> int:
    if not LEARNINGS_TRACE.is_file():
        errors.append("missing learnings trace")
        return 0
    seen: set[str] = set()
    for line in LEARNINGS_TRACE.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not re.fullmatch(r"L\d{1,2}|F|G", cells[0]):
            continue
        key, target, anchor = cells[0], cells[2].strip("`"), cells[3].strip("`")
        seen.add(key)
        path = ROOT / target
        if not path.is_file():
            errors.append(f"learnings trace {key}: file does not exist: {target}")
        elif anchor not in path.read_text(encoding="utf-8"):
            errors.append(f"learnings trace {key}: anchor {anchor!r} not found in {target}")
    for missing in sorted(LEARNINGS_EXPECTED - seen):
        errors.append(f"learnings trace: {missing} is not traced")
    return len(seen)


def resolve_link(base: Path, target: str) -> Path:
    if target.startswith(PLUGIN_ROOT_TOKEN):
        return (ROOT / target[len(PLUGIN_ROOT_TOKEN):].lstrip("/")).resolve()
    return (base / target).resolve()


def check_links(errors: list[str]) -> None:
    files = sorted(ROOT.glob("skills/**/*.md")) + sorted(
        p for p in ROOT.glob("tenants/**/*.md") if "source" not in p.relative_to(ROOT).parts)
    pointer_prefixes = ("references/", "templates/", "examples/", "../", "./")
    for path in files:
        base = path.parent
        parts = path.relative_to(ROOT).parts
        skill_root = (ROOT / "skills" / parts[1]).resolve() if parts[0] == "skills" else None
        text = path.read_text(encoding="utf-8")
        targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        targets += [m for m in re.findall(r"`([^`\n]+\.md)`", text)
                    if m.startswith(PLUGIN_ROOT_TOKEN) or m.startswith(pointer_prefixes)]
        for target in targets:
            if target.startswith(("http://", "https://", "mailto:", "#")) or "<" in target:
                continue
            resolved = resolve_link(base, target)
            if ROOT.resolve() not in resolved.parents:
                errors.append(f"{rel(path)}: link escapes the plugin root: {target}")
            elif not resolved.is_file():
                errors.append(f"{rel(path)}: link target does not exist: {target}")
            elif (skill_root is not None and not target.startswith(PLUGIN_ROOT_TOKEN)
                  and skill_root not in resolved.parents):
                errors.append(f"{rel(path)}: cross-skill link must use {PLUGIN_ROOT_TOKEN}: {target}")


def tenant_vocabulary() -> list[str]:
    """Terms a generic file must not carry, collected from every real tenant's config."""
    def strings(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, list):
            for v in value:
                yield from strings(v)
        elif isinstance(value, dict):
            for v in value.values():
                yield from strings(v)

    generic: set[str] = set()
    template = ROOT / "tenants" / "_template" / "config.json"
    if template.is_file():
        generic = set(strings(json.loads(template.read_text(encoding="utf-8")).get("vocabulary", {})))
    terms: set[str] = set()
    for cfg in sorted((ROOT / "tenants").glob("*/config.json")):
        if cfg.parent.name.startswith("_"):
            continue
        data = json.loads(cfg.read_text(encoding="utf-8"))
        terms.update(data.get("eventNames", []))
        terms.update(data.get("purity", {}).get("terms", []))
        terms.update(s for s in strings(data.get("vocabulary", {})) if s not in generic)
    return sorted(t for t in terms if len(t) >= 4)


def generic_files() -> list[Path]:
    paths = [p for p in ROOT.glob("skills/**/*") if p.is_file()]
    paths += [p for p in ROOT.glob("agents/**/*") if p.is_file()]
    paths += [p for p in ROOT.glob("hooks/**/*") if p.is_file()]
    paths += [p for p in ROOT.glob("hosts/**/*") if p.is_file()]
    paths += [ROOT / n for n in ("settings.json", "README.md", "CONNECTORS.md") if (ROOT / n).is_file()]
    return sorted(paths)


def check_tenant_purity(errors: list[str]) -> int:
    terms = tenant_vocabulary()
    term_res = [(t, re.compile(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])")) for t in terms]
    files = generic_files()
    for path in files:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            where = f"{rel(path)}:{number}"
            m = TENANT_WORD_RE.search(line) if TENANT_WORD_RE else None
            if m:
                errors.append(f"{where}: tenant name '{m.group(0)}' in a generic file")
            if PRIVATE_WORD_RE and PRIVATE_WORD_RE.search(line):
                errors.append(f"{where}: private term from .private-denylist in a generic file")
            for aid in ALERT_ID_RE.findall(line):
                if not aid.startswith(ALERT_ID_ALLOWED_PREFIX) and aid not in ALERT_ID_ALLOWED:
                    errors.append(f"{where}: alert ID '{aid}' in a generic file (use XXX-01)")
            for term, rx in term_res:
                if rx.search(line):
                    errors.append(f"{where}: tenant term '{term}' in a generic file")
            if ANY_EMAIL_RE.search(line):
                errors.append(f"{where}: email address in a generic file")
    return len(files)


def check_secrets(errors: list[str]) -> int:
    scanned = 0
    for path in sorted(ROOT.rglob("*")):
        if (not path.is_file() or "__pycache__" in path.parts or ".git" in path.parts
                or path.name == ".private-denylist" or path.suffix not in TEXT_SUFFIXES):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        parts = path.relative_to(ROOT).parts
        is_tenant_config = len(parts) == 3 and parts[0] == "tenants" and parts[2] == "config.json"
        for number, line in enumerate(text.splitlines(), start=1):
            if SECRET_RE.search(line):
                errors.append(f"{rel(path)}:{number}: intake URL or signature pattern")
            if TENANT_EMAIL_RE and TENANT_EMAIL_RE.search(line) and not is_tenant_config:
                errors.append(f"{rel(path)}:{number}: tenant email address outside tenants/<name>/config.json")
    return scanned


def check_tenants(errors: list[str]) -> list[str]:
    base = ROOT / "tenants"
    if not (base / "README.md").is_file():
        errors.append("missing tenants/README.md")
    names = sorted(p.name for p in base.iterdir() if p.is_dir())
    if "_template" not in names:
        errors.append("missing tenants/_template/")
    for name in names:
        for filename in TENANT_FILES:
            if not (base / name / filename).is_file():
                errors.append(f"tenants/{name}: missing {filename}")
        cfg = base / name / "config.json"
        if cfg.is_file():
            try:
                data = json.loads(cfg.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"tenants/{name}/config.json is not valid JSON: {exc}")
                continue
            if data.get("intake", {}).get("urlStoredHere") is not False:
                errors.append(f"tenants/{name}/config.json: intake.urlStoredHere must be false")
            for key in ("connectorBodyKeys",):
                extra = set(data.get(key, [])) - {"alertId", "journey", "uid", "ref"}
                if extra:
                    errors.append(f"tenants/{name}/config.json: connectorBodyKeys not allowed: {sorted(extra)}")
    template_csv = base / "_template" / "alert-registry.csv"
    if template_csv.is_file() and len(template_csv.read_text(encoding="utf-8").strip().splitlines()) != 1:
        errors.append("tenants/_template/alert-registry.csv must hold the header row only")
    return [n for n in names if not n.startswith("_")]


def check_agents(errors: list[str]) -> None:
    for relative in AGENTS:
        path = ROOT / "agents" / relative
        if not path.is_file():
            errors.append(f"missing agents/{relative}")
            continue
        frontmatter, body = parse_frontmatter(path, errors)
        stem = Path(relative).stem
        if frontmatter.get("name") != stem:
            errors.append(f"agents/{relative}: frontmatter name must equal the file stem: {stem}")
        if not frontmatter.get("description", "").strip():
            errors.append(f"agents/{relative}: needs a description")
        if not body.strip():
            errors.append(f"agents/{relative}: body is empty")
    found = sorted(str(p.relative_to(ROOT / "agents")) for p in (ROOT / "agents").rglob("*.md"))
    for extra in sorted(set(found) - set(AGENTS)):
        errors.append(f"agents/{extra}: not declared in the validator's AGENTS list")


def check_evals(errors: list[str]) -> list[str]:
    base = ROOT / "evals"
    if not (base / "README.md").is_file():
        errors.append("missing evals/README.md")
    for fixture in EVAL_FIXTURES:
        if not (base / "fixtures" / fixture).is_file():
            errors.append(f"missing evals/fixtures/{fixture}")
    names = sorted(p.name for p in base.iterdir() if p.is_dir() and p.name not in {"results", "fixtures"})
    # Current `claude plugin eval` format: no case.yaml
    # (a case.yaml needs schema_version, name and inline graders); graders are auto-discovered
    # from graders/*.md and each must open with frontmatter naming its type.
    expected_files = {"prompt.md", "graders/criteria.md", "graders/skill-fired.md"}
    for name in names:
        case = base / name
        files = {str(p.relative_to(case)) for p in case.rglob("*") if p.is_file()}
        if files != expected_files:
            errors.append(f"evals/{name}: must hold exactly {sorted(expected_files)}, found {sorted(files)}")
            continue
        for grader in ("criteria.md", "skill-fired.md"):
            gtext = (case / "graders" / grader).read_text(encoding="utf-8")
            if not re.match(r"---\ntype: (llm|tool_used)\n", gtext):
                errors.append(f"evals/{name}: graders/{grader} must open with frontmatter 'type: llm' or 'type: tool_used'")
        fired_text = (case / "graders" / "skill-fired.md").read_text(encoding="utf-8")
        target = re.search(r'\(observability:\)\?([a-z-]+)"', fired_text)
        if target and target.group(1) not in SKILLS:
            errors.append(f"evals/{name}: skill-fired input_match names a skill not in this package")
        prompt = (case / "prompt.md").read_text(encoding="utf-8")
        if not prompt.strip() or prompt.lstrip().startswith(("---", "#")):
            errors.append(f"evals/{name}: prompt.md must be a raw user turn")
        crit = (case / "graders" / "criteria.md").read_text(encoding="utf-8")
        if EVAL_LINE not in crit:
            errors.append(f"evals/{name}: criteria.md lacks the verbatim scoring line")
        n = crit.count("\n- [ ] ")
        if not 8 <= n <= 11:
            errors.append(f"evals/{name}: criteria.md has {n} items, needs 8-11")
        fired = (case / "graders" / "skill-fired.md").read_text(encoding="utf-8")
        m = fired.count("\n- [ ] ")
        if not 2 <= m <= 3:
            errors.append(f"evals/{name}: skill-fired.md has {m} items, needs 2-3")
        if ANY_EMAIL_RE.search(prompt) and "example.invalid" not in prompt:
            errors.append(f"evals/{name}: prompt.md contains an email address")
    return names


def check_root(errors: list[str]) -> None:
    for filename in ROOT_FILES:
        if not (ROOT / filename).is_file():
            errors.append(f"missing {filename}")
    for extra in DECLARED_EXTRAS:
        path = ROOT / extra
        if not path.is_file():
            errors.append(f"missing declared extra {extra}")
        elif path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{extra} is not valid JSON: {exc}")
    if (ROOT / "commands").exists():
        errors.append("commands/ must not exist: commands were converted to skills in 0.2.0")
    for entry in ROOT.iterdir():
        if entry.name not in ROOT_ALLOWED:
            errors.append(f"unexpected root entry: {entry.name}")
    settings = ROOT / "settings.json"
    if settings.is_file():
        data = json.loads(settings.read_text(encoding="utf-8")).get(ROUTER, {})
        if data.get("defaultTenant") is not None:
            errors.append("settings.json: defaultTenant must be null; tenants are resolved per request")
    hosts = ROOT / "hosts" / "openai.yaml"
    if not hosts.is_file():
        errors.append("missing hosts/openai.yaml")
    else:
        declared = re.findall(r"^\s*- name:\s*(\S+)", hosts.read_text(encoding="utf-8"), re.MULTILINE)
        if sorted(declared) != sorted(SKILLS):
            errors.append(f"hosts/openai.yaml must list each skill exactly once; found {declared}")


def main() -> int:
    errors: list[str] = []
    manifest = check_manifest(errors)
    author = (manifest.get("author") or {}).get("name", "")
    for slug, spec in SKILLS.items():
        check_skill(slug, spec, author, errors)
    check_references(errors)
    traced = check_learnings_trace(errors)
    check_links(errors)
    purity_files = check_tenant_purity(errors)
    scanned = check_secrets(errors)
    tenants = check_tenants(errors)
    check_agents(errors)
    check_root(errors)
    cases = check_evals(errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"\n{len(errors)} problem(s) found.")
        return 1

    print(f"PASS: {ROOT.name} v{manifest.get('version')} is structurally valid")
    print(f"PASS: {len(SKILLS)} skills, {len(AGENTS)} agents, no commands/")
    print("PASS: every link resolves, cross-skill links use ${CLAUDE_PLUGIN_ROOT}")
    print(f"PASS: tenant purity across {purity_files} generic files "
          f"(names, alert IDs, {len(tenant_vocabulary())} tenant terms, email addresses)")
    print(f"PASS: secret scan across {scanned} files; tenant addresses only in tenants/<name>/config.json")
    print(f"PASS: learnings trace covers {traced} items (L1-L23, F, G), every anchor present")
    print(f"PASS: {len(tenants)} tenant(s) plus _template with the full ten-file set: {', '.join(tenants)}")
    print("PASS: description ceilings respected (1024 per skill, 500 for the plugin)")
    print(f"PASS: version and author declared once, author is {author}")
    print("PASS: declared extras present: " + ", ".join(DECLARED_EXTRAS))
    print(f"PASS: {len(cases)} eval cases with graders, plus fixtures")
    for name in cases:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
