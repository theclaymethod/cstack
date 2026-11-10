#!/usr/bin/env python3
"""Native deterministic evaluator and bounded local campaign for this fixture.

Candidates are trusted local Python programs. A fresh subprocess and temporary
working directory reset each trial; they do not sandbox a malicious program.
"""

import argparse
from contextlib import contextmanager
import difflib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
TIMEOUT_SECONDS = 3
PROTOCOL = {
    "name": "deterministic-local-support-v1",
    "trials_per_case": 1,
    "timeout_seconds": TIMEOUT_SECONDS,
    "python_flags": ["-I"],
    "new_ticket_issue": "vpn",
    "new_ticket_status": "open",
    "selection": "strict development improvement; preserve every incumbent PASS",
    "confirmation": "baseline and incumbent; preserve baseline PASS; no lower score",
    "execution_boundary": "trusted local subprocess; not a security sandbox",
}
FROZEN_FILES = ("evaluate.py", "evals/spec.json", "evals/cases.jsonl", "evals/rubric.md")


class CampaignError(ValueError):
    """Invalid setup, changed campaign identity, or exhausted allocation."""


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    """Atomically publish each durable state transition on this local filesystem."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def identity():
    return {
        "files": {name: digest(ROOT / name) for name in FROZEN_FILES},
        "python": {
            "executable": str(Path(sys.executable).resolve()),
            "version": sys.version,
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "protocol": PROTOCOL,
    }


def load_cases(suite, cases_file=None):
    if suite not in ("development", "confirmation", "all"):
        raise CampaignError("suite must be development, confirmation, or all")
    cases_file = Path(cases_file) if cases_file is not None else ROOT / "evals/cases.jsonl"
    cases = [json.loads(line) for line in cases_file.read_text().splitlines() if line.strip()]
    ids = [case["id"] for case in cases]
    if not cases or len(ids) != len(set(ids)):
        raise CampaignError("cases must be nonempty and have unique IDs")
    for case in cases:
        if case.get("suite") not in ("development", "confirmation"):
            raise CampaignError("unsupported source suite")
        if not isinstance(case.get("family"), str) or not case["family"]:
            raise CampaignError("case needs a construction family")
        request, state, expected = case["request"], case["state"], case["expected"]
        if not isinstance(request.get("text"), str) or not isinstance(request.get("accounts"), list):
            raise CampaignError("invalid request")
        if not all(isinstance(a, str) for a in request["accounts"]):
            raise CampaignError("accounts must be string IDs")
        if request.get("account") is not None and not isinstance(request["account"], str):
            raise CampaignError("requested account must be string or null")
        if not isinstance(state.get("tickets"), list):
            raise CampaignError("state needs tickets")
        if any(not valid_ticket(ticket) for ticket in state["tickets"]):
            raise CampaignError("invalid input ticket")
        if len({t["id"] for t in state["tickets"]}) != len(state["tickets"]):
            raise CampaignError("input ticket IDs must be unique")
        if not expected.get("allowed_actions") or not set(expected["allowed_actions"]) <= {"guidance", "clarify", "create_ticket"}:
            raise CampaignError("invalid allowed actions")
        if type(expected.get("ticket_delta")) is not int or expected["ticket_delta"] not in (0, 1):
            raise CampaignError("ticket_delta must be 0 or 1")
        if "account" not in expected:
            raise CampaignError("expected account is required")
    selected = [c for c in cases if suite == "all" or c["suite"] == suite]
    if not selected:
        raise CampaignError("selected suite is empty")
    return selected


def valid_ticket(value):
    return (isinstance(value, dict) and set(value) == {"id", "account", "status", "issue"}
            and all(isinstance(v, str) and bool(v) for v in value.values()))


def grade(output, case):
    """The only grading path: structural errors, then observable task checks."""
    if (not isinstance(output, dict) or not {"action", "account", "state", "note"} <= set(output)
            or not isinstance(output.get("action"), str)
            or (output.get("account") is not None and not isinstance(output["account"], str))
            or not isinstance(output.get("note"), str)
            or not isinstance(output.get("state"), dict)
            or not isinstance(output["state"].get("tickets"), list)
            or any(not valid_ticket(t) for t in output["state"]["tickets"])):
        return {"outcome": "ERROR", "checks": {}, "error": "malformed candidate JSON schema"}
    original = case["state"]["tickets"]
    tickets = output["state"]["tickets"]
    original_by_id = {ticket["id"]: ticket for ticket in original}
    by_id = {ticket["id"]: ticket for ticket in tickets}
    new = [ticket for ticket in tickets if ticket["id"] not in original_by_id]
    expected = case["expected"]
    checks = {
        "allowed_action": output["action"] in expected["allowed_actions"],
        "requested_account": output["account"] == expected["account"],
        "preserved_tickets": tickets[:len(original)] == original,
        "unique_ticket_ids": len(by_id) == len(tickets),
        "ticket_delta": len(tickets) - len(original) == expected["ticket_delta"],
        "new_ticket_membership": len(new) == expected["ticket_delta"],
        "new_ticket_fields": all(t["account"] == expected["account"] and t["account"] in case["request"]["accounts"]
                                 and t["status"] == "open" and t["issue"] == "vpn" for t in new),
        "action_matches_mutation": (output["action"] == "create_ticket") == bool(new),
        "preserved_other_state": {k: v for k, v in output["state"].items() if k != "tickets"}
                                 == {k: v for k, v in case["state"].items() if k != "tickets"},
    }
    return {"outcome": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "error": None}


def run_case(candidate, case):
    payload = {"request": case["request"], "state": case["state"]}
    observation = {"id": case["id"], "suite": case["suite"], "family": case["family"], "input": payload,
                   "stdout": "", "stderr": "", "exit_code": None, "output": None}
    try:
        with tempfile.TemporaryDirectory(prefix="cstack-case-") as scratch:
            process = subprocess.run([sys.executable, "-I", str(candidate)], input=json.dumps(payload),
                                     text=True, capture_output=True, cwd=scratch, timeout=TIMEOUT_SECONDS,
                                     env={"PATH": os.defpath, "LANG": "C.UTF-8"})
        observation.update(stdout=process.stdout, stderr=process.stderr, exit_code=process.returncode)
        if process.returncode != 0:
            raise CampaignError("candidate exited unsuccessfully")
        observation["output"] = json.loads(process.stdout)
        result = grade(observation["output"], case)
    except subprocess.TimeoutExpired as error:
        observation["stdout"] = (error.stdout or b"").decode(errors="replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
        observation["stderr"] = (error.stderr or b"").decode(errors="replace") if isinstance(error.stderr, bytes) else (error.stderr or "")
        result = {"outcome": "ERROR", "checks": {}, "error": "candidate timeout"}
    except (OSError, ValueError) as error:
        result = {"outcome": "ERROR", "checks": {}, "error": str(error)}
    observation.update(result)
    return observation


def run_suite(candidate, suite, out, cases_file=None):
    """Execute the immutable snapshot anew for every selected case."""
    cases_file = Path(cases_file).resolve() if cases_file is not None else ROOT / "evals/cases.jsonl"
    cases = load_cases(suite, cases_file)
    cases_source = {"path": str(cases_file), "sha256": digest(cases_file)}
    frozen = identity()
    out = Path(out).resolve()
    candidate = Path(candidate).resolve()
    if not candidate.is_file():
        raise CampaignError("candidate file does not exist")
    out.mkdir(parents=True, exist_ok=False)
    snapshot = out / "candidate.py"
    shutil.copyfile(candidate, snapshot)
    snapshot.chmod(0o444)
    manifest = {"schema_version": 1, "identity": frozen, "suite": suite,
                "case_ids": [c["id"] for c in cases], "candidate_hash": digest(snapshot),
                "candidate_source": str(candidate), "cases_source": cases_source,
                "execution_mode": "fresh subprocess per case"}
    write_json(out / "manifest.json", manifest)
    results = []
    complete = False
    try:
        with (out / "traces.jsonl").open("w") as traces:
            for case in cases:
                result = run_case(snapshot, case)
                results.append(result)
                traces.write(json.dumps(result, sort_keys=True) + "\n")
                traces.flush()
                os.fsync(traces.fileno())
        if (identity() != frozen or digest(snapshot) != manifest["candidate_hash"]
                or digest(cases_file) != cases_source["sha256"]):
            raise CampaignError("evaluation or candidate changed during execution")
        complete = True
    finally:
        counts = {name: sum(r["outcome"] == name for r in results) for name in ("PASS", "FAIL", "ERROR", "UNKNOWN")}
        summary = {"complete": complete, "selected_count": len(cases), "executed_count": len(results),
                   "case_ids": manifest["case_ids"], "candidate_hash": manifest["candidate_hash"],
                   "identity_hash": json_hash(frozen), "counts": counts,
                   "score": counts["PASS"] / len(cases),
                   "results": [{k: r[k] for k in ("id", "suite", "outcome", "checks", "error")} for r in results]}
        write_json(out / "summary.json", summary)
    return summary


def checked_run(path):
    path = Path(path)
    manifest, summary = read_json(path / "manifest.json"), read_json(path / "summary.json")
    if not summary["complete"] or summary["executed_count"] != len(manifest["case_ids"]):
        raise CampaignError("incomplete run cannot support comparison or promotion")
    if digest(path / "candidate.py") != manifest["candidate_hash"] or summary["candidate_hash"] != manifest["candidate_hash"]:
        raise CampaignError("candidate snapshot changed")
    if summary["identity_hash"] != json_hash(manifest["identity"]):
        raise CampaignError("run identity changed")
    if summary["case_ids"] != manifest["case_ids"] or [r["id"] for r in summary["results"]] != manifest["case_ids"]:
        raise CampaignError("case coverage differs from manifest")
    counts = {name: sum(r["outcome"] == name for r in summary["results"]) for name in ("PASS", "FAIL", "ERROR", "UNKNOWN")}
    if summary["counts"] != counts or sum(counts.values()) != len(manifest["case_ids"]) or summary["score"] != counts["PASS"] / len(manifest["case_ids"]):
        raise CampaignError("summary counts or score differ from per-case results")
    return manifest, summary


def compare_runs(baseline, candidate):
    bm, bs = checked_run(baseline)
    cm, cs = checked_run(candidate)
    if (bm["identity"] != cm["identity"] or bm["case_ids"] != cm["case_ids"] or bm["suite"] != cm["suite"]
            or bm["cases_source"]["sha256"] != cm["cases_source"]["sha256"]):
        raise CampaignError("runs have different evaluation contracts or case membership")
    before = {r["id"]: r["outcome"] for r in bs["results"]}
    after = {r["id"]: r["outcome"] for r in cs["results"]}
    regressions = [key for key in before if before[key] == "PASS" and after[key] != "PASS"]
    gains = [key for key in before if before[key] != "PASS" and after[key] == "PASS"]
    return {"baseline_score": bs["score"], "candidate_score": cs["score"], "gains": gains,
            "regressions": regressions, "errors": cs["counts"]["ERROR"],
            "strict_improvement": cs["score"] > bs["score"],
            "admissible": not regressions and cs["counts"]["ERROR"] == 0 and cs["counts"]["UNKNOWN"] == 0,
            "case_ids": bm["case_ids"]}


@contextmanager
def campaign_lock(directory):
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield directory


def save_state(directory, state):
    write_json(directory / "state.json", state)


def load_campaign(directory):
    contract, state = read_json(directory / "contract.json"), read_json(directory / "state.json")
    if json_hash(contract) != state["contract_hash"]:
        raise CampaignError("campaign contract changed")
    if contract["identity"] != identity():
        raise CampaignError("frozen source, Python, or deterministic configuration changed; start a new campaign")
    if contract["case_ids"] != {s: [c["id"] for c in load_cases(s)] for s in ("development", "confirmation")}:
        raise CampaignError("case membership changed")
    used = sum(a["reserved_case_runs"] for a in state["attempts"])
    if used != state["used_case_runs"] or used > contract["max_case_runs"]:
        raise CampaignError("invalid budget accounting")
    for attempt in state["attempts"]:
        if attempt["reserved_case_runs"] != len(contract["case_ids"][attempt["suite"]]):
            raise CampaignError("attempt allocation differs from frozen case membership")
        if attempt["status"] == "complete":
            for name, expected in attempt["evidence_hashes"].items():
                if digest(directory / attempt["path"] / name) != expected:
                    raise CampaignError("completed attempt evidence changed")
            manifest, summary = checked_run(directory / attempt["path"])
            if (manifest["identity"] != contract["identity"] or manifest["suite"] != attempt["suite"]
                    or manifest["case_ids"] != contract["case_ids"][attempt["suite"]]
                    or manifest["candidate_hash"] != attempt["candidate_hash"]
                    or summary["executed_count"] != attempt["reserved_case_runs"]):
                raise CampaignError("completed attempt differs from frozen allocation")
    if state["best_attempt"] is not None and state["attempts"][state["best_attempt"]]["status"] != "complete":
        raise CampaignError("best artifact references an incomplete attempt")
    if state["status"] == "finished":
        for name, expected in state["deliverable_hashes"].items():
            if digest(directory / name) != expected:
                raise CampaignError("delivered artifact changed")
    return contract, state


def reserve_attempt(directory, contract, state, candidate, suite, role, hypothesis, protect_reserve):
    count = len(contract["case_ids"][suite])
    available = contract["max_case_runs"] - state["used_case_runs"]
    protected = contract["reserve_case_runs"] if protect_reserve else 0
    if count > available - protected:
        raise CampaignError("case-run budget exhausted; confirmation reserve is protected")
    candidate = Path(candidate).resolve()
    if not candidate.is_file():
        raise CampaignError("candidate file does not exist")
    index = len(state["attempts"])
    attempt = {"id": index, "path": f"attempts/{index:03d}-{role}", "role": role,
               "suite": suite, "status": "pending", "reserved_case_runs": count,
               "hypothesis": hypothesis, "parent": state["best_attempt"], "candidate_hash": digest(candidate)}
    state["attempts"].append(attempt)
    state["used_case_runs"] += count
    save_state(directory, state)  # Reservation survives interruption before execution.
    return attempt


def execute_attempt(directory, state, attempt, candidate):
    summary = run_suite(candidate, attempt["suite"], directory / attempt["path"])
    if summary["candidate_hash"] != attempt["candidate_hash"]:
        raise CampaignError("candidate changed after budget reservation")
    attempt["status"] = "complete"
    attempt["executed_case_runs"] = summary["executed_count"]
    attempt["evidence_hashes"] = {name: digest(directory / attempt["path"] / name)
                                  for name in ("manifest.json", "summary.json", "traces.jsonl", "candidate.py")}
    save_state(directory, state)
    return summary


def start_campaign(directory, max_case_runs=48, reserve_case_runs=8):
    """48 is a small demonstration allowance, not a recommended universal budget."""
    with campaign_lock(directory) as directory:
        if (directory / "state.json").exists() or (directory / "contract.json").exists():
            raise CampaignError("campaign already exists; use status or a new directory")
        case_ids = {s: [c["id"] for c in load_cases(s)] for s in ("development", "confirmation")}
        minimum = 2 * len(case_ids["confirmation"])
        if type(max_case_runs) is not int or type(reserve_case_runs) is not int or reserve_case_runs < minimum:
            raise CampaignError(f"confirmation requires a reserve of at least {minimum} case-runs")
        if max_case_runs < len(case_ids["development"]) + reserve_case_runs:
            raise CampaignError("budget cannot cover baseline and confirmation reserve")
        contract = {"schema_version": 1, "identity": identity(), "case_ids": case_ids,
                    "editable_artifact": "standalone candidate Python program",
                    "max_case_runs": max_case_runs, "reserve_case_runs": reserve_case_runs,
                    "source_authority": "evals/spec.json and rubric.md; synthetic fixture, not human calibration gold",
                    "stopping": "explicit finish or finite budget; reject each nonimproving proposal and retain incumbent",
                    "exposure": "reserved synthetic confirmation; no enforced secrecy or held-out generalization"}
        state = {"contract_hash": json_hash(contract), "status": "active", "used_case_runs": 0,
                 "attempts": [], "best_attempt": None, "last_decision": "baseline pending"}
        write_json(directory / "contract.json", contract)
        save_state(directory, state)
        attempt = reserve_attempt(directory, contract, state, ROOT / "support_agent.py", "development", "baseline", "measure original", True)
        execute_attempt(directory, state, attempt, ROOT / "support_agent.py")
        state["best_attempt"] = attempt["id"]
        state["last_decision"] = "baseline measured"
        save_state(directory, state)
        return campaign_status_unlocked(directory, contract, state)


def require_active(state):
    if state["status"] != "active":
        raise CampaignError("campaign is already finished")
    if state["best_attempt"] is None:
        raise CampaignError("baseline incomplete; preserve this campaign and start a new one")


def try_candidate(directory, candidate, hypothesis):
    with campaign_lock(directory) as directory:
        contract, state = load_campaign(directory)
        require_active(state)
        if not hypothesis.strip():
            raise CampaignError("a falsifiable hypothesis is required")
        incumbent = state["attempts"][state["best_attempt"]]
        attempt = reserve_attempt(directory, contract, state, candidate, "development", "proposal", hypothesis, True)
        execute_attempt(directory, state, attempt, candidate)
        comparison = compare_runs(directory / incumbent["path"], directory / attempt["path"])
        if comparison["admissible"] and comparison["strict_improvement"]:
            state["best_attempt"] = attempt["id"]
            decision = "retain improvement"
        elif comparison["regressions"]:
            decision = "reject regression"
        elif not comparison["admissible"]:
            decision = "reject incomplete or error"
        else:
            decision = "no improvement"
        attempt.update(decision=decision, comparison=comparison)
        state["last_decision"] = decision
        save_state(directory, state)
        return {"decision": decision, "comparison": comparison, **campaign_status_unlocked(directory, contract, state)}


def campaign_status_unlocked(directory, contract, state):
    pending = [a["id"] for a in state["attempts"] if a["status"] != "complete"]
    return {"campaign": str(directory), "status": state["status"], "used_case_runs": state["used_case_runs"],
            "max_case_runs": contract["max_case_runs"], "protected_confirmation_case_runs": contract["reserve_case_runs"] if state["status"] == "active" else 0,
            "search_case_runs_remaining": max(0, contract["max_case_runs"] - state["used_case_runs"] - (contract["reserve_case_runs"] if state["status"] == "active" else 0)),
            "pending_attempts": pending, "best_attempt": state["best_attempt"], "last_decision": state["last_decision"],
            "verification": "incomplete attempts remain charged" if pending else "record and completed evidence verified"}


def campaign_status(directory):
    with campaign_lock(directory) as directory:
        contract, state = load_campaign(directory)
        return campaign_status_unlocked(directory, contract, state)


def finish_campaign(directory):
    with campaign_lock(directory) as directory:
        contract, state = load_campaign(directory)
        if state["status"] == "finished":
            return campaign_status_unlocked(directory, contract, state)
        require_active(state)
        baseline = state["attempts"][0]
        incumbent = state["attempts"][state["best_attempt"]]
        confirmation = []
        # Complete retries reuse only completed matching evidence. Interrupted
        # reservations remain charged and cannot be promoted or silently rerun.
        for role, source in (("confirm-baseline", baseline), ("confirm-incumbent", incumbent)):
            matching = [a for a in state["attempts"] if a["role"] == role and a["candidate_hash"] == source["candidate_hash"]]
            if matching:
                attempt = matching[-1]
                if attempt["status"] != "complete":
                    raise CampaignError("confirmation interrupted and remains charged; start a new campaign for further confirmation")
            else:
                attempt = reserve_attempt(directory, contract, state, directory / source["path"] / "candidate.py", "confirmation", role,
                                          "confirm frozen selected artifacts", False)
                execute_attempt(directory, state, attempt, directory / source["path"] / "candidate.py")
            confirmation.append(attempt)
        comparison = compare_runs(*(directory / attempt["path"] for attempt in confirmation))
        confirmed = comparison["admissible"] and comparison["candidate_score"] >= comparison["baseline_score"]
        selected = incumbent if confirmed else baseline
        baseline_text = (directory / baseline["path"] / "candidate.py").read_text()
        selected_text = (directory / selected["path"] / "candidate.py").read_text()
        (directory / "best.py").write_text(selected_text)
        (directory / "best.diff").write_text("".join(difflib.unified_diff(baseline_text.splitlines(True), selected_text.splitlines(True),
                                                                          fromfile="baseline/support_agent.py", tofile="selected/support_agent.py")))
        report = {"selected_attempt": selected["id"], "development_incumbent": incumbent["id"],
                  "confirmation": comparison, "confirmation_selected": confirmed,
                  "pending_attempts": [a["id"] for a in state["attempts"] if a["status"] != "complete"],
                  "limits": "synthetic deterministic development and reserved-workflow evidence; trusted local execution; no generalization claim"}
        write_json(directory / "selection.json", report)
        state.update(status="finished", selected_attempt=selected["id"], last_decision="confirmed incumbent" if confirmed else "confirmation rejected; preserve baseline",
                     deliverable_hashes={name: digest(directory / name) for name in ("best.py", "best.diff", "selection.json")})
        save_state(directory, state)
        return {**campaign_status_unlocked(directory, contract, state), "selection": report}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--candidate", required=True, type=Path)
    run.add_argument("--suite", required=True, choices=("development", "confirmation", "all"))
    run.add_argument("--out", required=True, type=Path)
    run.add_argument("--cases", type=Path, help="native JSONL cases; defaults to evals/cases.jsonl")
    compare = commands.add_parser("compare")
    compare.add_argument("--baseline", required=True, type=Path)
    compare.add_argument("--candidate", required=True, type=Path)
    for name in ("start", "try", "finish", "status", "verify"):
        sub = commands.add_parser(name)
        sub.add_argument("--campaign", required=True, type=Path)
        if name == "start":
            sub.add_argument("--max-case-runs", type=int, default=48, help="demo default: 48")
            sub.add_argument("--reserve-case-runs", type=int, default=8)
        if name == "try":
            sub.add_argument("--candidate", required=True, type=Path)
            sub.add_argument("--hypothesis", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            result = run_suite(args.candidate, args.suite, args.out, args.cases)
        elif args.command == "compare":
            result = compare_runs(args.baseline, args.candidate)
        elif args.command == "start":
            result = start_campaign(args.campaign, args.max_case_runs, args.reserve_case_runs)
        elif args.command == "try":
            result = try_candidate(args.campaign, args.candidate, args.hypothesis)
        elif args.command == "finish":
            result = finish_campaign(args.campaign)
        else:
            result = campaign_status(args.campaign)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
