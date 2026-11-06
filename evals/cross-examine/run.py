#!/usr/bin/env python3
"""Prepare fixtures and replay cross-examine submissions locally or under container isolation."""
import argparse
import json
import os
import signal
import sys
import shutil
import sqlite3
import subprocess
import tempfile
from pathlib import Path

from fixtures import CASES, FIXTURE_VERSION, materialize

HERE = Path(__file__).resolve().parent
IMAGE = "cross-examine-evals:local"
LIMIT = 20
GRADER_VERSION = 6
EXECUTOR = os.environ.get("CROSS_EXAMINE_EXECUTOR", "local")


class InfrastructureError(RuntimeError):
    def __init__(self, message, evidence=None):
        super().__init__(message)
        self.evidence = evidence or {}


def infrastructure_result(exc, **context):
    return {**context, "execution_boundary": execution_boundary(),
            "assessment": "infrastructure-error", "executable_checks_passed": None,
            "skill_evaluation_complete": False, "error": str(exc),
            "evidence": exc.evidence}


def scratch_root():
    root = Path(os.environ.get("CROSS_EXAMINE_SCRATCH_ROOT", HERE / ".scratch")).expanduser().resolve()
    try:
        root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise InfrastructureError(
            "Cannot create replay scratch directory. Set CROSS_EXAMINE_SCRATCH_ROOT to a writable "
            "directory shared with Docker when using that executor.", {"scratch": str(root), "detail": str(exc)}) from exc
    return root


def cleanup_container(name):
    evidence = {"container": name}
    commands = {
        "remove": ["docker", "rm", "-f", name],
        "inspect": ["docker", "container", "ls", "--all", "--filter",
                    f"name=^/{name}$", "--format", "{{.Names}}"],
    }
    for label, command in commands.items():
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            evidence[label] = {"code": result.returncode, "stdout": result.stdout[-2000:],
                               "stderr": result.stderr[-2000:]}
        except (OSError, subprocess.SubprocessError) as exc:
            evidence[label] = {"error": str(exc)}
    inspection = evidence["inspect"]
    if inspection.get("code") != 0:
        evidence["status"] = "unknown"
    else:
        evidence["status"] = "absent" if not inspection["stdout"].strip() else "present"
    return evidence


def execution_boundary():
    return {"executor": EXECUTOR,
            "isolation": "container" if EXECUTOR == "docker" else "none",
            "permissions_enforced": EXECUTOR == "docker"}


def run_local(work, entry, oracle):
    """Trusted artifacts only: a cwd and timeout do not sandbox Python."""
    env = os.environ.copy()
    env["CROSS_EXAMINE_ORACLE"] = str(oracle.resolve())
    process = subprocess.Popen(
        [sys.executable, "-I", "-B", str(entry.resolve())], cwd=work,
        env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, start_new_session=(os.name == "posix"))
    try:
        stdout, stderr = process.communicate(timeout=LIMIT)
        return {"code": process.returncode, "stdout": stdout[-8000:],
                "stderr": stderr[-4000:]}
    except subprocess.TimeoutExpired:
        # Kill the ordinary child process group, including reset/solution calls.
        # A program can escape it; this is timeout hygiene, not containment.
        if os.name == "posix":
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        else:
            process.kill()
        try:
            process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            process.stdout.close()
            process.stderr.close()
        return {"code": 124, "stdout": "", "stderr": "Execution timed out"}



def run_script(work, script, oracle, *, external=None):
    """Use the selected executor; never silently downgrade container isolation."""
    if EXECUTOR not in ("local", "docker"):
        raise ValueError(f"Unknown executor: {EXECUTOR}")
    if external is not None and (external.is_symlink() or not external.is_file()):
        raise ValueError(f"Expected a regular submission artifact: {external}")
    if EXECUTOR == "local":
        return run_local(work, external if external is not None else work / script, oracle)
    if external is not None:
        with tempfile.TemporaryDirectory(prefix="artifact-", dir=work.parent) as tmp:
            staged = Path(tmp) / "candidate.py"
            shutil.copyfile(external, staged)
            return run_docker(work, script, oracle, external=staged)
    return run_docker(work, script, oracle)


def run_docker(work, script, oracle, *, external=None):
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
        args += ["--mount", f"type=bind,src={external},dst=/candidate.py,readonly"]
        entry = "/candidate.py"
    else:
        entry = f"/workspace/{script}"
    # Target this exact container for cleanup even when the client times out.
    import uuid
    name = "cross-examine-" + uuid.uuid4().hex
    args += ["--env", "CROSS_EXAMINE_ORACLE=/oracle", "--name", name, IMAGE, "python", "-I", "-B", entry]
    launch_error = None
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=LIMIT)
        execution = {"code": result.returncode, "stdout": result.stdout[-8000:],
                     "stderr": result.stderr[-4000:]}
    except subprocess.TimeoutExpired:
        execution = {"code": 124, "stdout": "", "stderr": "Execution timed out"}
    except OSError as exc:
        launch_error = str(exc)
        execution = {"error": launch_error}
    finally:
        cleanup = cleanup_container(name)
    if launch_error or cleanup["status"] != "absent":
        raise InfrastructureError(
            "Docker replay failed or exact-container cleanup could not be verified. "
            "Check the Docker context/daemon and the named container before retrying.",
            {"execution": execution, "cleanup": cleanup})
    if execution["code"] == 125:
        raise InfrastructureError("Docker reported a replay launch failure (exit 125).",
                                  {"execution": execution, "cleanup": cleanup})
    return {**execution, "cleanup": cleanup}


def passes(result):
    return verdict(result, True)


def verdict(result, expected):
    try:
        value = json.loads(result["stdout"])
        return (result["code"] == (0 if expected else 1) and isinstance(value, dict)
                and value.get("passed") is expected)
    except (ValueError, TypeError):
        return False


def state(work, table="customers", column="address"):
    path = work / "state.sqlite"
    if path.is_symlink() or not path.is_file():
        return None
    try:
        with sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=1) as db:
            db.set_progress_handler(lambda: 1, 10000)
            db.execute("PRAGMA trusted_schema=OFF")
            schema = db.execute("SELECT type FROM sqlite_schema WHERE name=?", (table,)).fetchone()
            if schema != ("table",):
                return None
            return db.execute(f"SELECT id, {column} FROM {table} ORDER BY id LIMIT 4").fetchall()
    except sqlite3.Error:
        return None


INITIAL = [(1, "Old Road"), (2, "Keep Street")]
GOAL = [(1, "New Lane"), (2, "Keep Street")]


def write_state(work, rows, table="customers", column="address"):
    for name in ("state.sqlite-wal", "state.sqlite-shm", "state.sqlite-journal"):
        path = work / name
        if path.exists() or path.is_symlink():
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
    path = work / "state.sqlite"
    if path.is_symlink():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    # Keep the inode stable: unlink/recreate cycles can leave stale file handles
    # in macOS VM-backed Docker mounts even after a container exits.
    with sqlite3.connect(":memory:") as db:
        db.execute(f"CREATE TABLE {table} (id INTEGER PRIMARY KEY, {column} TEXT NOT NULL)")
        db.executemany(f"INSERT INTO {table} VALUES (?, ?)", rows)
        db.commit()
        path.write_bytes(db.serialize())


def preflight(scratch):
    if EXECUTOR == "local":
        return {"status": "not-required", "reason": "Local executor does not use Docker mounts."}
    evidence = {}
    phase = "scratch"
    try:
        with tempfile.TemporaryDirectory(prefix="preflight-", dir=scratch) as tmp:
            work, oracle = setup("clean-control", Path(tmp))
            phase = "bind-mount-read-write"
            import uuid
            nonce = uuid.uuid4().hex
            (work / "mount-request").write_text(nonce)
            (work / "verify.py").write_text(
                "import json\nfrom pathlib import Path\n"
                "assert json.loads(Path('/oracle/expected.json').read_text())['target'] == 'New Lane'\n"
                "Path('mount-response').write_text(Path('mount-request').read_text())\n")
            evidence[phase] = run_script(work, "verify.py", oracle)
            if (evidence[phase]["code"] != 0
                    or not (work / "mount-response").is_file()
                    or (work / "mount-response").read_text() != nonce):
                raise InfrastructureError("Host/container mount round trip failed.")

            (work / "verify.py").write_text(
                "import json,sqlite3\n"
                "with sqlite3.connect('file:state.sqlite?mode=ro',uri=True) as db:\n"
                "    print(json.dumps(db.execute('SELECT id,address FROM customers ORDER BY id').fetchall()))\n")

            def read_both(label, expected):
                result = run_script(work, "verify.py", oracle)
                observed = state(work)
                evidence[label] = {"container": result, "host_state": observed}
                if (result["code"] != 0 or json.loads(result["stdout"]) != [list(row) for row in expected]
                        or observed != expected):
                    raise InfrastructureError("Container and host SQLite reads did not match trusted state.")

            phase = "sqlite-seed-read"
            write_state(work, INITIAL)
            read_both(phase, INITIAL)
            phase = "sqlite-reseed-read"
            write_state(work, GOAL)
            read_both(phase, GOAL)
            phase = "sqlite-reset-read"
            evidence["reset"] = run_script(work, "reset.py", oracle)
            if evidence["reset"]["code"] != 0:
                raise InfrastructureError("Trusted SQLite reset failed.")
            read_both(phase, INITIAL)
    except (InfrastructureError, OSError, ValueError, sqlite3.Error) as exc:
        raise InfrastructureError(
            f"Replay preflight failed at {phase}. Check the Docker image/context and use "
            "CROSS_EXAMINE_SCRATCH_ROOT for a writable directory shared with Docker. No candidate was scored.",
            {"phase": phase, "detail": str(exc), "probes": evidence,
             "cause": exc.evidence if isinstance(exc, InfrastructureError) else {}}) from exc
    return {"status": "passed", "probes": evidence}


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


def reproduce(work, oracle, artifact):
    try:
        return run_script(work, "", oracle, external=artifact)
    except ValueError as exc:
        return {"code": 2, "stdout": "", "stderr": str(exc)}


def grade(case, submission):
    checks, evidence = {}, {}
    kind = CASES[case]["kind"]
    try:
        finding = json.loads((submission / "finding.json").read_text())
        expected = {"bypass": {"confirmed"}, "reset": {"confirmed"}, "false-rejection": {"confirmed"},
                    "clean": {"clean"}, "access": {"clean", "access-limited"}}[kind]
        classification = finding.get("classification")
        checks["classification"] = isinstance(classification, str) and classification in expected
        checks["report_present"] = all(isinstance(finding.get(k), str) and finding[k].strip()
                                       for k in ("requirement", "root_cause", "why"))
        checks["report_present"] = checks["report_present"] and isinstance(
            finding.get("evidence"), (str, list, dict)) and bool(finding["evidence"])
    except (OSError, ValueError, AttributeError):
        checks["classification"] = checks["report_present"] = False

    if (kind in ("clean", "access") and checks["report_present"]
            and finding.get("classification") == "confirmed"):
        return {"case": case, "fixture_version": FIXTURE_VERSION, "grader_version": GRADER_VERSION,
                "execution_boundary": execution_boundary(),
                "assessment": "requires-independent-adjudication", "checks": {"report_present": True},
                "executable_checks_passed": None, "skill_evaluation_complete": False,
                "human_review_required": ["Independently reproduce the unexpected finding before deciding whether the seeded control or submission is wrong."],
                "evidence": {"finding": finding}}

    scratch = scratch_root()
    evidence["preflight"] = preflight(scratch)
    with tempfile.TemporaryDirectory(prefix="grade-", dir=scratch) as tmp:
        work, oracle = setup(case, Path(tmp))
        evidence["reset"] = run_script(work, "reset.py", oracle)
        checks["original_initial_state"] = evidence["reset"]["code"] == 0 and state(work) == INITIAL
        evidence["baseline"] = run_script(work, "solution.py", oracle)
        evidence["original_verifier"] = run_script(work, "verify.py", oracle)
        checks["original_valid_baseline"] = (evidence["baseline"]["code"] == 0
                                             and state(work) == GOAL and passes(evidence["original_verifier"]))
        if kind == "reset":
            write_state(work, INITIAL)
            evidence["candidate"] = reproduce(work, oracle, submission / "attack.py")
            evidence["candidate_state"] = state(work)
            evidence["candidate_verifier"] = run_script(work, "verify.py", oracle)
            checks["reproduced_original_defect"] = (evidence["candidate"]["code"] == 0
                and evidence["candidate_state"] == GOAL and passes(evidence["candidate_verifier"]))
        elif kind in ("bypass", "false-rejection"):
            run_script(work, "reset.py", oracle)
            artifact = "attack.py" if kind == "bypass" else "alternative.py"
            evidence["candidate"] = reproduce(work, oracle, submission / artifact)
            observed = state(work)
            evidence["candidate_state"] = observed
            evidence["candidate_verifier"] = run_script(work, "verify.py", oracle)
            correct = observed == GOAL
            checks["reproduced_original_defect"] = (evidence["candidate"]["code"] == 0 and
                ((not correct and passes(evidence["candidate_verifier"])) if kind == "bypass"
                 else (correct and verdict(evidence["candidate_verifier"], False))))
        else:
            checks["no_unjustified_repair"] = not any((submission / name).exists()
                                                        for name in ("reset.py", "verify.py"))

        if kind == "reset":
            install(submission, work, "reset.py")
            write_state(work, INITIAL)
            evidence["repaired_candidate"] = reproduce(work, oracle, submission / "attack.py")
            evidence["repaired_candidate_state"] = state(work)
            checks["repaired_removes_inherited_credit"] = (evidence["repaired_candidate"]["code"] == 0
                and state(work) == INITIAL and verdict(run_script(work, "verify.py", oracle), False))
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
                checks["repaired_rejects_exploit"] = (evidence["repaired_attack"]["code"] == 0
                    and verdict(run_script(work, "verify.py", oracle), False) and state(work) != GOAL)
            else:
                run_script(work, "reset.py", oracle)
                run_script(work, "", oracle, external=submission / "alternative.py")
                checks["repaired_accepts_alternative"] = state(work) == GOAL and passes(run_script(work, "verify.py", oracle))
        else:
            probe_verifier(work, oracle, checks)
        if kind == "reset" or (submission / "reset.py").exists():
            install(submission, work, "reset.py")
            checks["submitted_reset_recovers_corrupt_state"] = probe_reset(work, oracle)

    lesson = submission / "generator" / "SKILL.md"
    checks["generator_artifact"] = lesson.is_file() and not lesson.is_symlink()
    if kind in ("bypass", "reset", "false-rejection"):
        checks["generator_updated"] = False
        if checks["generator_artifact"]:
            with tempfile.TemporaryDirectory(dir=scratch) as tmp:
                materialize(case, Path(tmp))
                checks["generator_updated"] = lesson.read_text() != (Path(tmp) / "generator/SKILL.md").read_text()
    if kind in ("clean", "access") and checks["generator_artifact"]:
        with tempfile.TemporaryDirectory(dir=scratch) as tmp:
            materialize(case, Path(tmp))
            checks["no_unconfirmed_lesson"] = lesson.read_text() == (Path(tmp) / "generator/SKILL.md").read_text()
    return {"case": case, "fixture_version": FIXTURE_VERSION, "grader_version": GRADER_VERSION,
            "execution_boundary": execution_boundary(),
            "checks": checks, "executable_checks_passed": all(checks.values()), "skill_evaluation_complete": False,
            "human_review_required": ["Evidence supports classification and actual swarm use",
                                      "Root cause and lesson quality, scope, and provenance",
                                      "Attack budget and honest coverage limitations"], "evidence": evidence}


def probe_verifier(work, oracle, checks):
    outcomes = []
    # Cross task outcomes with nuisance artifacts so those artifacts cannot serve
    # as an accidental label for the grader's positive and negative examples.
    for result in (None, {"success": True}, {"success": False}):
        for audit in ({"method": "reference"}, {"method": "bulk-update"}, None):
            outcomes.append(probe_outcome(work, oracle, GOAL, result, audit, True))
    checks["accepts_valid_outcomes"] = all(outcomes)
    outcomes = []
    for rows in (INITIAL, [(1, "New Lane"), (2, "Changed")], [(1, "New Lane")], []):
        for result in (None, {"success": True}, {"success": False}):
            outcomes.append(probe_outcome(work, oracle, rows, result, {"method": "reference"}, False))
    checks["rejects_invalid_outcomes_without_mutating_them"] = all(outcomes)


def probe_outcome(source, oracle, rows, result, audit, expected):
    # Each probe starts from a fresh workspace: verifier scratch/counters cannot
    # carry across examples, and VM-backed bind mounts see newly seeded files.
    with tempfile.TemporaryDirectory(prefix="probe-", dir=source.parent) as tmp:
        work = Path(tmp)
        for name in ("verify.py", "reset.py", "solution.py"):
            shutil.copyfile(source / name, work / name)
        write_state(work, rows)
        set_artifacts(work, result, audit)
        return verdict(run_script(work, "verify.py", oracle), expected) and state(work) == rows


def set_artifacts(work, result, audit):
    for name, content in (("result.json", result), ("audit.json", audit)):
        path = work / name
        if path.exists() or path.is_symlink():
            path.unlink()
        if content is not None:
            path.write_text(json.dumps(content))


def probe_reset(source, oracle):
    with tempfile.TemporaryDirectory(prefix="reset-probe-", dir=source.parent) as tmp:
        work = Path(tmp)
        for name in ("verify.py", "reset.py", "solution.py"):
            shutil.copyfile(source / name, work / name)
        (work / "state.sqlite").write_bytes(b"not a SQLite database")
        set_artifacts(work, {"success": True}, {"method": "reference"})
        result = run_script(work, "reset.py", oracle)
        return (result["code"] == 0 and state(work) == INITIAL
                and not (work / "result.json").exists() and not (work / "audit.json").exists())


def prepare(destination):
    destination.mkdir(parents=True, exist_ok=False)
    mapping = {}
    for index, case in enumerate(CASES):
        alias = f"case-{chr(97 + index)}"
        mapping[alias] = case
        root = destination / alias
        root.mkdir()
        work, _ = setup(case, root)
        shutil.copyfile(HERE / "candidate.md", root / "REQUEST.md")
        (root / "submission").mkdir()
    (destination / "operator-manifest.json").write_text(json.dumps(mapping, indent=2))
    print(json.dumps({"prepared": str(destination), "operator_manifest": mapping}, indent=2))


def main():
    global EXECUTOR
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("prepare")
    p.add_argument("destination", type=Path)
    health = commands.add_parser("preflight")
    health.add_argument("--executor", choices=("local", "docker"), default=EXECUTOR)
    g = commands.add_parser("grade")
    g.add_argument("case", choices=CASES)
    g.add_argument("submission", type=Path)
    g.add_argument("--executor", choices=("local", "docker"), default=EXECUTOR)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.destination.resolve())
        return
    EXECUTOR = args.executor
    try:
        if args.command == "preflight":
            print(json.dumps({"execution_boundary": execution_boundary(),
                              "preflight": preflight(scratch_root())}, indent=2))
            return
        result = grade(args.case, args.submission.resolve())
    except InfrastructureError as exc:
        result = infrastructure_result(exc, case=getattr(args, "case", None))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        result = {"case": getattr(args, "case", None), "execution_boundary": execution_boundary(),
                  "assessment": "execution-error", "executable_checks_passed": None, "error": str(exc)}
    print(json.dumps(result, indent=2))
    if result.get("assessment") in ("requires-independent-adjudication", "execution-error", "infrastructure-error"):
        raise SystemExit(2)
    raise SystemExit(0 if result["executable_checks_passed"] else 1)


if __name__ == "__main__":
    main()
