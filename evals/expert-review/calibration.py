#!/usr/bin/env python3
"""Hand-authored reference records and insufficient-output controls, not model scores."""
import argparse
import json
from pathlib import Path
import run
from fixtures import CASES


def append(path, value):
    with path.open("a") as f:
        f.write(json.dumps(value) + "\n")


def reference(case, work, position):
    name = next(k for k, v in CASES.items() if v is case)
    path = work / "dataset/reviews.jsonl"
    rows = run.read_rows(path)
    if name == "live-correction":
        if position == 1:
            append(path, run.row(case, "u2"))
        if position == 3:
            r = run.row(case, "u2", correction="blue", identifier="r2", amends="r1")
            r["correction_source"] = "u4"
            append(path, r)
    if name == "live-uncertainty":
        if position == 1:
            r = run.row(case, "u2", "uncertain")
            r["unresolved"] = ["Whether this probability is actually wrong"]
            append(path, r)
        if position == 2:
            source = case["turns"][2]
            append(work / "dataset/rubric.jsonl", {"rubric_id": "source-named", "version": 1,
                   "question": "Is the source named?", "passing_answer": "yes", "source_id": "u3",
                   "quote": source["text"], "scope": "imported items only", "status": "confirmed"})
        if position == 3:
            r = run.row(case, "u4", identifier="r2")
            r["unresolved"] = ["No replacement probability supplied"]
            append(path, r)
    if name == "distill-merge":
        if position == 3:
            r = run.row(case, "u2", correction="blue", identifier="r2", amends="r1")
            r["correction_source"] = "u3"
            append(path, r)
        if position == 6:
            r = run.row(case, "u6", "retracted", identifier="r3", amends="r2")
            r["example_id"] = "u2"
            append(path, r)
    if name == "activation" and position == 3:
        r = run.row(case, "u4", correction="blue")
        r["correction_source"] = "u4"
        append(path, r)
    (work / "reply.md").write_text("Recorded supported observations; unresolved context remains explicit.\n")


def exercise(name, destination, mutate=None):
    work, operator = destination / "work", destination / "operator"
    run.prepare(name, work, operator)
    case = CASES[name]
    for position in range(case.get("start_at", 0), len(case["turns"])):
        reference(case, work, position)
        if mutate:
            mutate(work, position)
        run.capture(operator)
    return run.grade(operator)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    root = args.destination.resolve()
    root.mkdir(parents=True, exist_ok=False)
    summary = []
    for name in CASES:
        result = exercise(name, root / name)
        run.dump(root / name / "result.json", result)
        summary.append({"case": name, "passed": result["artifact_checks_passed"]})
    for variant in ("empty", "agent-correction", "rewrite", "duplicate", "false-source"):
        def mutate(work, position):
            path = work / "dataset/reviews.jsonl"
            rows = run.read_rows(path)
            if variant == "empty": rows = []
            if rows and variant == "agent-correction":
                rows[-1]["correction"] = "green"; rows[-1]["correction_source"] = "a3"
            if len(rows) == 2 and variant == "rewrite":
                rows[0]["correction"] = "blue"; rows[0]["correction_source"] = "u4"
            if rows and variant == "duplicate":
                extra = dict(rows[0]); extra["record_id"] = f"duplicate-{position}"; extra["example_id"] = f"extra-{position}"; rows.append(extra)
            if rows and variant == "false-source": rows[-1]["quote"] = "The expert approved this correction."
            path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        result = exercise("live-correction", root / variant, mutate)
        run.dump(root / variant / "result.json", result)
        summary.append({"case": variant, "passed": not result["artifact_checks_passed"]})
    for variant, name, expected_pass in (
            ("seed-deletion", "distill-merge", False),
            ("missing-rubric-identity", "live-uncertainty", False),
            ("provisional-summary", "partial-context", True),
            ("correcting-turn-source", "live-correction", True),
            ("pending-rubric", "live-uncertainty", True),
            ("confirmed-null", "live-uncertainty", False),
            ("pending-no-gap", "live-uncertainty", False),
            ("criterion-without-replacement", "live-uncertainty", True)):
        def mutate(work, position):
            path = work / "dataset/reviews.jsonl"
            rows = run.read_rows(path)
            if variant == "seed-deletion" and position == 3:
                rows = rows[1:]
                rows[0]["amends"] = None
            if variant == "missing-rubric-identity":
                rubric_path = work / "dataset/rubric.jsonl"
                rubrics = run.read_rows(rubric_path)
                for rubric in rubrics:
                    rubric.pop("rubric_id", None); rubric.pop("version", None)
                rubric_path.write_text("".join(json.dumps(r) + "\n" for r in rubrics))
            if variant in ("pending-rubric", "confirmed-null", "pending-no-gap") and position == 2:
                rubric_path = work / "dataset/rubric.jsonl"
                rubrics = run.read_rows(rubric_path)
                r = rubrics[-1]
                r["passing_answer"] = None
                r["status"] = "confirmed" if variant == "confirmed-null" else "proposed"
                r["unresolved"] = [] if variant == "pending-no-gap" else ["Whether source naming is required to pass"]
                rubric_path.write_text("".join(json.dumps(r) + "\n" for r in rubrics))
            if variant == "pending-rubric" and position == 3:
                rubric_path = work / "dataset/rubric.jsonl"
                r = dict(run.read_rows(rubric_path)[-1])
                r.update(version=2, passing_answer="yes", status="confirmed", source_id="u4",
                         quote=CASES[name]["turns"][3]["text"], origin_source_id="u3", unresolved=[])
                append(rubric_path, r)
            if variant == "provisional-summary":
                r = run.row(CASES[name], "s1", "uncertain")
                r["unresolved"] = ["Summary only; missing original expert words, input, output, and criterion"]
                rows = [r]
            if variant == "correcting-turn-source" and position >= 3:
                rows[-1]["source_id"] = "u4"
                rows[-1]["quote"] = CASES[name]["turns"][3]["text"]
            if variant == "criterion-without-replacement" and position == 3:
                rows[-1]["unresolved"] = []
                rows[-1]["replay_ready"] = True
                rows[-1]["rubric_answers"] = [{"rubric_id": "source-named", "version": 1,
                                              "applicable": True, "answer": "no", "source_id": "u4"}]
            path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        result = exercise(name, root / variant, mutate)
        run.dump(root / variant / "result.json", result)
        summary.append({"case": variant, "passed": result["artifact_checks_passed"] is expected_pass})
    run.dump(root / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    raise SystemExit(0 if all(r["passed"] for r in summary) else 1)


if __name__ == "__main__":
    main()
