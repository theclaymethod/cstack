#!/usr/bin/env python3
"""Prepare incremental cases, capture real dataset checkpoints, and grade data only."""
import argparse
import hashlib
import json
from pathlib import Path
from fixtures import CASES, VERSION

VERSION_GRADER = 1


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


def reveal(state):
    case = CASES[state["case"]]
    work = Path(state["work"])
    position = state["position"]
    dump(work / "source.json", visible(case, position))
    # Assets are fixed input versions, not mutable product state.
    for name, value in case["assets"].items():
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
    state = {"case": name, "work": str(work), "position": case.get("start_at", 0), "captures": []}
    (work / "REQUEST.md").write_text((Path(__file__).parent / "candidate.md").read_text())
    reveal(state)
    dump(operator / "state.json", state)


def read_rows(path):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 1_000_000:
        raise ValueError("Expected a regular JSONL file of at most 1 MB")
    result = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if len(result) > 1000 or not all(isinstance(r, dict) for r in result):
        raise ValueError("Expected at most 1000 JSON objects")
    return result


def capture(operator):
    state = json.loads((operator / "state.json").read_text())
    case = CASES[state["case"]]
    if state["position"] >= len(case["turns"]):
        raise ValueError("All turns already captured")
    work = Path(state["work"])
    # Candidate-written checkpoint files are not accepted as timing evidence.
    expected = visible(case, state["position"])
    if json.loads((work / "source.json").read_text()) != expected:
        raise ValueError("Reviewed source was modified")
    for name, value in case["assets"].items():
        if json.loads((work / name).read_text()) != value:
            raise ValueError("Reviewed original artifact was modified")
    index = len(state["captures"])
    checkpoint = operator / f"checkpoint-{index}"
    checkpoint.mkdir()
    hashes = {}
    for name in ("reviews.jsonl", "rubric.jsonl"):
        content = (work / "dataset" / name).read_bytes()
        (checkpoint / name).write_bytes(content)
        hashes[name] = digest(content)
    reply = (work / "reply.md").read_bytes() if (work / "reply.md").is_file() else b""
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
    previous, prior_rubrics = [], []
    sources = {e["id"]: e for e in case["turns"]}
    for i, receipt in enumerate(state["captures"]):
        label = f"checkpoint_{i}"
        try:
            directory = operator / receipt["directory"]
            checks[label + "_integrity"] = all(digest((directory / name).read_bytes()) == h for name, h in receipt["hashes"].items())
            rows = read_rows(directory / "reviews.jsonl")
            rubrics = read_rows(directory / "rubric.jsonl")
            checks[label + "_append_only"] = rows[:len(previous)] == previous and rubrics[:len(prior_rubrics)] == prior_rubrics
            ids, chains, seen = set(), {}, set()
            valid = True
            allowed = {e["id"] for e in case["turns"][:receipt["position"] + 1]}
            for r in rows:
                identifier = r.get("record_id")
                source = sources.get(r.get("source_id"), {})
                valid &= isinstance(identifier, str) and bool(identifier) and identifier not in ids
                valid &= r.get("item_id") == case["item"] and r.get("output_ref") == case["output"]
                valid &= r.get("label") in ("incorrect", "uncertain", "retracted")
                valid &= source.get("role") == "expert" and source.get("id") in allowed and r.get("quote") == source.get("text")
                valid &= isinstance(r.get("unresolved"), list) and isinstance(r.get("replay_ready"), bool)
                example = r.get("example_id")
                valid &= isinstance(example, str) and bool(example)
                if r.get("amends") is not None:
                    valid &= r["amends"] in ids and chains.get(example, {}).get("record_id") == r["amends"]
                else:
                    valid &= example not in chains
                event_key = (r.get("source_id"), r.get("label"), json.dumps(r.get("correction"), sort_keys=True))
                valid &= event_key not in seen
                seen.add(event_key)
                if r.get("correction") is not None:
                    cs = sources.get(r.get("correction_source"), {})
                    valid &= cs.get("role") == "expert" and cs.get("id") in allowed and cs.get("id") == case.get("correction_source")
                ids.add(identifier)
                chains[example] = r
            checks[label + "_provenance_and_lineage"] = bool(valid)
            expected = case["expected"][i]
            active = list(chains.values())
            matches = len(active) == len(expected)
            for target in expected:
                found = [r for r in active if r.get("source_id") == target["source"] and r.get("label") == target["label"]]
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
                checks[label + "_no_approval_or_post_stop_capture"] = rows == previous
            rubric_valid = all(isinstance(r.get("question"), str) and bool(r["question"].strip())
                               and r.get("passing_answer") in ("yes", "no")
                               and r.get("source_id") in allowed
                               and sources.get(r.get("source_id"), {}).get("role") == "expert"
                               and r.get("quote") == sources[r["source_id"]]["text"]
                               and r.get("status") in ("confirmed", "proposed")
                               for r in rubrics)
            checks[label + "_rubric_sources"] = rubric_valid
            if state["case"] == "live-uncertainty" and i >= 2:
                checks[label + "_rubric_captured"] = any(r.get("source_id") == "u3" and r.get("scope") == "imported items only" for r in rubrics)
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
