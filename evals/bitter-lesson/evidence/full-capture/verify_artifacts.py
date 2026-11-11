"""Verify the actual capture artifacts; no case execution or test fixtures."""
import hashlib
import json
from pathlib import Path

base=Path(__file__).resolve().parent
workspace=base.parent.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]

checks={}
for name in ("reviews.jsonl","rubric.jsonl","exclusions.jsonl"):
    records=rows(base/name)
    assert len(records)==len({r["identity_key"] for r in records})
    checks[name+":rows"]=len(records)
    checks[name+":unique_identities"]=True
assert checks["reviews.jsonl:rows"]==7
assert checks["rubric.jsonl:rows"]==6
assert checks["exclusions.jsonl:rows"]==2
source=(base/"source/review-session.md").read_text()
def verify_source(value):
    if isinstance(value,dict):
        if value.get("path")=="source/review-session.md":
            assert value["sha256"]==sha(base/value["path"])
            assert value["quote"] in source.splitlines()[value["line"]-1]
        for child in value.values():
            verify_source(child)
    elif isinstance(value,list):
        for child in value:
            verify_source(child)
for name in ("reviews.jsonl","rubric.jsonl","exclusions.jsonl"):
    verify_source(rows(base/name))
checks["exact_quotations_and_source_hashes"]=True
amendments=rows(base/"source-role-amendments.jsonl")
assert len(amendments)==1 and amendments[0]["changes_to_labels_or_expectations"] is False
assert amendments[0]["source_sha256"]==sha(base/"source/review-session.md")
assert {r["statement"] for r in amendments[0]["amends"]}=={1,3,5}
assert "agent role" in amendments[0]["corrected_authority"]
checks["source_role_metadata_amendment_verified"]=True
for stage in ("first","stopped","regenerated","merge1","merge2"):
    path=base/"snapshots"/stage
    receipt=json.loads((path/"checkpoint.json").read_text())
    for name,digest in receipt["files"].items():
        assert sha(path/name)==digest
    assert rows(path/"reviews.jsonl")[0]==json.loads((base/"prior-seed.json").read_text())
checks["all_checkpoints_and_prior_seed_verified"]=True
assert json.loads((base/"snapshots/first/capture-state.json").read_text())["active"]
assert not json.loads((base/"capture-state.json").read_text())["active"]
for name in ("reviews.jsonl","rubric.jsonl"):
    assert (base/"snapshots/merge1"/name).read_bytes()==(base/"snapshots/merge2"/name).read_bytes()
    assert (base/name).read_bytes()==(base/"snapshots/merge2"/name).read_bytes()
checks["merge2_zero_additions_and_byte_identical"]=True
original=rows(base/"native/original/traces.jsonl")[0]
regenerated=rows(base/"native/regenerated/traces.jsonl")[0]
assert original["input"]==regenerated["input"]
assert original["outcome"]=="FAIL" and regenerated["outcome"]=="PASS"
assert regenerated["output"]["state"]==regenerated["input"]["state"]
reviews={r["record_id"]:r for r in rows(base/"reviews.jsonl")}
assert reviews["native-regenerated-observation"]["judgment"]["label"] is None
assert reviews["native-original-observation"]["judgment"]["label"] is None
assert reviews["howto-scope-amendment-v2"]["amends"]=="howto-negative-v1"
checks["native_versions_and_judgment_separation"]=True
attempts=0
for stage in ("original","regenerated"):
    path=base/"native"/stage
    manifest=json.loads((path/"manifest.json").read_text())
    summary=json.loads((path/"summary.json").read_text())
    assert sha(path/"candidate.py")==manifest["candidate_hash"]
    for name,digest in manifest["identity"]["files"].items():
        assert sha(workspace/name)==digest
    attempts+=summary["executed_count"]
assert sha(workspace/"support_agent.py")==sha(base/"native/original/candidate.py")
assert attempts==2
checks.update(actual_native_case_executions=attempts,budget=48,remaining=46,
              core_files_unchanged=True,capture_active=False)
(base/"verification.json").write_text(json.dumps(checks,indent=2,sort_keys=True)+"\n")
print(json.dumps(checks,indent=2,sort_keys=True))
