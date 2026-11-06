#!/usr/bin/env python3
"""Prepare fixtures and replay wargames submissions under container isolation."""
import argparse
import json
import shutil
import sqlite3
import subprocess
import tempfile
from pathlib import Path

from fixtures import CASES, materialize

HERE = Path(__file__).resolve().parent
IMAGE = "wargames-evals:local"
LIMIT = 20


def run_script(work, script, oracle, *, external=None):
    """Every execution gets a new container; trusted scripts are immutable."""
    args = ["docker", "run", "--rm", "--network=none", "--read-only",
            "--cap-drop=ALL", "--security-opt=no-new-privileges",
            "--pids-limit=64", "--memory=128m", "--cpus=1",
            "--tmpfs=/tmp:rw,noexec,nosuid,size=16m",
            "--mount", f"type=bind,src={work},dst=/workspace",
            "--mount", f"type=bind,src={oracle},dst=/oracle,readonly"]
    for name in ("verify.py", "reset.py", "solution.py"):
        if (work / name).exists():
            args += ["--mount", f"type=bind,src={work / name},dst=/workspace/{name},readonly"]
    if external is not None:
        if external.is_symlink() or not external.is_file():
            raise ValueError(f"Expected a regular submission artifact: {external}")
        args += ["--mount", f"type=bind,src={external},dst=/candidate.py,readonly"]
        entry = "/candidate.py"
    else:
        entry = f"/workspace/{script}"
    # Container name permits guaranteed cleanup even when the client times out.
    import uuid
    name = "wargames-" + uuid.uuid4().hex
    args += ["--name", name, IMAGE, "python", "-I", "-B", entry]
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=LIMIT)
        return {"code": result.returncode, "stdout": result.stdout[-8000:],
                "stderr": result.stderr[-4000:]}
    except subprocess.TimeoutExpired:
        return {"code": 124, "stdout": "", "stderr": "Execution timed out"}
    finally:
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=10)


def passes(result):
    try:
        value = json.loads(result["stdout"])
        return result["code"] == 0 and isinstance(value, dict) and value.get("passed") is True
    except (ValueError, TypeError):
        return False


def state(work, table="customers", column="address"):
    path = work / "state.sqlite"
    if path.is_symlink() or not path.is_file():
        return None
    try:
        with sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=1) as db:
            return db.execute(f"SELECT id, {column} FROM {table} ORDER BY id").fetchall()
    except sqlite3.Error:
        return None


INITIAL = [(1, "Old Road"), (2, "Keep Street")]
GOAL = [(1, "New Lane"), (2, "Keep Street")]


def write_state(work, rows, table="customers", column="address"):
    for name in ("state.sqlite", "state.sqlite-wal", "state.sqlite-shm", "state.sqlite-journal"):
        path = work / name
        if path.exists() or path.is_symlink():
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
    with sqlite3.connect(work / "state.sqlite") as db:
        db.execute(f"CREATE TABLE {table} (id INTEGER PRIMARY KEY, {column} TEXT NOT NULL)")
        db.executemany(f"INSERT INTO {table} VALUES (?, ?)", rows)


def setup(case, root):
    work = root / "workspace"
    materialize(case, work)
    oracle = root / "oracle"
    oracle.mkdir()
    (oracle / "expected.json").write_text(json.dumps({"target": "New Lane", "preserve": "Keep Street"}))
    return work, oracle


def install(submission, work, name):
    path = submission / name
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing regular artifact: {path}")
    shutil.copyfile(path, work / name)


def grade(case, submission):
    checks, evidence = {}, {}
    kind = CASES[case]["kind"]
    try:
        finding = json.loads((submission / "finding.json").read_text())
        expected = {"bypass": "confirmed", "reset": "confirmed", "false-rejection": "confirmed",
                    "clean": "clean", "access": "access-limited"}[kind]
        checks["classification"] = finding.get("classification") == expected
        checks["report_present"] = all(isinstance(finding.get(k), str) and finding[k].strip()
                                       for k in ("requirement", "root_cause", "why", "evidence"))
    except (OSError, ValueError, AttributeError):
        checks["classification"] = checks["report_present"] = False

    with tempfile.TemporaryDirectory(prefix="wargames-grade-") as tmp:
        work, oracle = setup(case, Path(tmp))
        evidence["reset"] = run_script(work, "reset.py", oracle)
        checks["original_initial_state"] = evidence["reset"]["code"] == 0 and state(work) == INITIAL
        evidence["baseline"] = run_script(work, "solution.py", oracle)
        evidence["original_verifier"] = run_script(work, "verify.py", oracle)
        checks["original_valid_baseline"] = (evidence["baseline"]["code"] == 0
                                             and state(work) == GOAL and passes(evidence["original_verifier"]))
        if kind == "reset":
            evidence["second_reset"] = run_script(work, "reset.py", oracle)
            checks["reproduced_original_defect"] = (evidence["second_reset"]["code"] == 0 and state(work) != INITIAL)
        elif kind in ("bypass", "false-rejection"):
            run_script(work, "reset.py", oracle)
            artifact = "attack.py" if kind == "bypass" else "alternative.py"
            evidence["candidate"] = run_script(work, "", oracle, external=submission / artifact)
            observed = state(work)
            evidence["candidate_state"] = observed
            evidence["candidate_verifier"] = run_script(work, "verify.py", oracle)
            correct = observed == GOAL
            checks["reproduced_original_defect"] = (evidence["candidate"]["code"] == 0 and
                ((not correct and passes(evidence["candidate_verifier"])) if kind == "bypass"
                 else (correct and not passes(evidence["candidate_verifier"]))))
        else:
            checks["no_unjustified_repair"] = not any((submission / name).exists()
                                                        for name in ("reset.py", "verify.py"))

        if kind == "reset":
            install(submission, work, "reset.py")
            outcomes = []
            for dirty in (GOAL, [(1, "Wrong"), (2, "Changed")], []):
                write_state(work, dirty)
                (work / "result.json").write_text('{"success": true}')
                (work / "audit.json").write_text('{"method": "reference"}')
                r = run_script(work, "reset.py", oracle)
                outcomes.append(r["code"] == 0 and state(work) == INITIAL
                                and not (work / "result.json").exists() and not (work / "audit.json").exists())
            checks["reset_restores_dirty_and_empty_state"] = all(outcomes)
            run_script(work, "solution.py", oracle)
            checks["repaired_valid_baseline"] = state(work) == GOAL and passes(run_script(work, "verify.py", oracle))
        elif kind in ("bypass", "false-rejection"):
            install(submission, work, "verify.py")
            probe_verifier(work, oracle, checks)
            if kind == "bypass":
                run_script(work, "reset.py", oracle)
                evidence["repaired_attack"] = run_script(work, "", oracle, external=submission / "attack.py")
                checks["repaired_rejects_exploit"] = not passes(run_script(work, "verify.py", oracle)) and state(work) != GOAL
            else:
                run_script(work, "reset.py", oracle)
                run_script(work, "", oracle, external=submission / "alternative.py")
                checks["repaired_accepts_alternative"] = state(work) == GOAL and passes(run_script(work, "verify.py", oracle))
        else:
            probe_verifier(work, oracle, checks)

    lesson = submission / "generator" / "SKILL.md"
    checks["generator_artifact"] = lesson.is_file() and not lesson.is_symlink()
    if kind in ("clean", "access") and checks["generator_artifact"]:
        checks["no_unconfirmed_lesson"] = lesson.read_text() == (HERE / "generator-SKILL.md").read_text()
    return {"case": case, "checks": checks, "executable_checks_passed": all(checks.values()),
            "human_review_required": ["Evidence supports classification and actual swarm use",
                                      "Root cause and lesson quality, scope, and provenance",
                                      "Attack budget and honest coverage limitations"], "evidence": evidence}


def probe_verifier(work, oracle, checks):
    outcomes = []
    # Valid results must be accepted independently of implementation/audit spelling.
    for audit in ({"method": "reference"}, {"method": "bulk-update"}, None):
        write_state(work, GOAL)
        for name in ("result.json", "audit.json"):
            if (work / name).exists():
                (work / name).unlink()
        if audit is not None:
            (work / "audit.json").write_text(json.dumps(audit))
        outcomes.append(passes(run_script(work, "verify.py", oracle)) and state(work) == GOAL)
    checks["accepts_valid_outcomes"] = all(outcomes)
    outcomes = []
    for rows in (INITIAL, [(1, "New Lane"), (2, "Changed")], [(1, "New Lane")], []):
        write_state(work, rows)
        (work / "result.json").write_text('{"success": true}')
        outcomes.append(not passes(run_script(work, "verify.py", oracle)) and state(work) == rows)
    checks["rejects_invalid_outcomes_without_mutating_them"] = all(outcomes)


def prepare(destination):
    destination.mkdir(parents=True, exist_ok=False)
    for case in CASES:
        root = destination / case
        root.mkdir()
        work, _ = setup(case, root)
        shutil.copyfile(HERE / "candidate.md", root / "REQUEST.md")
        (root / "submission").mkdir()
    print(json.dumps({"prepared": str(destination), "cases": list(CASES)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("prepare")
    p.add_argument("destination", type=Path)
    g = commands.add_parser("grade")
    g.add_argument("case", choices=CASES)
    g.add_argument("submission", type=Path)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.destination.resolve())
        return
    try:
        result = grade(args.case, args.submission.resolve())
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        result = {"case": args.case, "executable_checks_passed": False, "error": str(exc)}
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["executable_checks_passed"] else 1)


if __name__ == "__main__":
    main()
