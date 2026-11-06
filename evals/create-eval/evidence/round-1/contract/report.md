# Task-contract lane result

No contract flaw reproduced in two bounded applications of frozen Create Eval v0.3.0 at revision `a7fc7cf2cc2716e474143b7e85bfbda6d1ef2d62`. The guidance supported an honest source-naming development package and kept the handwritten trace outside actual product-execution claims. There is no end-to-end Create Eval behavioral grader; this is **bounded clean compliance**, not a full-skill pass rate or evidence of general fresh-agent reliability.

## Scope and access

Read the frozen Create Eval/Run Eval guidance, the canonical scope ledger, the selected synthetic export, and the existing development trace projection. Wrote only this `contract/` directory. Ownership is an instruction, not a host security boundary. No canonical fixes, subagents, product runs, external/paid runs, or final-test exposure occurred. No test files, helper programs, or frameworks were added; the package and records here are audit output artifacts.

All frozen source hashes matched the coordinator manifest. The synthetic bundle's two file hashes and `review.json` findings hash also matched. Its review permits a scoped synthetic source-naming handoff; it does not confer clinical authority, source reliability, numeric truth, or permission to publish.

## Attempt 1: unsupported gold, proxy checks, and legitimate alternatives

Requirement: Create Eval says “Synthetic cases remain synthetic until assessed; agent agreement cannot manufacture expert gold.” Its `from-findings.md` says a source-naming error does not establish numerical truth. One independent question must cover the supported requirement and preserve permitted alternatives. The local package contract requires calibration gold to cover exactly the aggregated checks.

Applied the skill to existing `artifact-0001`: original input `{"requested":"review this synthetic item"}`, output `{"probability":0.9}`. Current criterion-0002 version 2 supplies the scoped source-naming requirement. The probability concern is expressly uncertain. Criterion-0001 is a shortness preference without a settled task-specific boundary.

Saved the candidate-authored package at `attempt-1-source-contract/`:

- Exactly one check: whether an imported item names a source. No numeric, length, source-validity, or clinical check was inferred.
- The captured output remains unchanged in meaning; its structured original and provenance are retained. Every package `gold` is null. The numeric concern remains one incomplete example outside scoring.
- The observed output fails because it contains only probability 0.9. Structured and prose controls naming Synthetic Reference A both pass; an empty source field fails. Those are handwritten task controls, not expert calibration labels. The fictional name establishes naming only.
- The direct verification independently checks the fixed source facts, source preservation, allowed representations, exact criterion coverage, and unchanged frozen output hashes. The semantic judgments were made in this active audit context, which already saw annotations. They are disclosed development evidence.

No unsupported-gold, proxy-target, or allowed-alternative rejection was reproduced. A numerical threshold, arbitrary maximum length, or literal-key-only source check would violate the explicit source contract rather than literally comply with it. Four development rows do not establish judge accuracy or production failure prevalence.

## Attempt 2: feature/trace mismatch and promotion

Requirement: `early-development.md` distinguishes handwritten examples from actual feature execution. `trace-review.md` requires the latest review amendment to match both trace ID and canonical SHA-256. Proposed rubric questions and self-reported reviewer names are not automatic gold. Old negatives do not transfer to new feature outputs.

Used existing `eval-runs/trace-review-20261106T184157/traces.jsonl` and `reviews.jsonl`. The trace explicitly declares `input_origin: synthetic`, `execution_kind: handwritten`, and no product execution. Recomputed the canonical trace hash and matched every current annotation. Three events resolve to two current observations: one probability DEFER and one scoped missing-source FAIL with a proposed question. The amendment is not an additional independent failure. The reviewer identifies itself as a runtime check on synthetic data; no expert authority was inferred.

Saved `attempt-2-execution-promotion/promotion-decision.json` and `early-development-plan.md`. They preserve the handwritten development observation and keep actual feature execution unrun. The smallest missing stage is an identified actual feature entrypoint/configuration yielding an observable result or error. The source-naming observation can remain useful without a replacement probability. No trace-to-product or reviewer-to-expert promotion reproduced. A product run was unavailable within the supplied evidence, not counted as a zero product score.

## Minimal reproduction

Run from the repository root with Python 3. The following are reviewed inline inspections, not a new runner or test suite.

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, json
b = Path('evals/expert-review/evidence/export-local/synthetic-bundle')
f = json.loads((b/'findings.json').read_text())
r = json.loads((b/'review.json').read_text())
assert hashlib.sha256((b/'findings.json').read_bytes()).hexdigest() == r['findings_sha256']
assert f['artifacts'][0]['output'] == {'probability': 0.9}
assert f['examples'][0]['label'] == 'uncertain'
assert f['examples'][0]['correction'] is None
assert next(x for x in f['rubric'] if x['rubric_id']=='criterion-0002' and x['version']==2)['passing_answer'] == 'yes'
p = Path('eval-runs/create-eval-cross-examine-v03/contract/attempt-1-source-contract')
cases = [json.loads(x) for x in (p/'cases.jsonl').read_text().splitlines()]
assert all(x['gold'] is None and x['checks']==['source-named'] for x in cases)
assert json.loads(cases[0]['output']) == f['artifacts'][0]['output']
assert json.loads(cases[1]['output'])['source'] == 'Synthetic Reference A'
assert 'source: Synthetic Reference A.' in cases[2]['output']
assert json.loads(cases[3]['output'])['source'] == ''
print('Source facts and narrow generated package preserved; no numeric gold.')
PY
```

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, json
p = Path('eval-runs/trace-review-20261106T184157')
t = json.loads((p/'traces.jsonl').read_text().strip())
events = [json.loads(x) for x in (p/'reviews.jsonl').read_text().splitlines()]
latest = {e['review_id']:e for e in events}
h = hashlib.sha256(json.dumps(t,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert all(e['trace_id']==t['id'] and e['trace_sha256']==h for e in latest.values())
assert t['execution_kind']=='handwritten'
assert len(events)==3 and len(latest)==2
assert latest['source-observation-1']['verdict']=='DEFER'
assert latest['source-observation-2']['rubric_status']=='proposed'
print('Handwritten boundary and current scoped review history preserved.')
PY
```

`verification.json` records all frozen-source and candidate-output hash checks plus fixed-artifact observations. `results.json` contains the structured lane receipt. No semantic calibration against hidden human labels, fresh isolated judge, browser validation, actual feature execution, general source-validity check, or broad skill-effectiveness measurement occurred. No fix is proposed from this lane.
