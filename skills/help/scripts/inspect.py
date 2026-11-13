#!/usr/bin/env python3
"""Read-only inventory of CStack artifacts and one next-skill recommendation."""

import argparse
import hashlib
import json
import os
import re
from pathlib import Path


SKIP = {".git", ".agents", ".claude", ".cursor", "node_modules", ".venv", "__pycache__", ".tools", ".models", "skills"}
OPEN_LEDGER = re.compile(r"(?im)^(?:status|review|validation)\s*:\s*(open|unreviewed|unverified|pending)\b|^\s*-\s+\[\s\]\s+\S")
UNCERTAIN = {"uncertain", "unresolved", "proposed", "pending"}
EXERCISES = 13


def digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_json(path):
    try:
        if path.stat().st_size > 300_000:
            return None
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def load_jsonl(path, limit=40):
    rows = []
    try:
        if path.stat().st_size > 2_000_000:
            return rows
        with path.open(encoding="utf-8") as handle:
            for index, line in enumerate(handle):
                if index >= limit:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict):
                    rows.append(value)
    except (OSError, UnicodeError):
        return rows
    return rows


def rel(root, path):
    return path.resolve().relative_to(root.resolve()).as_posix()


def inside(root, recorded):
    if not isinstance(recorded, str) or not recorded:
        return None
    candidate = Path(recorded)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        candidate = candidate.resolve()
    except OSError:
        return None
    root = root.resolve()
    if candidate.is_file() and (candidate == root or root in candidate.parents):
        return candidate
    return None


def judgment_text(row):
    for key in ("judgment", "label", "verdict", "expert_judgment"):
        value = row.get(key)
        if isinstance(value, str) and value.strip() and value.strip().lower() not in UNCERTAIN:
            return value.strip()
        if isinstance(value, dict):
            if str(value.get("status", "")).lower() in UNCERTAIN:
                continue
            for inner in ("label", "verdict", "statement", "text"):
                text = value.get(inner)
                if isinstance(text, str) and text.strip() and text.strip().lower() not in UNCERTAIN:
                    return text.strip()
    return None


def replay_ready(row):
    if not (row.get("example_id") or row.get("record_id")):
        return False
    if row.get("unresolved") or row.get("replay_blockers"):
        return False
    if judgment_text(row) is None:
        return False
    if not any(row.get(key) for key in ("criterion", "criterion_id", "rubric_id")):
        return False
    return any(row.get(key) for key in ("input", "output", "reviewed_output", "artifact"))


def is_case(row):
    return isinstance(row.get("id"), str) and bool(row["id"]) and any(key in row for key in ("expected", "request", "input"))


def is_record(row):
    return bool(row.get("example_id") or row.get("record_id"))


def pending_cards(value):
    if not isinstance(value, dict):
        return False
    for key in ("cards", "scenarios", "pending"):
        items = value.get(key)
        if isinstance(items, list) and any(isinstance(item, dict) and str(item.get("status", "")).lower() in {"pending", "deferred"} for item in items):
            return True
    return False


def judge_checks(value):
    checks = value.get("checks") if isinstance(value, dict) else None
    return isinstance(checks, dict) and isinstance(checks.get("judge"), list) and bool(checks["judge"])


def migration_status(value):
    if not isinstance(value, dict):
        return None
    encoded = json.dumps(value)
    recognized = ("old_model" in value and "new_model" in value) or ("old-fixture" in encoded and "new-fixture" in encoded)
    if not recognized:
        return None
    missing = value.get("missing_cells")
    if value.get("complete") is False or (isinstance(missing, list) and missing):
        return "incomplete"
    if value.get("complete") is True or value.get("selected") or value.get("selection"):
        return "complete"
    return "incomplete"


def walk(root):
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP and not name.startswith("."))
        yield Path(current), files


def classify(root):
    root = root.resolve()
    manifest = root / "plugin.json"
    if manifest.is_file() and (root / "skills/expert-mode/SKILL.md").is_file() and (root / "fixtures/playground/evaluate.py").is_file():
        try:
            if json.loads(manifest.read_text(encoding="utf-8")).get("name") == "cstack" and not (root / ".cstack-source.json").is_file():
                return "cstack-checkout"
        except (OSError, UnicodeError, json.JSONDecodeError):
            pass
    playground = (root / "evaluate.py").is_file() and (root / "exercises/01-expert-mode.md").is_file() and (root / "support_agent.py").is_file()
    if playground and not (root / ".cstack-source.json").is_file():
        return "canonical-playground"
    if playground or (root / ".cstack-source.json").is_file():
        return "playground"
    return "project"


def blank():
    return {
        "specs": [], "user_cases": [], "receipts": [], "stale": [], "campaigns": [],
        "records": [], "replay_ready": 0, "bootstrap_pending": [], "ledgers": [],
        "open_ledgers": [], "judge_needed": [], "judge_done": [], "adversarial": [],
        "ablation": [], "migration_incomplete": [], "migration_complete": [],
        "loose_traces": [], "course": None, "user_work": False,
    }


def consider_receipt(root, directory, found):
    manifest_path = directory / "manifest.json"
    summary_path = directory / "summary.json"
    if not (manifest_path.is_file() and summary_path.is_file() and (directory / "traces.jsonl").is_file()):
        if (directory / "traces.jsonl").is_file() and not manifest_path.is_file():
            found["loose_traces"].append(rel(root, directory / "traces.jsonl"))
        return
    manifest = load_json(manifest_path)
    summary = load_json(summary_path)
    source = manifest.get("cases_source") if manifest else None
    if not manifest or not isinstance(source, dict) or not isinstance(source.get("sha256"), str) or not summary:
        return
    reasons = []
    cases_path = inside(root, source.get("path"))
    if cases_path is not None and digest(cases_path) != source["sha256"]:
        reasons.append("cases")
    files = manifest.get("identity", {}).get("files") if isinstance(manifest.get("identity"), dict) else None
    if isinstance(files, dict):
        for name, recorded in files.items():
            target = root / name
            if isinstance(recorded, str) and target.is_file() and digest(target) != recorded:
                reasons.append(name)
    path = rel(root, directory)
    receipt = {"path": path, "mtime": summary_path.stat().st_mtime, "reasons": reasons, "summary": summary}
    found["receipts"].append(receipt)
    if reasons:
        found["stale"].append(path)


def consider_campaign(root, directory, found):
    contract = load_json(directory / "contract.json")
    state = load_json(directory / "state.json")
    files = contract.get("identity", {}).get("files") if contract else None
    if not isinstance(files, dict) or not state:
        return
    mismatches = [name for name, recorded in files.items() if isinstance(recorded, str) and (root / name).is_file() and digest(root / name) != recorded]
    compared = [name for name in files if (root / name).is_file()]
    if mismatches:
        match = "incompatible"
    elif compared:
        match = "compatible"
    else:
        match = "unverifiable"
    attempts = state.get("attempts") if isinstance(state.get("attempts"), list) else []
    pending = any(isinstance(item, dict) and item.get("status") not in {None, "complete"} for item in attempts)
    active = state.get("status") == "active" or pending
    found["campaigns"].append({"path": rel(root, directory), "match": match, "active": active, "status": state.get("status")})


def consider_course(root, found):
    progress = root / "eval-runs/course/progress"
    state_path = progress / "state.json"
    events = sorted(progress.joinpath("events").glob("*.json")) if progress.joinpath("events").is_dir() else []
    if state_path.is_file():
        state = load_json(state_path) or {}
        found["course"] = {
            "path": rel(root, state_path),
            "revision": state.get("revision") or 0,
            "stage": state.get("stage"),
            "completed": state.get("completed") if isinstance(state.get("completed"), list) else [],
            "next_action": state.get("next_action") or "",
        }
    elif events:
        found["course"] = {"path": rel(root, events[-1]), "revision": len(events), "stage": "unknown", "completed": [], "next_action": "", "journal_only": True}


def scan(root):
    found = blank()
    kind = classify(root)
    if kind == "cstack-checkout":
        return kind, found
    for current, files in walk(root):
        names = set(files)
        if {"manifest.json", "summary.json", "traces.jsonl"} & names or "traces.jsonl" in names:
            consider_receipt(root, current, found)
        if "contract.json" in names and "state.json" in names:
            consider_campaign(root, current, found)
        if current.name in {"case-build"} and "eval-runs" in current.parts:
            found["adversarial"].append(rel(root, current))
        if current.name in {"ablation", "simplification"} and "eval-runs" in current.parts:
            if any((current / name).exists() for name in ("state.json", "results.json")) or any(current.glob("selected*")):
                found["ablation"].append(rel(root, current))
        judge_dir = any(part in {"judge-calibration", "judge_calibration"} for part in current.parts)
        if judge_dir and "results.json" in names:
            found["judge_done"].append(rel(root, current / "results.json"))
        elif judge_dir and ({"fitting.json", "state.json"} & names) and "results.json" not in names:
            found["judge_needed"].append(rel(root, current))
        for name in sorted(names):
            path = current / name
            lowered = name.lower()
            if name in {"spec.json", "rubric.md"} or name == "task.toml":
                found["specs"].append(rel(root, path))
            if "ledger" in lowered and name.endswith(".md"):
                found["ledgers"].append(rel(root, path))
                try:
                    text = path.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    text = ""
                if OPEN_LEDGER.search(text):
                    found["open_ledgers"].append(rel(root, path))
            if name.endswith(".jsonl"):
                rows = load_jsonl(path, limit=200)
                shipped = kind == "playground" and rel(root, path) == "evals/cases.jsonl"
                if any(is_record(row) for row in rows):
                    found["records"].append(rel(root, path))
                    found["replay_ready"] += sum(1 for row in rows if replay_ready(row))
                if not shipped and any(is_case(row) for row in rows):
                    found["user_cases"].append(rel(root, path))
            if not name.endswith(".json"):
                continue
            value = load_json(path)
            if value is None:
                continue
            relative = rel(root, path)
            under_runs = "eval-runs" in path.parts
            if (under_runs or "bootstrap" in lowered) and pending_cards(value):
                found["bootstrap_pending"].append(relative)
            if judge_checks(value):
                found["judge_needed"].append(relative)
            if name == "fitting.json" and not (path.parent / "results.json").is_file():
                found["judge_needed"].append(rel(root, path.parent))
            if name == "results.json" and (path.parent / "fitting.json").is_file():
                found["judge_done"].append(relative)
            if under_runs and "activation" in value and "outcome" in value:
                found["adversarial"].append(relative)
            status = migration_status(value) if under_runs else None
            if status == "incomplete":
                found["migration_incomplete"].append(relative)
            elif status == "complete":
                found["migration_complete"].append(relative)
    consider_course(root, found)
    found["user_work"] = any(found[key] for key in (
        "user_cases", "receipts", "campaigns", "records", "bootstrap_pending", "ledgers",
        "judge_needed", "judge_done", "adversarial", "ablation", "migration_incomplete", "migration_complete", "loose_traces"))
    if found["course"] and (found["course"].get("revision") or 0) > 0:
        found["user_work"] = True
    for key in ("specs", "user_cases", "records", "bootstrap_pending", "ledgers", "open_ledgers", "judge_needed", "judge_done", "adversarial", "ablation", "migration_incomplete", "loose_traces"):
        found[key] = sorted(set(found[key]))
    found["receipts"].sort(key=lambda item: (item["mtime"], item["path"]))
    return kind, found


def newest(found):
    return found["receipts"][-1] if found["receipts"] else None


def untrustworthy(receipt):
    if receipt is None:
        return False
    summary = receipt["summary"]
    counts = summary.get("counts") if isinstance(summary.get("counts"), dict) else {}
    unknown = counts.get("UNKNOWN") or 0
    return bool(receipt["reasons"]) or summary.get("complete") is False or unknown > 0


def failing(receipt):
    if receipt is None or untrustworthy(receipt):
        return False
    counts = receipt["summary"].get("counts") if isinstance(receipt["summary"].get("counts"), dict) else {}
    return (counts.get("FAIL") or 0) > 0 or (counts.get("ERROR") or 0) > 0


def passing(receipt):
    if receipt is None or untrustworthy(receipt) or failing(receipt):
        return False
    counts = receipt["summary"].get("counts") if isinstance(receipt["summary"].get("counts"), dict) else {}
    return (counts.get("PASS") or 0) > 0 or receipt["summary"].get("complete") is True


def course_open(found):
    course = found.get("course")
    if not course or not (course.get("revision") or 0):
        return False
    if course.get("journal_only") or course.get("stage") == "unknown":
        return True
    completed = course.get("completed") or []
    return not (course.get("stage") == "handoff" and len(completed) >= EXERCISES)


def recommendation(kind, found):
    def answer(skill, why, evidence):
        return {"skill": skill, "why": why, "evidence": [item for item in evidence if item]}

    if kind == "cstack-checkout":
        return answer("course", "This folder is the CStack pack. Its evals/ history is pack evidence, not your campaign. Materialize the playground and start the course.", ["fixtures/playground/exercises/01-expert-mode.md"])
    if kind == "canonical-playground":
        return answer("course", "This is the canonical playground fixture. Materialize a disposable workspace with scripts/new_workspace.py, then start the course there.", ["exercises/01-expert-mode.md"])

    active = [item for item in found["campaigns"] if item["active"] and item["match"] == "compatible"]
    if active:
        path = active[-1]["path"]
        return answer("hill-climb", f"A compatible campaign is still active at {path}. Resume it before starting another measurement. Pending attempts stay charged.", [path])
    unverified = [item for item in found["campaigns"] if item["active"] and item["match"] == "unverifiable"]
    if unverified:
        path = unverified[-1]["path"]
        return answer("hill-climb", f"The campaign at {path} is active, and its contract files are not in this workspace. Reconcile that identity before new trials.", [path])
    incompatible = [item for item in found["campaigns"] if item["match"] == "incompatible"]
    if incompatible:
        path = incompatible[-1]["path"]
        return answer("hill-climb", f"The campaign at {path} no longer matches the evaluator or cases. Preserve it and start a new campaign and baseline.", [path])

    current = newest(found)
    if untrustworthy(current):
        reason = "no longer matches the current cases or evaluator" if current["reasons"] else "is incomplete or still has unknown outcomes"
        return answer("run-eval", f"The newest receipt at {current['path']} {reason}. Re-execute before trusting that score.", [current["path"]])
    if found["open_ledgers"]:
        path = found["open_ledgers"][0]
        return answer("cross-examine", f"The ledger at {path} still has an open or unreviewed item. Finish that audit before a new optimization.", [path])
    if found["bootstrap_pending"]:
        path = found["bootstrap_pending"][0]
        return answer("bootstrap", f"Scenario review is unfinished at {path}. Keep pending cards out of authoring.", [path])
    if course_open(found):
        course = found["course"]
        stage = course.get("stage") or "the saved exercise"
        action = course.get("next_action") or "Resume from the saved checkpoint."
        return answer("course", f"Course progress is at {stage}. {action}", [course.get("path")])
    if kind == "playground" and not found["user_work"]:
        return answer("course", "This playground has the shipped fixture and no saved exercise work. The course walks exercises 01–13.", ["exercises/01-expert-mode.md"])
    if found["records"] and found["replay_ready"] == 0 and not found["user_cases"] and not found["receipts"]:
        return answer("expert-mode", f"Review records at {found['records'][0]} have no row that ties an explicit judgment to an input, an output, and a criterion.", [found["records"][0]])
    if found["replay_ready"] and not found["user_cases"]:
        noun = "judgment" if found["replay_ready"] == 1 else "judgments"
        return answer("create-eval", f"{found['replay_ready']} replay-ready {noun} have no cases yet. Author from those rows; an expectation approval is not an output label.", [found["records"][0]])
    if found["user_cases"] and not found["receipts"]:
        return answer("run-eval", f"Cases exist at {found['user_cases'][0]} and have no execution receipt.", [found["user_cases"][0]])
    if found["judge_needed"] and not found["judge_done"]:
        return answer("calibrate-judge", "A semantic judge is configured and no calibration result is saved. Do not fit the product to that judge yet.", [found["judge_needed"][0]])
    if found["loose_traces"] and not found["records"] and not found["receipts"]:
        return answer("expert-mode", f"Traces at {found['loose_traces'][0]} have no saved expert judgment.", [found["loose_traces"][0]])
    if failing(current) and not any(item["active"] for item in found["campaigns"]):
        counts = current["summary"].get("counts") if isinstance(current["summary"].get("counts"), dict) else {}
        return answer("hill-climb", f"The newest receipt at {current['path']} has {counts.get('FAIL') or 0} failure(s) and {counts.get('ERROR') or 0} error(s), and no campaign is active.", [current["path"]])
    if passing(current) and not found["ledgers"]:
        return answer("cross-examine", f"The newest receipt at {current['path']} passes, and the verifier has no challenge ledger. A pass does not show that the score checks the intended outcome.", [current["path"]])
    if passing(current) and not found["adversarial"]:
        return answer("adversarial-cases", f"Measured passes at {current['path']} have no constructed challenge set yet.", [current["path"]])
    if found["migration_incomplete"]:
        return answer("bitter-lesson", f"A model-migration comparison at {found['migration_incomplete'][0]} is unfinished. Missing cells stay missing.", [found["migration_incomplete"][0]])
    if passing(current) and not found["ablation"]:
        return answer("ablation", f"The newest receipt at {current['path']} passes, and removal has not been tested against that bar.", [current["path"]])
    if kind == "project" and not found["user_work"] and not found["receipts"]:
        if found["specs"]:
            why = f"A spec is present at {found['specs'][0]}, and there are no cases, receipts, or review records yet. Interview for the behavior before authoring."
            evidence = [found["specs"][0]]
        else:
            why = "No eval spec, cases, receipts, or review records are in this workspace. Interview for the behavior."
            evidence = []
        return answer("bootstrap", why, evidence)
    evidence = []
    if current:
        evidence.append(current["path"])
    if found["ledgers"]:
        evidence.append(found["ledgers"][0])
    return answer("expert-mode", "The recorded loop is present. Capture a judgment on the next change you actually review.", evidence)


def inspect(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Workspace does not exist: {root}")
    kind, found = scan(root)
    current = newest(found)
    public_receipts = [{"path": item["path"], "stale": bool(item["reasons"]), "reasons": item["reasons"], "counts": item["summary"].get("counts"), "complete": item["summary"].get("complete")} for item in found["receipts"]]
    return {
        "root": str(root),
        "workspace_kind": kind,
        "specs": found["specs"],
        "user_cases": found["user_cases"],
        "receipts": public_receipts,
        "newest_receipt": None if current is None else public_receipts[-1],
        "stale": found["stale"],
        "campaigns": found["campaigns"],
        "records": found["records"],
        "replay_ready": found["replay_ready"],
        "bootstrap_pending": found["bootstrap_pending"],
        "ledgers": found["ledgers"],
        "open_ledgers": found["open_ledgers"],
        "judge_needed": found["judge_needed"],
        "judge_done": found["judge_done"],
        "adversarial": found["adversarial"],
        "ablation": found["ablation"],
        "migration_incomplete": found["migration_incomplete"],
        "loose_traces": found["loose_traces"],
        "course": found["course"],
        "user_work": found["user_work"],
        "recommendation": recommendation(kind, found),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(json.dumps(inspect(args.root), indent=2))


if __name__ == "__main__":
    main()
