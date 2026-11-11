"""Local staged Expert Mode/Distill Me exercise; no network or provider calls.

Run stages in order. Retrying merge evidence is idempotent by assertion identity.
Native runs use evaluate.py, never this script as a replacement evaluator.
"""
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WS = ROOT.parents[1]
SESSION = "scripted-review-session:short-capture"
SOURCE = "source/review-session.md"
SOURCE_HASH = hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest()
UT = lambda: datetime.now(timezone.utc).isoformat()
STATEMENTS = {}
for line in (ROOT / SOURCE).read_text().splitlines():
    if line[:1].isdigit():
        number, text = line.split(". ", 1)
        role, quote = text.split(": ", 1)
        STATEMENTS[int(number)] = (role, quote.strip("“”"))


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def rows(name):
    path = ROOT / name
    return [json.loads(x) for x in path.read_text().splitlines() if x] if path.exists() else []


def append(name, value):
    with (ROOT / name).open("a") as f:
        f.write(json.dumps(value, sort_keys=True) + "\n")


def source(number):
    role, quote = STATEMENTS[number]
    return {"path": SOURCE, "sha256": SOURCE_HASH, "statement_number": number,
            "role": role, "verbatim": quote,
            "authority": "synthetic scripted role; not live expert or current-user endorsement"}


def record(rid, number, assertion, example="narrative-howto", **extra):
    return {"schema_version": 1, "record_id": rid, "example_id": example,
            "session_id": SESSION, "captured_at": UT(), "judgment_time": None,
            "source": source(number), "assertion": assertion,
            "identity": [SOURCE_HASH, number, None, assertion],
            "reviewed_input": None, "original_reviewed_output": None,
            "reviewed_output_version": None,
            "input_description": "VPN setup guide" if example == "narrative-howto" else None,
            "execution_association": None,
            "replay_ready": False,
            "replay_blockers": ["Narrative supplies no exact input/state or original reviewed output/version",
                                "Native dev-howto input differs; no evidence reviewer saw that run"],
            **extra}


def criterion(cid, number, question, passing, applicability, **extra):
    return {"criterion_id": cid, "version": 1, "revises": None,
            "source": source(number), "question": question,
            "passing_answer": passing, "applicability": applicability,
            "threshold": None, "normalization": "faithful binary normalization of scripted statement",
            "authority": "scripted fixture only", **extra}


def add_unique(name, entries, key):
    existing = rows(name)
    seen = {json.dumps(x.get(key, ["prior-local", x.get("record_id")]), sort_keys=True) for x in existing}
    added = []
    for entry in entries:
        identity = json.dumps(entry[key], sort_keys=True)
        if identity not in seen:
            append(name, entry)
            seen.add(identity)
            added.append(entry.get("record_id", entry.get("criterion_id")))
    return added


def checkpoint(name):
    dst = ROOT / "checkpoints" / name
    dst.mkdir(parents=True, exist_ok=False)
    for filename in ("reviews.jsonl", "rubric.jsonl", "excluded-proposals.jsonl", "mode.json", "events.jsonl"):
        shutil.copy2(ROOT / filename, dst / filename)
    save(dst / "contents.json", {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in dst.iterdir() if p.is_file()})


def capture():
    if (ROOT / "reviews.jsonl").exists():
        raise SystemExit("capture already exists; preserve initial checkpoint")
    append("events.jsonl", {"event": "explicit Expert Mode activation", "captured_at": UT(),
                            "authorization": "controlled task requests Expert Mode on supplied synthetic source"})
    save(ROOT / "mode.json", {"active": True, "session_id": SESSION,
                              "source_scope": [SOURCE], "unsaved_entries": []})
    append("reviews.jsonl", {"record_id": "prior-unrelated-local-annotation", "example_id": "unrelated-local",
                            "session_id": SESSION, "captured_at": UT(), "kind": "local note",
                            "text": "Seeded unrelated local annotation: preserve this record during merges.",
                            "authority": "exercise setup; no expert judgment", "judgment": None})
    append("reviews.jsonl", record("howto-negative-v1", 2, "howto-ticket-error",
        kind="explicit negative with partial correction", capture_mode="expert-mode",
        judgment={"label": "incorrect", "scope": "scripted narrative how-to item only"},
        correction={"behavior": "Give guidance and leave existing tickets unchanged.", "source_statement": 2,
                    "canonical_replacement_output": None},
        rubric_answers=[{"criterion_id": "howto-guidance-and-no-ticket-change", "version": 1,
                         "applicability": True, "answer": False,
                         "basis": "Narrative agent says ticket opened; reviewer explicitly rejects it.",
                         "native_case_answer": None}]))
    append("reviews.jsonl", record("urgency-unresolved-v1", 6, "urgency-policy-undecided",
        example="urgency-policy", kind="uncertain policy", capture_mode="expert-mode", judgment=None,
        correction=None, unresolved=["No urgency policy, threshold, bypass condition, or passing direction decided."],
        rubric_answers=[{"criterion_id": "urgency-policy", "version": 1,
                         "applicability": "unresolved", "answer": None}]))
    append("rubric.jsonl", criterion("howto-guidance-and-no-ticket-change", 2,
        "For this VPN how-to request, does the assistant give guidance and leave existing tickets unchanged?",
        True, "VPN setup guide how-to request in scripted narrative",
        status="source-backed", exceptions="No rule for all VPN problems is implied.", alternatives=None))
    append("rubric.jsonl", criterion("urgency-policy", 6,
        "Should an urgent request bypass clarification?", None, "Unresolved",
        status="proposed-unresolved", normalization="agent-proposed question, not a confirmed rule",
        exceptions=None, alternatives=None))
    (ROOT / "excluded-proposals.jsonl").touch()
    trace = json.loads((ROOT / "native/baseline/traces.jsonl").read_text())
    save(ROOT / "native-versions.json", {"baseline": {
        "native_receipt": "native/baseline/manifest.json", "trace": "native/baseline/traces.jsonl",
        "case": trace["id"], "input": trace["input"], "original_output": trace["output"],
        "source": "native/baseline/candidate.py", "grade": "FAIL",
        "review_authority": "native deterministic grader; inspected by current agent",
        "scripted_reviewer_judgment": None, "narrative_association": "unproven; different request wording"}})
    append("events.jsonl", {"event": "Expert Mode captured supported statements 2 and 6", "captured_at": UT()})
    checkpoint("first")


def stop():
    mode = json.loads((ROOT / "mode.json").read_text())
    mode["active"] = False
    mode["stopped_at"] = UT()
    save(ROOT / "mode.json", mode)
    append("events.jsonl", {"event": "explicit stop of ongoing Expert Mode capture", "captured_at": UT()})
    checkpoint("stopped")


def merge(name):
    before_mode = (ROOT / "mode.json").read_bytes()
    assert json.loads(before_mode)["active"] is False
    additions = [record("howto-scope-amendment-v1", 4, "ticket-rule-scope-clarification",
        kind="linked scope amendment", capture_mode="distill-me", amends="howto-negative-v1",
        judgment=None, correction={"scope": "Does not generalize to every VPN problem.",
            "explicit_rule": "An explicit ticket request for a clear account should create a ticket unless an open VPN ticket already exists for that account."},
        rubric_answers=[{"criterion_id": "explicit-ticket-and-account-duplicate", "version": 1,
                         "applicability": None, "answer": None,
                         "reason": "No actual reviewed ticket-request item/state provided."}]),
        record("account-scope-rule-v1", 7, "unrelated-account-does-not-block",
        example="account-duplicate-policy", kind="explicit general rule", capture_mode="distill-me",
        judgment=None, correction={"behavior": "An unrelated account's ticket must not block the requested new ticket."},
        rubric_answers=[{"criterion_id": "unrelated-account-no-block", "version": 1,
                         "applicability": None, "answer": None,
                         "reason": "Rule stated; no exact reviewed example provided."}])]
    rubric_additions = [criterion("explicit-ticket-and-account-duplicate", 4,
        "For an explicit VPN ticket request with a clear account, is a ticket created unless an open VPN ticket already exists for that account?",
        True, "Explicit VPN ticket request; clear account", status="source-backed",
        exceptions="An open VPN ticket already exists for that same account.", alternatives=None),
        criterion("unrelated-account-no-block", 7,
        "For an account-specific duplicate check, does an unrelated account's ticket leave the requested new ticket unblocked?",
        True, "Account-specific duplicate check on a requested new ticket", status="source-backed",
        exceptions=None, alternatives=None)]
    proposals = [{"record_id": f"excluded-agent-{n}", "source": source(n),
                  "identity": [SOURCE_HASH, n, "agent-proposal"], "status": status,
                  "expected_behavior": None, "expert_endorsement": False}
                 for n, status in ((3, "rejected generalization; reviewer statement 4"),
                                   (5, "unendorsed agent urgency suggestion; reviewer statement 6 unresolved"))]
    result = {"reviews_added": add_unique("reviews.jsonl", additions, "identity"),
              "rubric_added": add_unique("rubric.jsonl", rubric_additions, "criterion_id"),
              "excluded_added": add_unique("excluded-proposals.jsonl", proposals, "identity")}
    assert before_mode == (ROOT / "mode.json").read_bytes()
    append("events.jsonl", {"event": "explicit Distill Me pass", "checkpoint": name,
                            "captured_at": UT(), "capture_mode_before_and_after": False,
                            "authorized_source": SOURCE, "merge_result": result})
    save(ROOT / f"{name}-result.json", result)
    checkpoint(name)
    print(json.dumps(result, indent=2))


def verify():
    for name in ("reviews.jsonl", "rubric.jsonl", "excluded-proposals.jsonl"):
        a = ROOT / "checkpoints/merge1" / name
        b = ROOT / "checkpoints/merge2" / name
        assert a.read_bytes() == b.read_bytes(), name
        parsed = rows(name)
        key = "record_id" if name != "rubric.jsonl" else "criterion_id"
        assert len({r[key] for r in parsed}) == len(parsed)
    reviews = rows("reviews.jsonl")
    assert any(r["record_id"] == "prior-unrelated-local-annotation" for r in reviews)
    assert any(r.get("amends") == "howto-negative-v1" for r in reviews)
    assert json.loads((ROOT / "mode.json").read_text())["active"] is False
    used = sum(json.loads(p.read_text())["executed_count"] for p in (ROOT / "native").glob("*/summary.json"))
    assert used == 2
    baseline = json.loads((ROOT / "native/baseline/traces.jsonl").read_text())
    regenerated = json.loads((ROOT / "native/regenerated/traces.jsonl").read_text())
    assert baseline["input"] == regenerated["input"]
    assert baseline["output"]["action"] == "create_ticket"
    assert regenerated["output"]["action"] == "guidance"
    assert regenerated["output"]["state"] == regenerated["input"]["state"]
    assert (WS / "support_agent.py").read_bytes() == (ROOT / "native/baseline/candidate.py").read_bytes()
    versions = json.loads((ROOT / "native-versions.json").read_text())
    if "regenerated" in versions:
        assert versions["regenerated"]["inherited_judgment"] is None
        assert versions["regenerated"]["scripted_reviewer_judgment"] is None
    assert all(r.get("execution_association") is None for r in reviews)
    print(json.dumps({"verified": True, "native_case_executions": used,
                      "second_merge_duplicate_additions": 0, "capture_active": False}))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("stage", choices=["capture", "stop", "merge1", "merge2", "verify"])
    stage = p.parse_args().stage
    if stage.startswith("merge"):
        merge(stage)
    else:
        globals()[stage]()
