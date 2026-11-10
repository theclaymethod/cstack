"""Local deterministic capture/merge driver; never executes native cases."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SESSION = "short-capture-scripted-exercise"
SOURCE = HERE / "source.md"
SOURCE_HASH = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
QUOTES = {
    2: "For that how-to request, opening a ticket is wrong. Give guidance and leave existing tickets unchanged.",
    3: "Then every VPN problem should get guidance only.",
    4: "That does not follow. An explicit ticket request for a clear account should create a ticket unless an open VPN ticket already exists for that account.",
    5: "I suggest urgent requests should always bypass clarification.",
    6: "I have not decided the urgency policy.",
    7: "For an account-specific duplicate check, an unrelated account's ticket must not block the requested new ticket.",
}


def ref(n):
    assert QUOTES[n] in SOURCE.read_text()
    return {"path": "source.md", "sha256": SOURCE_HASH, "statement": n,
            "wording": QUOTES[n], "speaker": "agent" if n in (3, 5) else "scripted-reviewer",
            "source_timestamp": None, "message_id": None}


def review(rid, eid, refs, mode, **extra):
    row = {"record_id": rid, "example_id": eid, "session_id": SESSION,
           "authority": "scripted synthetic observation; no real expert endorsement",
           "capture_mode": mode, "sources": [ref(n) for n in refs],
           "reviewed_input": None, "reviewed_output": None,
           "reviewed_output_version": None, "expert_label": None,
           "rubric_answers": [], "amends": None,
           "replay_ready": False,
           "replay_blockers": ["exact original reviewed input/output/version absent from narrative"],
           "judgment_time": None}
    row.update(extra)
    return row


def criterion(rid, cid, version, refs, question, passing, applies, **extra):
    row = {"record_id": rid, "criterion_id": cid, "version": version,
           "session_id": SESSION, "sources": [ref(n) for n in refs],
           "authority": "faithful binary normalization of scripted source; not human approved",
           "question": question, "passing_answer": passing,
           "applicability": applies, "status": "source-backed-synthetic",
           "revises": None}
    row.update(extra)
    return row


def first_rows():
    seed = {"record_id": "prior-local-note", "example_id": "prior-unrelated-format",
            "session_id": "prior-synthetic-seed", "kind": "local-annotation",
            "annotation": "Unrelated local note: prefer a short summary in a demo report.",
            "authority": "task-authored seed; no expert label", "expert_label": None,
            "replay_ready": False, "sources": [], "amends": None}
    scoped = review("howto-negative-v1", "scripted-howto-output", [2], "expert-mode",
                    kind="correctness", scripted_label="incorrect",
                    reviewed_input={"known_description": "VPN setup guide", "exact_payload": None},
                    reviewed_output={"known_description": "assistant reports that it opened a ticket", "exact_output": None},
                    correction={"action": "guidance", "tickets": "unchanged", "scope": "that how-to request", "source": ref(2)},
                    interpretation="A scoped negative; no rule about every VPN problem.",
                    rubric_answers=[{"criterion_id": "howto-no-ticket", "version": 1, "answer": False,
                                     "applicability": "scripted how-to output only", "source": ref(2)}],
                    related_native_evidence={"path": "native-baseline/traces.jsonl", "association": "analogous only; different request text; no exact reviewed-output association"})
    urgency = review("urgency-pending-v1", "urgency-policy", [6], "expert-mode",
                     kind="uncertainty", scripted_label=None,
                     unresolved=["When, if ever, may urgency bypass account clarification?"],
                     correction=None, interpretation="Undecided policy; no urgency threshold supplied.")
    rules = [criterion("rubric-howto-v1", "howto-no-ticket", 1, [2],
                       "For the stated how-to request, does the response give guidance and leave existing tickets unchanged?",
                       True, "The reviewed how-to request; no claim about explicit ticket requests."),
             criterion("rubric-urgency-v1", "urgency-bypass", 1, [6],
                       "May urgency bypass account clarification?", None,
                       None, status="proposed-unresolved", authority="agent formulation of explicitly unresolved scripted policy",
                       unresolved=["passing answer, scope, conditions and urgency threshold are unknown"])]
    return [seed, scoped, urgency], rules


def merge_rows():
    # Re-extract the same supported rows, then add the later clarification as an amendment.
    reviews, rules = first_rows()
    reviews = reviews[1:]
    reviews += [review("howto-scope-amendment-v2", "scripted-howto-output", [3, 4], "distill-me",
                       amends="howto-negative-v1", kind="scope-clarification",
                       scripted_label=None,
                       interpretation="Retain source 2's negative; reject the agent's every-VPN guidance generalization.",
                       original_label_retained=True, correction=None,
                       excluded_proposals=[{"source": ref(3), "endorsed": False}]),
                review("explicit-ticket-rule-v1", "explicit-ticket-policy", [4], "distill-me",
                       kind="general-rule", scripted_label=None, correction=None,
                       interpretation="Clear-account explicit ticket requests create unless that account has an open VPN ticket; no individual execution was judged.",
                       unresolved=["No exact request, state or output supplied for this policy example."]),
                review("duplicate-scope-amendment-v2", "explicit-ticket-policy", [7], "distill-me",
                       amends="explicit-ticket-rule-v1", kind="scope-clarification", scripted_label=None,
                       interpretation="An unrelated account's ticket cannot block creation for the requested account.",
                       correction=None),
                review("urgency-proposal-exclusion", "urgency-policy", [5, 6], "distill-me",
                       amends="urgency-pending-v1", kind="excluded-agent-proposal", scripted_label=None,
                       correction=None, excluded_proposals=[{"source": ref(5), "endorsed": False}],
                       interpretation="Keep pending urgency policy; the agent suggestion is not an expected answer.")]
    rules += [criterion("rubric-ticket-v1", "explicit-ticket-creation", 1, [4],
                        "For an explicit ticket request with a clear account and no open VPN ticket for that account, is a ticket created?",
                        True, "Explicit ticket request; clear account; no same-account open VPN ticket."),
              criterion("rubric-ticket-v2", "explicit-ticket-creation", 2, [4, 7],
                        "For an explicit ticket request with a clear account and no open VPN ticket for that account, is a ticket created even when an unrelated account has a ticket?",
                        True, "Explicit ticket request; clear account; no same-account open VPN ticket. Unrelated account tickets do not block.",
                        revises="rubric-ticket-v1"),
              criterion("rubric-same-account-duplicate-v1", "same-account-duplicate", 1, [4],
                        "When the clear requested account already has an open VPN ticket, does the response avoid creating a duplicate?",
                        True, "Explicit ticket request for an account with its own open VPN ticket."),
              criterion("rubric-unrelated-account-v1", "unrelated-account-not-blocker", 1, [7],
                        "Does an unrelated account's ticket block the requested account's new ticket solely because it exists?",
                        False, "Account-specific duplicate check; other creation preconditions must hold.")]
    return reviews, rules


def read(name):
    path = HERE / name
    return [json.loads(line) for line in path.read_text().splitlines() if line] if path.exists() else []


def write(name, rows):
    path = HERE / name
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    assert [json.loads(line) for line in path.read_text().splitlines()] == rows


def merge(existing, candidates):
    by_id = {row["record_id"]: row for row in existing}
    added = []
    for row in candidates:
        if row["record_id"] in by_id:
            # Capture provenance/times belong to the original saved observation.
            comparable = {k: v for k, v in by_id[row["record_id"]].items() if k != "captured_at"}
            assert comparable == row, "Same identity with changed assertion; require an amendment"
            continue
        row["captured_at"] = datetime.now(timezone.utc).isoformat()
        by_id[row["record_id"]] = row
        added.append(row["record_id"])
    return list(by_id.values()), added


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["first", "merge1", "merge2"])
    args = parser.parse_args()
    snap = HERE / args.stage
    assert not snap.exists(), "checkpoint exists; preserve original evidence"
    if args.stage == "first":
        assert not (HERE / "reviews.jsonl").exists()
        candidates = first_rows()
        existing = ([], [])
        capture_state = "active"
    else:
        existing = (read("reviews.jsonl"), read("rubric.jsonl"))
        assert existing[0] and existing[1]
        candidates = merge_rows()
        capture_state = "inactive"
    reviews, ra = merge(existing[0], candidates[0])
    rules, ca = merge(existing[1], candidates[1])
    assert len({row["record_id"] for row in reviews + rules}) == len(reviews + rules)
    assert reviews[0]["record_id"] == "prior-local-note"
    if args.stage == "merge2":
        assert not ra and not ca, "unchanged source must add no duplicates"
        assert reviews == existing[0] and rules == existing[1]
    write("reviews.jsonl", reviews)
    write("rubric.jsonl", rules)
    state = {"session_id": SESSION, "ongoing_capture": capture_state,
             "unsaved_entries": [], "pending_questions": ["urgency policy", "original reviewed input/output/version association"],
             "last_operation": "expert-mode" if args.stage == "first" else "distill-me",
             "source_hash": SOURCE_HASH}
    (HERE / "state.json").write_text(json.dumps(state, indent=2) + "\n")
    snap.mkdir()
    for name in ("reviews.jsonl", "rubric.jsonl", "state.json"):
        (snap / name).write_bytes((HERE / name).read_bytes())
    receipt = {"stage": args.stage, "review_records_added": ra, "criterion_records_added": ca,
               "review_count": len(reviews), "rubric_count": len(rules),
               "ongoing_capture": capture_state, "native_cases_executed": 0}
    (snap / "merge-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
