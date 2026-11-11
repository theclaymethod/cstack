#!/usr/bin/env python3
"""Local record writer/merge driver; does not execute candidates or infer gold.

Run capture, stop, merge1, merge2 in order after the native original run.
Rerun `merge2` to verify unchanged evidence produces no duplicate additions.
Use --base PATH to reproduce records against a copy of the preserved evidence.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil

SESSION = "controlled-full-capture"
DEFAULT = Path(__file__).resolve().parent

def now():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")

def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

def append(path, candidates):
    old = rows(path)
    keys = {r["identity_key"] for r in old}
    added = []
    with path.open("a") as stream:
        for row in candidates:
            if row["identity_key"] in keys:
                continue
            row = dict(row, captured_at=now(), session_id=SESSION)
            stream.write(json.dumps(row, sort_keys=True) + "\n")
            keys.add(row["identity_key"])
            added.append(row["record_id"])
    assert rows(path)[:len(old)] == old
    assert len({r["identity_key"] for r in rows(path)}) == len(rows(path))
    return added

def source(base, statement):
    raw = base / "source/review-session.md"
    line = next((i, line) for i, line in enumerate(raw.read_text().splitlines(), 1)
                if line.startswith(str(statement) + ". "))
    quote = line[1].split("“", 1)[1].rsplit("”", 1)[0]
    role = "agent" if statement in (1, 3, 5) else "reviewer"
    return {"path": "source/review-session.md", "sha256": digest(raw),
            "statement": statement, "line": line[0], "quote": quote,
            "role": role,
            "authority": f"scripted synthetic {role} role; not a real expert or current user",
            "judgment_time": None, "message_id": None}

def key(base, statement, assertion, version="narrative-output-v1"):
    return digest(base / "source/review-session.md") + f":statement-{statement}:{version}:{assertion}"

def judgment(base, statement, record_id, example, assertion, **extra):
    return dict(record_id=record_id, example_id=example, amends=None,
                identity_key=key(base, statement, assertion),
                source=source(base, statement), capture_method="expert-mode",
                original_output_version="narrative-output-v1" if example == "narrative-howto" else None,
                **extra)

def criterion(base, statement, record_id, criterion_id, question, passing_answer, applicability,
              status="source-backed synthetic normalization"):
    return dict(record_id=record_id, criterion_id=criterion_id, version=1, revises=None,
                identity_key=key(base, statement, criterion_id, "rubric-v1"),
                source=source(base, statement), question=question, passing_answer=passing_answer,
                applicability=applicability, status=status, authority="synthetic fixture only")

def initial(base):
    trace = rows(base / "native/original/traces.jsonl")[0]
    native_manifest = json.loads((base / "native/original/manifest.json").read_text())
    reviews = [
        dict(record_id="prior-local-annotation", example_id="prior-local-example",
             identity_key="seed:unrelated-local-annotation:v1", amends=None,
             capture_method="explicit synthetic seed", source={"authority": "task-authorized local seed"},
             judgment={"label": None, "type": "annotation", "wording": "Unrelated prior local annotation; retain verbatim."},
             input=None, original_reviewed_output=None, replay_ready=False,
             replay_blockers=["Seed only, no reviewed example or external authority."]),
        judgment(base, 2, "howto-negative-v1", "narrative-howto", "scoped-negative",
                 judgment={"label": "incorrect", "type": "correctness", "wording": source(base,2)["quote"]},
                 input={"request_text": "VPN setup guide", "complete_payload": None},
                 original_reviewed_output={"reported_behavior": "opened a ticket", "complete_output": None,
                                           "source": source(base,1)},
                 correction={"behavior": "Give guidance and leave existing tickets unchanged.",
                             "scope": "that how-to request", "canonical_replacement": None, "source": source(base,2)},
                 rubric_answers=[{"criterion_id":"howto-guidance", "version":1, "answer":False,
                                  "applicability":"applies to narrative behavior only", "source_statement":2},
                                 {"criterion_id":"howto-preserve-state", "version":1, "answer":None,
                                  "applicability":"unknown exact state", "source_statement":2}],
                 related_native_evidence="native/original/traces.jsonl",
                 output_association="Similar scenario only; no exact association to dev-howto supplied.",
                 replay_ready=False,
                 replay_blockers=["Narrative has no complete input/state or output/version.",
                                  "Native request text differs; reviewer did not explicitly inspect this native receipt."]),
        judgment(base, 6, "urgency-unresolved-v1", "urgency-policy", "unresolved-policy",
                 judgment={"label":None, "type":"uncertain policy", "wording":source(base,6)["quote"]},
                 input=None, original_reviewed_output=None, correction=None, rubric_answers=[],
                 unresolved=["Whether or when urgency bypasses clarification; no urgency threshold supplied."],
                 replay_ready=False, replay_blockers=["Policy undecided; no reviewed output."]),
        dict(record_id="native-original-observation", example_id="native-dev-howto", amends=None,
             identity_key="native:original:"+native_manifest["candidate_hash"]+":dev-howto",
             capture_method="actual native observation", source={"authority":"native deterministic synthetic contract",
             "manifest":"native/original/manifest.json", "trace":"native/original/traces.jsonl"},
             original_output_version=native_manifest["candidate_hash"], input=trace["input"],
             original_reviewed_output=trace["output"], stdout=trace["stdout"],
             judgment={"label":None,"type":"no reviewer assessment", "wording":None},
             native_verdict=trace["outcome"], native_checks=trace["checks"],
             reviewer_association=None, replay_ready=False,
             native_replay_ready=True,
             replay_blockers=["No scripted reviewer statement exactly associated with this executed input/output."])
    ]
    rubric = [
        criterion(base,2,"rubric-howto-guidance-v1","howto-guidance","For that how-to request, did the assistant give guidance instead of opening a ticket?",True,"The cited VPN setup guide how-to request; not every VPN problem."),
        criterion(base,2,"rubric-howto-preserve-v1","howto-preserve-state","For that how-to request, were existing tickets left unchanged?",True,"The cited how-to request; requires original and resulting state to score."),
        criterion(base,6,"rubric-urgency-proposed-v1","urgency-bypass","Should an urgent request bypass account clarification?",None,"Urgency policy, threshold, and exceptions unresolved.","proposed; unresolved")
    ]
    return reviews, rubric

def retrospective(base):
    reviews, rubric = initial(base)
    # Include prior live captures in candidate matching, using the same identities.
    for row in reviews:
        if row["capture_method"] == "expert-mode":
            row["capture_method"] = "distill-me"
    amendment = judgment(base,4,"howto-scope-amendment-v2","narrative-howto","scope-clarification",
        judgment={"label":None,"type":"scope clarification; not a new judged output","wording":source(base,4)["quote"]},
        correction={"behavior":"Explicit ticket request for a clear account creates a ticket unless an open VPN ticket exists for that account.",
                    "scope":"Explicit authorized ticket requests, not how-to questions", "source":source(base,4)},
        rubric_answers=[], replay_ready=False,
        replay_blockers=["Rule has no exact reviewed execution attached; original narrative context remains incomplete."],
        relation="Rejects statement 3's proposed every-VPN guidance generalization; clarifies the boundary without retracting statement 2.")
    amendment["amends"] = "howto-negative-v1"
    amendment["capture_method"] = "distill-me"
    reviews += [amendment,
        judgment(base,7,"account-local-duplicate-rule-v1","account-local-duplicate-rule","explicit-rule",
            judgment={"label":None,"type":"explicit general rule","wording":source(base,7)["quote"]},
            input=None, original_reviewed_output=None,
            correction={"behavior":"An unrelated account's ticket must not block the requested new ticket.","source":source(base,7)},
            rubric_answers=[], replay_ready=False,
            replay_blockers=["No exact input/output/state or item-level label for this rule."])
    ]
    reviews[-1]["capture_method"] = "distill-me"
    rubric += [
        criterion(base,4,"rubric-explicit-ticket-v1","explicit-ticket-creation","For an explicit ticket request with a clear account and no open VPN ticket for that account, did the assistant create a ticket?",True,"Explicit ticket request, clear account; exception: existing open VPN ticket for the same account."),
        criterion(base,4,"rubric-open-duplicate-v1","same-account-open-duplicate","Did an explicit ticket request avoid creating a duplicate when an open VPN ticket already existed for the selected account?",True,"Open VPN ticket for the same account; other tickets are outside this exception."),
        criterion(base,7,"rubric-unrelated-ticket-v1","unrelated-account-not-blocking","Did an unrelated account's ticket avoid blocking the requested new ticket?",True,"Account-specific duplicate check; authorization and account clarity remain conditions from statement 4.")
    ]
    return reviews, rubric

def checkpoint(base, name):
    directory = base / "snapshots" / name
    directory.mkdir(parents=True, exist_ok=False)
    for file in ("reviews.jsonl", "rubric.jsonl", "capture-state.json", "exclusions.jsonl"):
        if (base / file).exists():
            shutil.copyfile(base / file, directory / file)
    save(directory / "checkpoint.json", {"name":name,"saved_at":now(),
          "files":{p.name:digest(p) for p in directory.iterdir() if p.is_file()}})

def run(base, phase):
    base.mkdir(parents=True, exist_ok=True)
    if phase == "capture":
        assert not (base / "capture-state.json").exists(), "capture already initialized"
        reviews, rubric = initial(base)
        # Seed before activation; preserve this exact row in all later checkpoints.
        append(base/"reviews.jsonl", reviews[:1])
        save(base/"prior-seed.json", rows(base/"reviews.jsonl")[0])
        save(base/"capture-state.json", {"session_id":SESSION,"active":True,
             "invocation":"Controlled task explicitly requests Expert Mode", "activated_at":now(),
             "paths":["reviews.jsonl","rubric.jsonl"],"pending_questions":["urgency policy", "exact narrative/native output association"],"unsaved_entries":[]})
        append(base/"reviews.jsonl", reviews[1:])
        append(base/"rubric.jsonl", rubric)
        exclusions = [dict(record_id="exclude-generalization",identity_key=key(base,3,"unendorsed-generalization"),source=source(base,3),
                           reason="Agent-proposed every-VPN guidance rule, explicitly rejected in statement 4; not an expectation."),
                      dict(record_id="exclude-urgency-suggestion",identity_key=key(base,5,"unendorsed-urgency"),source=source(base,5),
                           reason="Agent suggestion; statement 6 explicitly leaves policy undecided; not an expectation.")]
        append(base/"exclusions.jsonl", exclusions)
        checkpoint(base,"first")
    elif phase == "stop":
        state=json.loads((base/"capture-state.json").read_text())
        assert state["active"]
        state.update(active=False, stopped_at=now(), stop_reason="Controlled task explicitly requests stop before Distill Me")
        save(base/"capture-state.json",state)
        checkpoint(base,"stopped")
    elif phase == "regeneration":
        assert json.loads((base/"capture-state.json").read_text())["active"] is False
        original_manifest=json.loads((base/"native/original/manifest.json").read_text())
        manifest=json.loads((base/"native/regenerated/manifest.json").read_text())
        trace=rows(base/"native/regenerated/traces.jsonl")[0]
        original=rows(base/"native/original/traces.jsonl")[0]
        assert trace["input"] == original["input"]
        assert trace["outcome"] == "PASS"
        append(base/"reviews.jsonl", [dict(
            record_id="native-regenerated-observation", example_id="native-dev-howto-regenerated", amends=None,
            identity_key="native:regenerated:"+manifest["candidate_hash"]+":dev-howto",
            capture_method="separately authorized regeneration after capture stopped",
            source={"authority":"agent-authored demonstration assessed by native synthetic contract only",
                    "trace":"native/regenerated/traces.jsonl", "manifest":"native/regenerated/manifest.json"},
            original_output_version=manifest["candidate_hash"], input=trace["input"],
            original_reviewed_output=trace["output"], stdout=trace["stdout"],
            derives_from="native-original-observation", original_version=original_manifest["candidate_hash"],
            judgment={"label":None,"wording":None,"type":"unassessed new version"},
            native_verdict=trace["outcome"], native_checks=trace["checks"],
            reviewer_association=None, rubric_answers=[], canonical_replacement=False,
            replay_ready=False,native_replay_ready=True,
            replay_blockers=["No reviewer assessment of regenerated output; old judgment does not transfer."]
        )])
        checkpoint(base,"regenerated")
    else:
        state=json.loads((base/"capture-state.json").read_text())
        assert state["active"] is False
        reviews, rubric=retrospective(base)
        before={p:digest(base/p) for p in ("reviews.jsonl","rubric.jsonl")}
        added_reviews=append(base/"reviews.jsonl",reviews)
        added_rubric=append(base/"rubric.jsonl",rubric)
        assert json.loads((base/"capture-state.json").read_text()) == state
        assert rows(base/"reviews.jsonl")[0] == json.loads((base/"prior-seed.json").read_text())
        log={"phase":phase,"time":now(),"source_sha256":digest(base/"source/review-session.md"),
             "added_reviews":added_reviews,"added_rubric":added_rubric,
             "before":before,"after":{p:digest(base/p) for p in before},"capture_active":False,
             "matching":"source hash + statement + output version + specific assertion",
             "unknown_matches":[],"source_authority":"scripted synthetic fixture"}
        if phase=="merge2":
            assert not added_reviews and not added_rubric
            assert log["before"] == log["after"]
        path=base/(phase+"-result.json")
        if path.exists():
            assert phase=="merge2"
            path=base/"merge2-repeat-result.json"
        save(path,log)
        if not (base/"snapshots"/phase).exists():
            checkpoint(base,phase)
        print(json.dumps(log,indent=2))

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["capture","stop","regeneration","merge1","merge2"])
    parser.add_argument("--base",type=Path,default=DEFAULT)
    args=parser.parse_args()
    run(args.base.resolve(),args.phase)
