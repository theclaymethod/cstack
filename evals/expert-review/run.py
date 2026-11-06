#!/usr/bin/env python3
"""Prepare incremental cases, capture real dataset checkpoints, and grade data only."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from fixtures import CASES, VERSION

VERSION_GRADER = 4
REVIEW_FIELDS = {"record_id", "example_id", "amends", "item_id", "output_ref", "label",
                 "source_id", "quote", "correction", "correction_source", "unresolved", "replay_ready"}
RUBRIC_FIELDS = {"rubric_id", "version", "question", "passing_answer", "source_id", "quote", "scope", "status"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def row(case, source, label="incorrect", correction=None, *, identifier="r1", amends=None):
    events = {e["id"]: e for e in case["turns"]}
    return {"record_id": identifier, "example_id": source, "amends": amends,
            "item_id": case["item"], "output_ref": case["output"], "label": label,
            "source_id": source, "quote": events[source]["text"],
            "correction": correction, "correction_source": None,
            "unresolved": [], "replay_ready": False}


def visible(case, position):
    return {"session_id": "synthetic-session", "events": case["turns"][:position + 1]}


def available_assets(case, position):
    return {name: value for name, value in case["assets"].items()
            if case.get("asset_reveal", {}).get(name, 0) <= position}


def reveal(state):
    case = CASES[state["case"]]
    work = Path(state["work"])
    position = state["position"]
    dump(work / "source.json", visible(case, position))
    # Assets are fixed input versions, not mutable product state.
    for name, value in available_assets(case, position).items():
        dump(work / name, value)
    (work / "CURRENT_TURN.md").write_text(case["turns"][position]["text"] + "\n")


def prepare(name, work, operator):
    work, operator = work.resolve(), operator.resolve()
    if work == operator or work in operator.parents or operator in work.parents:
        raise ValueError("Workspace and operator receipts must be separate sibling trees.")
    work.mkdir(parents=True, exist_ok=False)
    operator.mkdir(parents=True, exist_ok=False)
    case = CASES[name]
    (work / "dataset").mkdir()
    for filename in ("reviews.jsonl", "rubric.jsonl"):
        (work / "dataset" / filename).write_text("")
    if case.get("seed"):
        (work / "dataset/reviews.jsonl").write_text(json.dumps(row(case, case["seed"])) + "\n")
    shutil.copytree(work / "dataset", operator / "initial")
    state = {"case": name, "work": str(work), "position": case.get("start_at", 0), "captures": []}
    suite = Path(__file__).resolve().parent
    (work / "REQUEST.md").write_text((suite / "candidate.md").read_text())
    guidance = suite.parents[1] / "skills"
    for name in ("expert-mode", "distill-me"):
        shutil.copytree(guidance / name, work / "guidance" / name)
    state["input_hashes"] = {
        str(p.relative_to(work)): digest(p.read_bytes())
        for p in (work / "guidance").rglob("*") if p.is_file()
    }
    state["input_hashes"]["REQUEST.md"] = digest((work / "REQUEST.md").read_bytes())
    dump(operator / "versions.json", {
        "fixture_version": VERSION, "grader_version": VERSION_GRADER,
        "source_hashes": {name: digest((suite / name).read_bytes())
                          for name in ("run.py", "fixtures.py", "candidate.md")},
        "guidance_hashes": state["input_hashes"], "run_kind": "development",
        "execution_boundary": "Host instructions; data parsing only; no OS isolation"
    })
    reveal(state)
    dump(operator / "state.json", state)


def read_rows(path):
    result = [json.loads(line) for line in read_data(path).decode().splitlines() if line.strip()]
    if len(result) > 1000 or not all(isinstance(r, dict) for r in result):
        raise ValueError("Expected at most 1000 JSON objects")
    return result


def read_data(path, limit=1_000_000):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        raise ValueError("Expected a bounded regular file")
    with path.open("rb") as handle:
        content = handle.read(limit + 1)
    if len(content) > limit:
        raise ValueError("File exceeds size limit")
    return content


def capture(operator):
    state = json.loads((operator / "state.json").read_text())
    case = CASES[state["case"]]
    if state["position"] >= len(case["turns"]):
        raise ValueError("All turns already captured")
    work = Path(state["work"])
    for name, expected_hash in state["input_hashes"].items():
        if digest((work / name).read_bytes()) != expected_hash:
            raise ValueError("Task request or supplied guidance was modified")
    # Candidate-written checkpoint files are not accepted as timing evidence.
    expected = visible(case, state["position"])
    if json.loads((work / "source.json").read_text()) != expected:
        raise ValueError("Reviewed source was modified")
    for name, value in available_assets(case, state["position"]).items():
        if json.loads((work / name).read_text()) != value:
            raise ValueError("Reviewed original artifact was modified")
    index = len(state["captures"])
    checkpoint = operator / f"checkpoint-{index}"
    checkpoint.mkdir()
    hashes = {}
    for name in ("reviews.jsonl", "rubric.jsonl"):
        content = read_data(work / "dataset" / name)
        (checkpoint / name).write_bytes(content)
        hashes[name] = digest(content)
    reply = read_data(work / "reply.md", 100_000) if (work / "reply.md").exists() else b""
    (checkpoint / "reply.md").write_bytes(reply)
    hashes["reply.md"] = digest(reply)
    state["captures"].append({"position": state["position"], "directory": checkpoint.name, "hashes": hashes})
    state["position"] += 1
    if state["position"] < len(case["turns"]):
        reveal(state)
    dump(operator / "state.json", state)
    return {"captured": index, "next_turn": state["position"] if state["position"] < len(case["turns"]) else None}


def grade(operator):
    state = json.loads((operator / "state.json").read_text())
    case = CASES[state["case"]]
    checks, details = {}, []
    start = case.get("start_at", 0)
    checks["all_turns_captured"] = len(state["captures"]) == len(case["expected"])
    previous = read_rows(operator / "initial/reviews.jsonl")
    prior_rubrics = read_rows(operator / "initial/rubric.jsonl")
    sources = {e["id"]: e for e in case["turns"]}
    for i, receipt in enumerate(state["captures"]):
        label = f"checkpoint_{i}"
        try:
            checks[label + "_sequence"] = receipt["position"] == start + i
            directory = operator / receipt["directory"]
            checks[label + "_integrity"] = all(digest((directory / name).read_bytes()) == h for name, h in receipt["hashes"].items())
            rows = read_rows(directory / "reviews.jsonl")
            rubrics = read_rows(directory / "rubric.jsonl")
            checks[label + "_append_only"] = rows[:len(previous)] == previous and rubrics[:len(prior_rubrics)] == prior_rubrics
            ids, chains, origins, seen = set(), {}, {}, set()
            valid = True
            allowed = {e["id"] for e in case["turns"][:receipt["position"] + 1]}
            for r in rows:
                valid &= REVIEW_FIELDS <= r.keys()
                identifier = r.get("record_id")
                source = sources.get(r.get("source_id"), {})
                provisional = (source.get("role") == "summary" and r.get("label") == "uncertain"
                               and r.get("correction") is None and bool(r.get("unresolved"))
                               and r.get("replay_ready") is False and r.get("output_ref") is None)
                valid &= isinstance(identifier, str) and bool(identifier.strip()) and identifier not in ids
                valid &= r.get("item_id") == case["item"] and r.get("output_ref") == case["output"]
                valid &= r.get("label") in ("incorrect", "uncertain", "retracted")
                valid &= (source.get("role") == "expert" or provisional) and source.get("id") in allowed and r.get("quote") == source.get("text")
                valid &= isinstance(r.get("unresolved"), list) and isinstance(r.get("replay_ready"), bool)
                valid &= all(isinstance(gap, str) and bool(gap.strip()) for gap in r.get("unresolved", []))
                example = r.get("example_id")
                valid &= isinstance(example, str) and bool(example.strip())
                if r.get("amends") is not None:
                    valid &= r["amends"] in ids and chains.get(example, {}).get("record_id") == r["amends"]
                else:
                    valid &= example not in chains
                    origins[example] = r.get("source_id")
                event_key = (r.get("source_id"), r.get("label"), json.dumps(r.get("correction"), sort_keys=True))
                valid &= event_key not in seen
                seen.add(event_key)
                if r.get("correction") is not None:
                    cs = sources.get(r.get("correction_source"), {})
                    valid &= cs.get("role") == "expert" and cs.get("id") in allowed and cs.get("id") == case.get("correction_source")
                else:
                    valid &= r.get("correction_source") is None
                if r.get("unresolved") or r.get("label") in ("uncertain", "retracted"):
                    valid &= r.get("replay_ready") is False
                ids.add(identifier)
                chains[example] = r
            checks[label + "_provenance_and_lineage"] = bool(valid)
            expected = case["expected"][i]
            active = list(chains.values())
            matches = len(active) == len(expected)
            if state["case"] == "partial-context":
                # Both reporting the gap and retaining a provisional summary are valid.
                matches = len(active) <= 1 and all(r.get("source_id") == "s1" and r.get("label") == "uncertain" for r in active)
            for target in expected:
                found = [r for r in active if r.get("label") == target["label"] and (
                    r.get("source_id") == target["source"] or (
                        target["correction"] is not None and origins.get(r.get("example_id")) == target["source"]
                        and r.get("source_id") == case.get("correction_source")))]
                matches &= len(found) == 1
                if len(found) == 1:
                    r = found[0]
                    matches &= r.get("correction") == target["correction"]
                    if target["unresolved"]:
                        matches &= bool(r.get("unresolved")) and r.get("replay_ready") is False
            checks[label + "_expected_observations"] = bool(matches)
            if state["case"] == "distill-merge" and i == 1:
                checks["repeat_invocation_idempotent"] = rows == previous and rubrics == prior_rubrics
            if state["case"] == "live-correction" and i >= 4:
                checks[label + "_no_approval_or_post_stop_capture"] = rows == previous and rubrics == prior_rubrics
            if (state["case"] == "activation" and i <= 2) or (state["case"] == "distill-merge" and i == 2):
                checks[label + "_inactive_capture_unchanged"] = rows == previous and rubrics == prior_rubrics
            rubric_valid = all(RUBRIC_FIELDS <= r.keys()
                               and isinstance(r.get("rubric_id"), str) and bool(r["rubric_id"].strip())
                               and type(r.get("version")) is int and r["version"] > 0
                               and isinstance(r.get("scope"), str) and bool(r["scope"].strip())
                               and isinstance(r.get("question"), str) and bool(r["question"].strip())
                               and (r.get("passing_answer") in ("yes", "no") or (
                                   r.get("status") == "proposed" and r.get("passing_answer") is None
                                   and isinstance(r.get("unresolved"), list) and bool(r["unresolved"])
                                   and all(isinstance(gap, str) and bool(gap.strip()) for gap in r["unresolved"])))
                               and r.get("source_id") in allowed
                               and sources.get(r.get("source_id"), {}).get("role") == "expert"
                               and r.get("quote") == sources[r["source_id"]]["text"]
                               and r.get("status") in ("confirmed", "proposed")
                               for r in rubrics)
            rubric_versions, latest_rubrics = set(), {}
            for r in rubrics:
                key = (r.get("rubric_id"), r.get("version"))
                rubric_valid &= key not in rubric_versions
                rubric_versions.add(key)
                prior = latest_rubrics.get(r.get("rubric_id"))
                if prior is not None:
                    rubric_valid &= r["version"] > prior["version"]
                latest_rubrics[r.get("rubric_id")] = r
            checks[label + "_rubric_sources"] = rubric_valid
            if state["case"] == "live-uncertainty" and i >= 2:
                criterion_sources = {"u3"} if i == 2 else {"u3", "u4"}
                checks[label + "_rubric_captured"] = any(
                    r.get("source_id") in criterion_sources and r.get("scope") == "imported items only"
                    and (i == 2 or (r.get("status") == "confirmed" and r.get("passing_answer") in ("yes", "no")))
                    for r in latest_rubrics.values())
            previous, prior_rubrics = rows, rubrics
            details.append({"position": receipt["position"], "rows": len(rows), "rubrics": len(rubrics)})
        except (ValueError, TypeError, KeyError, IndexError, OSError) as exc:
            checks[label + "_valid_data"] = False
            details.append({"position": receipt["position"], "error": str(exc)})
    return {"case": state["case"], "fixture_version": VERSION, "grader_version": VERSION_GRADER,
            "checks": checks, "artifact_checks_passed": all(checks.values()), "skill_evaluation_complete": False,
            "human_review_required": ["Clinical/domain meaning and correction normalization", "Binary rubric question semantics and scope",
                                      "Selective useful clarification and succinct replies", "Actual independent review passes and source-access compliance",
                                      "Honest partial-context coverage and replay-readiness claims"], "checkpoints": details}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare"); p.add_argument("case", choices=CASES); p.add_argument("work", type=Path); p.add_argument("operator", type=Path)
    for name in ("capture", "grade"):
        p = sub.add_parser(name); p.add_argument("operator", type=Path)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.case, args.work, args.operator); return
    value = capture(args.operator) if args.command == "capture" else grade(args.operator)
    print(json.dumps(value, indent=2))
    if args.command == "grade":
        raise SystemExit(0 if value["artifact_checks_passed"] else 1)


if __name__ == "__main__":
    main()
