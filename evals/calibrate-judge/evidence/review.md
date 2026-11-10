# Independent calibration review

Reviewed the reference-only skill, all three references, playground adapters/statistics/workflow/backend, and `fixtures/playground/tests/test_judge_calibration.py` against the approved offline-only intent. No provider/network calls, canonical source edits, or broad test-suite reruns. Focused reproductions ran only under `review-scratch/`.

Two concrete defects found in the initial source:

1. **[P2] Malformed typed responses can escape normalization instead of becoming ERROR.** `fixtures/playground/judge_calibration/adapters.py:49` uses `set(probs)` before establishing that probabilities is an object. A valid JSON array `['PASS','FAIL']` passes that key check, then `.values()` raises uncaught `AttributeError`. Separately, `probability()` line 7 evaluates `math.isfinite(10**400)` before the range check and raises uncaught `OverflowError`. Both escape the exception boundary at line 61. The protocol explicitly requires malformed responses to remain visible as ERROR; an escaping exception also prevents the workflow's per-call raw-evidence/counter save at workflow lines 114–117. Validate native container shapes and numeric range before operations that assume them, with a regression for each demonstrated input.

2. **[P2] Completed predictions are not anchored in the campaign registration.** Workflow lines 118–121 write the predictions hash only to the run's adjacent manifest. Registration records only config hash/status; compare lines 128–136 therefore checks a mutable predictions file against its mutable adjacent hash. In a copied eight-case validation replay, the real claim-only LLM fixture scored 0.5. After rewriting each retained raw text, stdout, and normalized decision to the known gold, and updating only the adjacent manifest predictions hash, `compare()` accepted the run and returned 1.0 with the worker-call count unchanged at eight. No campaign state/config/input/gold changes were needed. The existing changed-evidence test exercises inconsistent tampering but misses this self-consistent rewrite. Record the completed predictions digest in campaign state and compare it against the file and manifest. This is an integrity check within the trusted local workflow, not a claim of containment against an actor able to rewrite every asset/state file.

Evidence is in `review-scratch/evidence.txt`; the rerunnable focused reproducer is `review-scratch/reproduce.py` (run from the staged cstack checkout with `PYTHONPATH=fixtures/playground python3 <absolute-reproducer-path>`). It copies the existing `demo-first/dataset` into a fresh scratch directory and refreshes only that copy's source-manifest hashes for a replay against the current reviewed code; the original demo provenance is left untouched. Each replay executes eight deterministic local fixture workers and zero native source/provider executions. Two initial/full replay attempts consumed 16 offline fixture workers total; the earlier failed source-version check executed none.

No arithmetic defect found in nominal/weighted kappa, the failure-positive confusion denominators, abstention coverage, Brier/log-loss semantics, or family bootstrap implementation inspected. Undefined replicates remain visible. Class-conditional decided metrics and all-attempted exposure are labeled. Synthetic typed scores, deterministic stability, reference behavior passed as runtime evidence, and final-role exposure are disclosed without human/live calibration claims. The source-derived fixture oracle intentionally tests mechanics, so its agreement is not independent model evidence.

Limits: this is a focused source review and cheap replay, not SDK/provider validation, statistical certification, or an exhaustive adversarial audit. Final exposure controls operate within one in-memory campaign, and all fixture gold is publicly readable; the docs explicitly disclaim blindness/containment, so this does not establish independent final evidence. No live adapter/model support was verified. Findings describe the source before any parent-agent remediation.

## Independent remediation replay

Replayed the exact original reproducer against the fixed staged source, in a new scratch copy, without modifying the attack. `review-scratch/evidence-fixed.txt` records:

- The malformed Choice array now returns ERROR with an explicit distribution-schema error.
- The `10**400` Noul probability now returns ERROR with an explicit probability-range error.
- The same self-consistent raw/stdout/decision rewrite and adjacent-manifest hash replacement is rejected with `ValueError: Campaign-anchored prediction evidence changed`. The initial unchanged run was successfully compared before the attack; the rejection occurs on the second comparison.

Inspected the implementation changes and regression coverage: probability range precedes `math.isfinite`, Choice requires an object, completed registration stores both predictions and manifest digests, and comparison verifies those anchors. Both original findings are accepted as fixed. No remaining concrete issue found in this focused remediation review. The unchanged scope/readiness limits above still apply.

This remediation replay added eight deterministic offline fixture workers, for 24 review fixture workers total, with zero provider calls and zero native-source reruns. No broad suite was rerun independently.
