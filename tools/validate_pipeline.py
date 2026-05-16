#!/usr/bin/env python3
"""ASG Content OS v2 — pipeline + contract validator (stdlib only).

Proves the skeleton is self-consistent, not paper:
  1. every run envelope conforms to schemas/envelope.schema.json (required
     keys / enums / patterns) and to its skill's io-schema `skill` const;
  2. every library_ref in every envelope + dossier RESOLVES to a real
     entry in libraries/*/*.json  (this is the Gate-6 contract, enforced);
  3. the run's envelope chain wires correctly via next_skill (incl. the
     editorial-gate block->fix->pass retry loop);
  4. the Article Type Parameter Table is consistent between
     asg-publishing-gate.md (Single Source of Truth) and
     asg-editorial-gate/io-schema.json $defs (the mirror).

Exit 0 = all green. Exit 1 = at least one failure.
Usage:  python3 tools/validate_pipeline.py [run_id ...]   (default: ASG-044)
"""
import json, re, sys, glob, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok, fail = [], []


def check(cond, msg):
    (ok if cond else fail).append(msg)
    print(("  PASS " if cond else "  FAIL ") + msg)


def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)


# ---- 1. build the Library ID universe -------------------------------------
def library_ids():
    ids = set()
    for jp in glob.glob(os.path.join(ROOT, "libraries", "**", "*.json"), recursive=True):
        data = json.load(open(jp, encoding="utf-8"))
        for key in ("facts", "cases", "sources", "voices", "topics",
                    "data_points"):
            for row in data.get(key, []):
                if isinstance(row, dict) and "id" in row:
                    ids.add(row["id"])
    return ids


LIB_IDS = library_ids()
REF_RE = re.compile(
    r"^(ASG-[A-Z]+-[0-9]{3,}|(FACT|CASE|SOURCE|VOICE|TOPIC)-[A-Za-z0-9-]+)$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
ART_RE = re.compile(r"^ASG-(\d{3,}|BM-\d{4}W\d{1,2}|AUDIT-\d{3,}|MA-\d{4}-\d{2})$")
ENV_REQUIRED = ["schema_version", "skill", "skill_version", "run_id",
                "article_id", "stage", "timestamp", "status", "input", "output"]

# skill name -> io-schema path. Single source: discovered, then asserted
# against the envelope enum so a new skill cannot silently bypass the contract.
IO_SCHEMA = {
    "asg-strategic-filter": "skills/pre-production/asg-strategic-filter/io-schema.json",
    "asg-keyword-researcher": "skills/pre-production/asg-keyword-researcher/io-schema.json",
    "asg-seo-writer-v2": "skills/production/asg-seo-writer-v2/io-schema.json",
    "asg-editorial-gate": "skills/quality-control/asg-editorial-gate/io-schema.json",
    "asg-voice-checker": "skills/quality-control/asg-voice-checker/io-schema.json",
    "asg-geo-benchmarker": "skills/feedback/asg-geo-benchmarker/io-schema.json",
    "asg-monthly-auditor": "skills/feedback/asg-monthly-auditor/io-schema.json",
    "asg-stock-auditor": "skills/utility/asg-stock-auditor/io-schema.json",
    "asg-facebook-page": "skills/distribution/asg-facebook-page/io-schema.json",
    "asg-facebook-groups": "skills/distribution/asg-facebook-groups/io-schema.json",
    "asg-short-video-scripter": "skills/distribution/asg-short-video-scripter/io-schema.json",
    "asg-platform-polisher": "skills/distribution/asg-platform-polisher/io-schema.json",
}
ENVELOPE_SKILL_ENUM = set(
    load("schemas/envelope.schema.json")["properties"]["skill"]["enum"])
SKILL_ENUM = set(IO_SCHEMA) | ENVELOPE_SKILL_ENUM
STAGE_ENUM = set(
    load("schemas/envelope.schema.json")["properties"]["stage"]["enum"])
STATUS_ENUM = {"ok", "blocked", "flagged", "modify", "error"}


def validate_envelope(path, env):
    tag = os.path.basename(path)
    for k in ENV_REQUIRED:
        check(k in env, f"{tag}: required key '{k}' present")
    check(env.get("schema_version") == "2.0", f"{tag}: schema_version==2.0")
    check(env.get("skill") in SKILL_ENUM, f"{tag}: skill in enum ({env.get('skill')})")
    check(bool(SEMVER_RE.match(env.get("skill_version", ""))), f"{tag}: skill_version semver")
    check(env.get("stage") in STAGE_ENUM, f"{tag}: stage in enum")
    check(env.get("status") in STATUS_ENUM, f"{tag}: status in enum")
    check(bool(ART_RE.match(env.get("article_id", ""))), f"{tag}: article_id pattern")
    try:
        datetime.datetime.fromisoformat(env.get("timestamp", "").replace("Z", "+00:00"))
        tsok = True
    except Exception:
        tsok = False
    check(tsok, f"{tag}: timestamp ISO-8601")
    check(isinstance(env.get("input"), dict), f"{tag}: input is object")
    check(isinstance(env.get("output"), dict), f"{tag}: output is object")
    for r in env.get("library_refs", []):
        check(bool(REF_RE.match(r)), f"{tag}: library_ref '{r}' well-formed")
        check(r in LIB_IDS, f"{tag}: library_ref '{r}' RESOLVES in libraries/ (Gate-6 contract)")
    # skill const wiring is real
    sk = env.get("skill")
    if sk in IO_SCHEMA:
        const = load(IO_SCHEMA[sk]).get("properties", {}).get("skill", {}).get("const")
        check(const == sk, f"{tag}: io-schema skill const matches ({const})")


def validate_chain(run):
    rundir = os.path.join("data", "runs", run)
    files = sorted(glob.glob(os.path.join(ROOT, rundir, "[0-9]*.json")))
    check(len(files) > 0, f"{run}: has envelope files")
    envs = []
    for fp in files:
        rel = os.path.relpath(fp, ROOT)
        env = json.load(open(fp, encoding="utf-8"))
        print(f"\n[{rel}]")
        validate_envelope(fp, env)
        envs.append((os.path.basename(fp), env))
    # first skill must be the filter
    if envs:
        check(envs[0][1]["skill"] == "asg-strategic-filter",
              f"{run}: pipeline starts with asg-strategic-filter")
    # next_skill wiring (gate retry: a 'blocked' gate may be followed by another gate attempt)
    for i in range(len(envs) - 1):
        name, e = envs[i]
        nxt = envs[i + 1][1]["skill"]
        ns = e.get("next_skill")
        if e["skill"] == "asg-editorial-gate" and e["status"] == "blocked":
            check(envs[i + 1][1]["skill"] == "asg-editorial-gate",
                  f"{run}: blocked gate is followed by a gate retry")
        else:
            check(ns == nxt, f"{run}: {name} next_skill='{ns}' -> next file skill='{nxt}'")
    # terminal envelope ends the chain
    if envs:
        last = envs[-1][1]
        check(last.get("next_skill") in (None, "null"),
              f"{run}: terminal envelope next_skill is null")
    return envs


def validate_dossier(run):
    dp = os.path.join("data", "runs", run, "dossier.json")
    if not os.path.exists(os.path.join(ROOT, dp)):
        return
    d = load(dp)
    print(f"\n[{dp}]")
    for k in ("article_id", "run_id", "topic", "article_type"):
        check(k in d, f"dossier: required key '{k}'")
    for r in d.get("library_refs", []):
        check(r in LIB_IDS, f"dossier: library_ref '{r}' RESOLVES")
    # dossier.draft asg_data_refs must all resolve (Gate-6 at dossier level)
    refs = (d.get("draft") or {}).get("asset_manifest", {}).get("asg_data_refs", [])
    for r in refs:
        check(r in LIB_IDS, f"dossier.draft asg_data_ref '{r}' RESOLVES")


def validate_standalone(run):
    """Bypass/utility runs (benchmarker, stock-auditor, keyword fixture) emit a
    single non-numbered envelope (audit.json / keyword.json / benchmark.json)
    rather than a numbered main chain. Validate envelope conformance + ref
    resolution, skip chain/ordering logic."""
    rundir = os.path.join(ROOT, "data", "runs", run)
    files = sorted(p for p in glob.glob(os.path.join(rundir, "*.json"))
                   if os.path.basename(p) != "dossier.json"
                   and not re.match(r"^[0-9]", os.path.basename(p)))
    for fp in files:
        rel = os.path.relpath(fp, ROOT)
        env = json.load(open(fp, encoding="utf-8"))
        print(f"\n[{rel}] (standalone)")
        validate_envelope(fp, env)
        ns = env.get("next_skill")
        check(ns in (None, "null") or ns in IO_SCHEMA,
              f"{run}: standalone next_skill is null or a registered skill ({ns})")
    return files


def discover_runs():
    base = os.path.join(ROOT, "data", "runs")
    out = []
    for d in sorted(os.listdir(base)):
        p = os.path.join(base, d)
        if not os.path.isdir(p):
            continue
        chained = bool(glob.glob(os.path.join(p, "[0-9]*.json")))
        standalone = [f for f in glob.glob(os.path.join(p, "*.json"))
                      if os.path.basename(f) != "dossier.json"
                      and not re.match(r"^[0-9]", os.path.basename(f))]
        if chained or standalone:
            out.append((d, "chain" if chained else "standalone"))
    return out


def validate_param_table_consistency():
    print("\n[cross-file: Article Type Parameter Table SSoT]")
    defs = load("skills/quality-control/asg-editorial-gate/io-schema.json")["$defs"]["article_type_params"]
    expected = {
        "pillar":   {"word_count": [3000, 5000], "h2_count": [6, 7], "internal_links": 4, "external_links": 10, "asg_data_refs": 9, "case_refs": 2},
        "share":    {"word_count": [2000, 3000], "h2_count": [5, 6], "internal_links": 3, "external_links": 8, "asg_data_refs": 5, "case_refs": 1},
        "response": {"word_count": [1200, 2000], "h2_count": [3, 4], "internal_links": 2, "external_links": 5, "asg_data_refs": 3, "case_refs": 1},
    }
    for t, exp in expected.items():
        for k, v in exp.items():
            check(defs[t][k] == v, f"io-schema $defs {t}.{k}=={v} (got {defs[t].get(k)})")
    gate_md = open(os.path.join(ROOT, "rulebooks", "asg-publishing-gate.md"), encoding="utf-8").read()
    for token in ("3000–5000", "2000–3000", "1200–2000"):
        check(token in gate_md, f"publishing-gate.md §A contains word band '{token}' (SSoT aligned)")


def validate_skill_schemas():
    print("\n[all skill io-schemas — envelope conformance + enum-todo resolved]")
    for name, rel in sorted(IO_SCHEMA.items()):
        check(os.path.exists(os.path.join(ROOT, rel)), f"{name}: io-schema file exists")
        if not os.path.exists(os.path.join(ROOT, rel)):
            continue
        s = load(rel)
        refs = [a.get("$ref") for a in s.get("allOf", [])]
        check("https://asg-content-os/schemas/envelope.schema.json" in refs,
              f"{name}: io-schema allOf $ref envelope")
        check(s.get("properties", {}).get("skill", {}).get("const") == name,
              f"{name}: skill const == dir name")
        check(name in ENVELOPE_SKILL_ENUM,
              f"{name}: present in envelope.schema.json skill enum (enum-todo resolved)")
        check("input" in s.get("properties", {}) and "output" in s.get("properties", {}),
              f"{name}: io-schema declares input + output")
    # discovered skill dirs must all be registered (no orphan skill bypassing lint)
    found = {os.path.basename(os.path.dirname(p))
             for p in glob.glob(os.path.join(ROOT, "skills", "*", "*", "io-schema.json"))}
    for d in sorted(found):
        check(d in IO_SCHEMA, f"skill dir '{d}' is registered in validator IO_SCHEMA")
    # every envelope-enum skill must have an io-schema (no dangling enum entry)
    for e in sorted(ENVELOPE_SKILL_ENUM):
        check(e in IO_SCHEMA, f"envelope enum skill '{e}' has a registered io-schema")


def main():
    if len(sys.argv) > 1:
        runs = [(r, None) for r in sys.argv[1:]]
    else:
        runs = discover_runs()  # auto-discover every run dir, classified
    print(f"Library ID universe: {len(LIB_IDS)} ids loaded "
          f"| {len(IO_SCHEMA)} skills registered "
          f"| {len(runs)} runs\n" + "=" * 64)
    for run, kind in runs:
        # explicit CLI arg with unknown kind: detect from disk
        if kind is None:
            p = os.path.join(ROOT, "data", "runs", run)
            kind = "chain" if glob.glob(os.path.join(p, "[0-9]*.json")) else "standalone"
        print(f"\n### RUN {run} [{kind}] " + "#" * 32)
        if kind == "chain":
            validate_chain(run)
            validate_dossier(run)
        else:
            validate_standalone(run)
    validate_skill_schemas()
    validate_param_table_consistency()
    print("\n" + "=" * 64)
    print(f"RESULT: {len(ok)} passed, {len(fail)} failed")
    if fail:
        print("\nFAILURES:")
        for m in fail:
            print("  - " + m)
        sys.exit(1)
    print("ALL GREEN — pipeline contract is self-consistent.")
    sys.exit(0)


if __name__ == "__main__":
    main()
