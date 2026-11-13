#!/usr/bin/env python3
"""Append-only progress for the CStack course. The tutor runs this; the learner decides."""

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path


EXERCISES = [
    "01-expert-mode",
    "02-distill-me",
    "03-bootstrap",
    "04-create-eval",
    "05-run-eval",
    "06-cross-examine",
    "07-hill-climb",
    "08-adversarial-cases",
    "09-methods-and-dspy",
    "10-calibrate-judge",
    "11-ablation",
    "12-bitter-lesson",
    "13-review-calibration-capture",
]
STAGES = ["orient", *EXERCISES, "handoff"]
ASSISTANCE = {"independent", "hinted", "worked"}


def progress_dir(workspace):
    return workspace / "eval-runs" / "course" / "progress"


def events_dir(workspace):
    return progress_dir(workspace) / "events"


def sha(path):
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary_path, path)


def empty_state():
    return {
        "version": 1,
        "revision": 0,
        "stage": "orient",
        "completed": [],
        "decisions": {},
        "artifacts": {},
        "unresolved": [],
        "next_action": "Show exercise 01's trace and ask what should have happened.",
        "last_learner_response": "",
        "last_observation": "",
        "assistance": None,
    }


def materialized(workspace):
    return (workspace / ".cstack-source.json").is_file()


def require_workspace(workspace):
    workspace = workspace.resolve()
    if not workspace.is_dir():
        raise SystemExit(f"Workspace does not exist: {workspace}")
    if (workspace / "exercises/01-expert-mode.md").is_file() and not materialized(workspace):
        raise SystemExit("This is the canonical playground fixture. Materialize a workspace with scripts/new_workspace.py. Course progress is not written here.")
    return workspace


def problems(workspace):
    found = []
    if sys.version_info < (3, 11):
        found.append(f"Python {sys.version.split()[0]} is older than the playground's 3.11+")
    for relative in ("evaluate.py", "support_agent.py", "exercises/01-expert-mode.md", "evals/spec.json", "evals/cases.jsonl"):
        if not (workspace / relative).is_file():
            found.append("missing " + relative)
    if not materialized(workspace):
        found.append("not a materialized workspace (.cstack-source.json missing)")
    return found


def journal(workspace):
    current = empty_state()
    paths = sorted(events_dir(workspace).glob("*.json")) if events_dir(workspace).is_dir() else []
    for index, path in enumerate(paths, 1):
        event = read_json(path)
        state = event.get("state")
        if not isinstance(state, dict) or state.get("revision") != index or path.stem != f"{index:06d}":
            raise SystemExit("Progress journal is inconsistent. Preserve it and follow references/recovery.md. Do not delete events.")
        current = state
    cache = progress_dir(workspace) / "state.json"
    if paths:
        save_json(cache, current)
    elif cache.exists():
        raise SystemExit("Progress cache exists without its journal. Preserve both and follow references/recovery.md.")
    return current


def notes(workspace):
    found = []
    for relative in ("eval-runs/course/checkpoint-draft.json", "eval-runs/course/progress/manual-notes.md"):
        if (workspace / relative).exists():
            found.append(relative)
    return found


def changed(workspace, state):
    found = []
    artifacts = state.get("artifacts") if isinstance(state.get("artifacts"), dict) else {}
    for relative, recorded in sorted(artifacts.items()):
        path = workspace / relative
        if not path.is_file() or path.is_symlink():
            found.append({"path": relative, "status": "missing"})
        elif sha(path) != recorded:
            found.append({"path": relative, "status": "changed"})
    return found


def status(workspace):
    workspace = require_workspace(workspace)
    state = journal(workspace)
    return {
        "workspace": str(workspace),
        "doctor": problems(workspace),
        "revision": state["revision"],
        "stage": state["stage"],
        "completed": state["completed"],
        "next_action": state["next_action"],
        "last_learner_response": state.get("last_learner_response") or "",
        "last_observation": state.get("last_observation") or "",
        "assistance": state.get("assistance"),
        "unresolved": state.get("unresolved") or [],
        "decisions": state.get("decisions") or {},
        "changed_or_missing": changed(workspace, state),
        "notes_to_reconcile": notes(workspace),
    }


def contained(workspace, relative):
    if not isinstance(relative, str) or not relative or relative.startswith("/") or ".." in Path(relative).parts:
        raise SystemExit(f"Artifact path must stay inside the workspace: {relative}")
    path = (workspace / relative).resolve()
    root = workspace.resolve()
    if path != root and root not in path.parents:
        raise SystemExit(f"Artifact path must stay inside the workspace: {relative}")
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f"Artifact is missing or linked: {relative}")
    return path


def valid_progress(completed, stage):
    if completed != EXERCISES[:len(completed)]:
        return False
    if stage == "orient":
        return not completed
    if stage == "handoff":
        return completed == EXERCISES
    if stage not in EXERCISES:
        return False
    return len(completed) <= EXERCISES.index(stage) + 1


def checkpoint(workspace, record_path, expected):
    workspace = require_workspace(workspace)
    if problems(workspace):
        raise SystemExit("Doctor failed: " + "; ".join(problems(workspace)))
    before = journal(workspace)
    if expected != before["revision"]:
        raise SystemExit(f"Progress changed (current revision {before['revision']}). Run status and reconcile. Do not overwrite.")
    record_file = Path(record_path)
    if not record_file.is_absolute():
        record_file = workspace / record_file
    record = read_json(record_file)
    stage = record.get("stage")
    if stage not in STAGES or not isinstance(record.get("next_action"), str) or not record["next_action"].strip():
        raise SystemExit("Checkpoint needs a known stage and an exact next_action")
    if not isinstance(record.get("learner_response"), str) or not isinstance(record.get("observation"), str):
        raise SystemExit("Checkpoint needs learner_response (empty only for a tool-only event) and observation")
    if not isinstance(record.get("unresolved"), list) or not all(isinstance(item, str) for item in record["unresolved"]):
        raise SystemExit("unresolved must be a list of strings")
    completed = record.get("completed", before["completed"])
    if not isinstance(completed, list) or not valid_progress(completed, stage):
        raise SystemExit("completed must be the exercise prefix for this stage, and handoff requires all 13")
    if completed[:len(before["completed"])] != before["completed"]:
        raise SystemExit("Completed work cannot be removed")
    assistance = record.get("assistance", before.get("assistance"))
    if assistance is not None and assistance not in ASSISTANCE:
        raise SystemExit("assistance must be independent, hinted, or worked")
    decisions = dict(before.get("decisions") or {})
    if "decisions" in record:
        if not isinstance(record["decisions"], dict):
            raise SystemExit("decisions must be an object")
        decisions.update(record["decisions"])
    artifacts = dict(before.get("artifacts") or {})
    for relative in record.get("artifacts") or []:
        artifacts[relative] = sha(contained(workspace, relative))
    after = dict(before)
    after.update(stage=stage, completed=completed, decisions=decisions, artifacts=artifacts,
                 unresolved=list(record["unresolved"]), next_action=record["next_action"].strip(),
                 last_learner_response=record["learner_response"], last_observation=record["observation"],
                 assistance=assistance, revision=expected + 1,
                 updated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    event = {"learner_response": record["learner_response"], "observation": record["observation"], "assistance": assistance, "state": after}
    directory = events_dir(workspace)
    directory.mkdir(parents=True, exist_ok=True)
    event_path = directory / f"{after['revision']:06d}.json"
    descriptor, pending = tempfile.mkstemp(prefix="checkpoint-", suffix=".tmp", dir=directory)
    pending_path = Path(pending)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(event, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(pending_path, event_path)
        except FileExistsError:
            raise SystemExit("That revision already exists. Run status and reconcile. Do not overwrite.")
    finally:
        pending_path.unlink(missing_ok=True)
    save_json(progress_dir(workspace) / "state.json", after)
    return after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    commands.add_parser("status")
    save = commands.add_parser("checkpoint")
    save.add_argument("--record", type=Path, required=True)
    save.add_argument("--expected", type=int, required=True)
    args = parser.parse_args()
    if args.command == "doctor":
        workspace = require_workspace(args.workspace)
        found = problems(workspace)
        print(json.dumps({"workspace": str(workspace), "problems": found}, indent=2))
        raise SystemExit(1 if found else 0)
    if args.command == "status":
        print(json.dumps(status(args.workspace), indent=2))
        return
    saved = checkpoint(args.workspace, args.record, args.expected)
    print(json.dumps({"revision": saved["revision"], "stage": saved["stage"], "completed": saved["completed"], "next_action": saved["next_action"]}, indent=2))


if __name__ == "__main__":
    main()
