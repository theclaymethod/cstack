Environment/lifecycle lane, one bounded round, two concrete attempts. No lifecycle inconsistency was reproduced in the exercised paths. This is a clean result for these two hypotheses, not an overall Create Eval pass.

Original target: C Stack Create Eval v0.3.0, commit `a7fc7cf2cc2716e474143b7e85bfbda6d1ef2d62`. The trusted frozen reviewer SHA-256 was checked before both runs: `9abd20fcf096b8895c7d66dd8d76009ba2c12e5d7881b737e596af0a4e65ed41`.

The candidate had the host account's actual filesystem and localhost access. Write ownership was instructional, not OS containment. All writes were confined to this lane; no canonical files, source data, frozen files, other lanes, external services, or untrusted candidate programs were modified or executed. The reviewed inline Python imported the trusted frozen reviewer, launched its real `ReviewServer` on loopback in a thread, and exercised its HTTP handler. CLI launch behavior and browser rendering were not exercised. Python bytecode generation was disabled. Every launched server was shut down in a finally block.

The evidence was the existing synthetic, handwritten projection at `eval-runs/trace-review-20261106T184157/traces.jsonl`. Labels, names, a proposed correction, and proposed rubric question used below are explicitly synthetic lifecycle controls. They are not expert labels, clinical truth, product-execution evidence, or an eval dataset. The changed-output action perturbed only a lane-local copy of that existing trace.

The independently desired lifecycle behavior was established from the frozen trace-review contract before execution: join reviews by trace ID and canonical hash; never transfer an old verdict to a changed trace; preserve separate reviewer disagreements; use the latest amendment per stable review ID; retain earlier records and correction provenance; reject a stale amendment; and resume the same current state after restart. A latest-event API alone is not expected to expose all history, because the guidance explicitly directs the coding agent to read both JSONL files.

Attempt 1 tried to carry an old review into a changed trace version after restart.

- Legitimate baseline: pristine input and no reviews returned HTTP 200. Saving the original synthetic diagnostic FAIL returned HTTP 200. An unchanged restart returned the same matching review.
- Minimal perturbation: change only the copied output probability from 0.9 to 0.91, then restart with the same review file.
- Observed response: the old event remained in the raw API history projection, but the documented ID-and-hash join (also the source UI predicate) yielded zero matching reviews. Posting the old hash returned HTTP 400, `Trace changed or is outside this review snapshot`. Posting the existing review ID with the new hash returned HTTP 400, `An existing review cannot be reassigned to another trace version`.
- A distinct new review ID for the changed trace returned HTTP 200 and appended a separate observation. It did not amend or transfer the old verdict.
- Reset evidence: restoring byte-identical original trace bytes and restarting yielded only the original matching review. The changed-version observation remained separate history. Two durable JSONL events remained. The external source file's SHA-256 was identical before/after.
- Result: failed attack. No violated requirement was observed.

Exact requests, responses, hashes, current-state joins, and persisted events are in [attempt-1.json](attempt-1.json); the review history is [attempt-1-reviews.jsonl](attempt-1-reviews.jsonl).

Attempt 2 tried to collapse reviewer disagreement or leave a superseded negative in current state after amendments and restart.

- Legitimate baseline: pristine copied input and no review file returned zero observations. Saving A's synthetic FAIL with a proposed correction/question and independent B's PASS on the same scope each returned HTTP 200. Both observations remained current.
- Minimal actions: amend A's observation from FAIL to DEFER, then submit an edit still amending A's original record.
- Observed response: A's amendment returned HTTP 200 and appended a third history event. The stale save returned HTTP 409, `Review changed in another tab; reload before saving`, without changing disk.
- Persisted state: the original file prefix remained byte-for-byte intact. The original event retained A's correction and supplied reviewer; the new event linked it through `amends`. The proposed rubric remained explicitly proposed. No conversion to expert gold occurred.
- Restart evidence: unchanged paths yielded exactly two latest observations, A=DEFER and B=PASS. The earlier A=FAIL remained history rather than another current case. The before/after-restart current records were equal. The copied and external source trace bytes remained unchanged.
- Result: failed attack. No violated requirement was observed.

Exact requests, responses, and persisted events are in [attempt-2.json](attempt-2.json); the review history is [attempt-2-reviews.jsonl](attempt-2-reviews.jsonl).

Limitations: these observations establish the real HTTP and persistence behavior for the two paths only. Current GET exposes latest events, so an importer that ignores the documented JSONL history could miss earlier correction provenance. The helper stores trace and snapshot hashes rather than an archival copy of the source snapshot; this run retained the original input and did not reproduce irreversible loss. Those are explicit limits of this audit, not demonstrated workflow violations. Reviewer names remain self-reported, as documented. UI rendering, reviewer authority, semantic label quality, end-to-end eval authoring, and general skill effectiveness were not measured. There is no full authoring-skill grader, and HTTP acceptance gives no full-skill credit.

The exact inline commands executed follow. They include checks, controls, reset, transcript capture, and cleanup; they are recorded as report text, with no runner, test helper, or test fixture file added.

```bash
python3 - <<'PY'
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, threading, urllib.request, urllib.error
from pathlib import Path
from contextlib import contextmanager

lane = Path("eval-runs/create-eval-cross-examine-v03/environment")
lane.mkdir(parents=True, exist_ok=True)
frozen = lane.parent / "frozen/skills/create-eval/scripts/review_traces.py"
assert hashlib.sha256(frozen.read_bytes()).hexdigest() == "9abd20fcf096b8895c7d66dd8d76009ba2c12e5d7881b737e596af0a4e65ed41"
spec = importlib.util.spec_from_file_location("frozen_reviewer_environment", frozen)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source = Path("eval-runs/trace-review-20261106T184157/traces.jsonl")
original = source.read_bytes()
traces = lane / "attempt-1-traces.jsonl"
reviews = lane / "attempt-1-reviews.jsonl"
assert not traces.exists() and not reviews.exists()
traces.write_bytes(original)
log = {"hypothesis": "An old review can become current for a changed trace across restart.", "steps": []}

@contextmanager
def launch():
    server = module.ReviewServer(("127.0.0.1", 0), traces, reviews, "Lifecycle control")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    def request(path="/api/data", body=None):
        payload = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request("http://127.0.0.1:" + str(server.server_port) + path,
            data=payload, headers={"Authorization": "Bearer " + server.token, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return {"status": response.status, "body": json.load(response)}
        except urllib.error.HTTPError as error:
            return {"status": error.code, "body": json.load(error)}
    try:
        yield request
    finally:
        server.shutdown()
        thread.join()
        server.server_close()

def visible(data):
    return [review for review in data["reviews"] if any(
        review["trace_id"] == row["trace"]["id"] and review["trace_sha256"] == row["sha256"]
        for row in data["rows"])]

with launch() as request:
    first = request()
    log["steps"].append({"action": "GET unchanged original; legitimate baseline", "response": first})
    row = first["body"]["rows"][0]
    body = {"trace_id": row["trace"]["id"], "trace_sha256": row["sha256"],
        "review_id": "environment-version-control", "amends": None,
        "reviewer": "Synthetic lifecycle reviewer", "scope": "Synthetic lifecycle control only",
        "verdict": "FAIL", "notes": "Diagnostic label for persistence; not an expert or domain judgment.",
        "correction": "", "rubric_questions": []}
    saved = request("/api/reviews", body)
    log["steps"].append({"action": "POST original review; legitimate save", "request": body, "response": saved})

with launch() as request:
    resumed = request()
    log["steps"].append({"action": "Restart unchanged paths", "response": resumed,
        "matching_review_count": len(visible(resumed["body"]))})

changed = json.loads(original.decode().strip())
changed["output"]["probability"] = 0.91
traces.write_text(json.dumps(changed) + "\n")
with launch() as request:
    changed_data = request()
    log["steps"].append({"action": "Restart after changing only synthetic probability 0.9 to 0.91",
        "response": changed_data, "matching_review_count": len(visible(changed_data["body"]))})
    old_request = dict(body, amends=saved["body"]["record_id"])
    stale = request("/api/reviews", old_request)
    log["steps"].append({"action": "POST old trace hash on changed snapshot", "request": old_request, "response": stale})
    reassigned = dict(old_request, trace_sha256=changed_data["body"]["rows"][0]["sha256"])
    refused = request("/api/reviews", reassigned)
    log["steps"].append({"action": "POST existing review ID with new trace hash", "request": reassigned, "response": refused})
    new_body = dict(reassigned, review_id="environment-new-version", amends=None, verdict="UNREVIEWED",
        notes="Separate observation of changed synthetic output; no transferred label.")
    new_saved = request("/api/reviews", new_body)
    log["steps"].append({"action": "POST distinct observation on changed trace", "request": new_body, "response": new_saved})

traces.write_bytes(original)
with launch() as request:
    restored = request()
    log["steps"].append({"action": "Restore byte-identical original and restart", "response": restored,
        "matching_review_count": len(visible(restored["body"]))})
history = module.read_jsonl(reviews)
log.update({
    "original_source_sha256_before": hashlib.sha256(original).hexdigest(),
    "original_source_sha256_after": hashlib.sha256(source.read_bytes()).hexdigest(),
    "scratch_reset_byte_identical": traces.read_bytes() == original,
    "persisted_history": history,
    "observed": {
        "legitimate_save_status": saved["status"],
        "unchanged_restart_matches_original": len(visible(resumed["body"])) == 1,
        "changed_restart_does_not_match_old_review": len(visible(changed_data["body"])) == 0,
        "old_hash_status": stale["status"],
        "reassignment_status": refused["status"],
        "restored_original_matches_old_only": [x["review_id"] for x in visible(restored["body"])] == ["environment-version-control"],
        "history_records": len(history)
    },
    "result": "No bypass reproduced: old label is excluded by the documented trace-ID-and-hash join. Raw API retains historical latest records; UI matching predicate excludes changed versions.",
    "limitations": ["HTTP and persisted JSONL only; no browser render.",
        "The helper stores hashes and annotations, not a durable copy of the original trace snapshot. This run kept and restored the original source, so it does not prove irreversible evidence loss.",
        "Synthetic diagnostic labels establish lifecycle behavior only."]})
(lane / "attempt-1.json").write_text(json.dumps(log, indent=2) + "\n")
print(json.dumps(log["observed"], indent=2))
PY
```

```bash
python3 - <<'PY'
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, threading, urllib.request, urllib.error
from pathlib import Path
from contextlib import contextmanager

lane = Path("eval-runs/create-eval-cross-examine-v03/environment")
frozen = lane.parent / "frozen/skills/create-eval/scripts/review_traces.py"
assert hashlib.sha256(frozen.read_bytes()).hexdigest() == "9abd20fcf096b8895c7d66dd8d76009ba2c12e5d7881b737e596af0a4e65ed41"
spec = importlib.util.spec_from_file_location("frozen_reviewer_environment", frozen)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source = Path("eval-runs/trace-review-20261106T184157/traces.jsonl")
original = source.read_bytes()
traces = lane / "attempt-2-traces.jsonl"
reviews = lane / "attempt-2-reviews.jsonl"
assert not traces.exists() and not reviews.exists()
traces.write_bytes(original)
log = {"hypothesis": "Reviewer disagreement or a superseded negative can collapse into misleading current review state after amendments/restart.", "steps": []}

@contextmanager
def launch():
    server = module.ReviewServer(("127.0.0.1", 0), traces, reviews, "Lifecycle control")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    def request(path="/api/data", body=None):
        payload = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request("http://127.0.0.1:" + str(server.server_port) + path,
            data=payload, headers={"Authorization": "Bearer " + server.token, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return {"status": response.status, "body": json.load(response)}
        except urllib.error.HTTPError as error:
            return {"status": error.code, "body": json.load(error)}
    try:
        yield request
    finally:
        server.shutdown()
        thread.join()
        server.server_close()

with launch() as request:
    initial = request()
    log["steps"].append({"action": "GET pristine review file; legitimate baseline", "response": initial})
    row = initial["body"]["rows"][0]
    a = {"trace_id": row["trace"]["id"], "trace_sha256": row["sha256"],
        "review_id": "environment-reviewer-a", "amends": None,
        "reviewer": "Synthetic Reviewer A", "scope": "Synthetic diagnostic assertion",
        "verdict": "FAIL", "notes": "Synthetic lifecycle control only; no expert or domain judgment.",
        "correction": "Diagnostic proposed correction supplied by synthetic Reviewer A.",
        "rubric_questions": ["Does this synthetic diagnostic assertion meet its task contract?"]}
    first = request("/api/reviews", a)
    prefix = reviews.read_bytes()
    log["steps"].append({"action": "POST Reviewer A FAIL with proposed correction/question", "request": a, "response": first})
    b = dict(a, review_id="environment-reviewer-b", reviewer="Synthetic Reviewer B",
        verdict="PASS", notes="Independent synthetic dissent on the same scope.", correction="", rubric_questions=[])
    second = request("/api/reviews", b)
    log["steps"].append({"action": "POST independent Reviewer B PASS on same scope", "request": b, "response": second})
    dissent = request()
    log["steps"].append({"action": "GET both decided observations", "response": dissent})
    amendment = dict(a, amends=first["body"]["record_id"], verdict="DEFER",
        notes="Withdraw the decided negative pending evidence; correction remains a proposal.")
    amended = request("/api/reviews", amendment)
    log["steps"].append({"action": "POST Reviewer A amendment FAIL to DEFER", "request": amendment, "response": amended})
    before_stale = reviews.read_bytes()
    stale_body = dict(amendment, verdict="FAIL", notes="Stale tab's attempted overwrite.")
    stale = request("/api/reviews", stale_body)
    log["steps"].append({"action": "POST stale amendment from old record", "request": stale_body, "response": stale,
        "disk_unchanged": reviews.read_bytes() == before_stale})
    after = request()
    log["steps"].append({"action": "GET latest state before restart", "response": after})

with launch() as request:
    restarted = request()
    log["steps"].append({"action": "Restart unchanged paths", "response": restarted})
history = module.read_jsonl(reviews)
current = restarted["body"]["reviews"]
current_by_id = {record["review_id"]: record for record in current}
log.update({
    "original_source_sha256_before": hashlib.sha256(original).hexdigest(),
    "original_source_sha256_after": hashlib.sha256(source.read_bytes()).hexdigest(),
    "scratch_trace_unchanged": traces.read_bytes() == original,
    "persisted_history": history,
    "observed": {
        "baseline_review_count": len(initial["body"]["reviews"]),
        "all_legitimate_save_statuses": [first["status"], second["status"], amended["status"]],
        "independent_disagreement_preserved_before_amendment":
            sorted(record["verdict"] for record in dissent["body"]["reviews"]) == ["FAIL", "PASS"],
        "stale_amendment_status": stale["status"],
        "stale_amendment_no_disk_change": before_stale == reviews.read_bytes(),
        "append_only_original_prefix_preserved": reviews.read_bytes().startswith(prefix),
        "history_records": len(history),
        "latest_count_after_restart": len(current),
        "latest_verdicts_after_restart": sorted(record["verdict"] for record in current),
        "amendment_links_original": current_by_id[a["review_id"]]["amends"] == first["body"]["record_id"],
        "original_correction_supplier_in_history": history[0]["reviewer"] == "Synthetic Reviewer A",
        "current_correction_remains_proposed": current_by_id[a["review_id"]]["rubric_status"] == "proposed",
        "deferred_review_has_no_current_fail": current_by_id[a["review_id"]]["verdict"] == "DEFER",
        "restart_preserves_current_records": after["body"]["reviews"] == current
    },
    "result": "No bypass reproduced: separate review IDs preserve dissent; amendment supersedes rather than duplicates the negative; stale writes are rejected; disk retains original provenance and amendment chain.",
    "limitations": ["Current GET returns latest records, not amendment history. Complete provenance inspection requires direct JSONL history, which the guidance explicitly permits.",
        "Reviewer names are self-reported. No reviewer-authority verification, browser rendering, semantic judge, or full authoring-skill grader was exercised.",
        "Synthetic lifecycle labels and corrections do not establish domain truth."]})
(lane / "attempt-2.json").write_text(json.dumps(log, indent=2) + "\n")
print(json.dumps(log["observed"], indent=2))
PY
```
