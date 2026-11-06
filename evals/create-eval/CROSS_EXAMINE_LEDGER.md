# Create Eval cross-examination

## Contract and boundary — round 1

Original revision: `a7fc7cf2cc2716e474143b7e85bfbda6d1ef2d62` (C Stack v0.3.0). This is a development audit of Create Eval and the references/tooling it actually uses, not an unseen benchmark.

Intended capability: author replayable evals that measure the requested behavior, grounded in actual available evidence and appropriate expert authority. Before relevant production traces exist, the workflow should support realistic inputs, actual feature runs, usable review, and promotion of supported observations. Preserve assertion scope, unresolved evidence, independent source families, and legitimate alternatives. Capture and package validity alone do not establish eval quality.

Permitted shortcuts: reuse project harnesses, existing trace viewers, external eval skills, deterministic checks for explicit invariants, and local files. A scoped negative needs no unrelated complete replacement. A mocked or unrun feature may yield honest provisional cases, not product-execution evidence. A bounded clean conclusion is acceptable; finding a flaw is not mandatory.

Access: three attackers receive the frozen skill/references and existing synthetic evidence. Each owns a separate ignored scratch directory and may write only there. All processes retain the host account's actual permissions; these instructions do not enforce containment. No production system, real expert data, paid model API, database, or Docker is needed. Inline reviewed Python may exercise the trusted local reviewer. Candidate-authored programs are not executed as untrusted submissions.

Budget: one parallel round, three lanes (verifier, environment, task contract), at most two concrete attempts per lane. Coordinator reproduction, legitimate controls, repairs, and reporting follow that round. No additional discovery round is implied.

Verifier boundary: there is **no end-to-end Create Eval behavioral grader**. Existing package receipts check installation and local helper behavior. The review API's HTTP/persistence result is an actual executable path, but is not a score for eval-authoring competence. Document-only counterexamples are contract gaps or hypotheses unless their promised behavior is reproduced. No full-skill pass rate will be inferred.

Original guidance is frozen with per-file SHA-256 values before dispatch in the local run manifest. Frozen source remains recoverable from the original commit. Existing evidence is synthetic; no clinical truth or clinician endorsement is claimed. Baselines and findings will be appended below. Attack reports, before/after results, and public reproductions will be stored beside this ledger after coordinator review.

Out of scope: security penetration testing, attacking external systems, changing hidden labels, opening reserved final-test data, manufacturing expert gold, measuring production prevalence, and proving broad held-out skill effectiveness. Browser rendering remains unverified in the current environment.

## Initial evidence limits

The v0.3.0 packaging receipt records 17 direct HTTP/persistence checks and installed CLI startup. These establish helper mechanics only. They do not evaluate how a fresh agent follows Create Eval or whether a generated grader measures its task. This audit must keep those claims separate.

## Completed round — 2026-11-06

Three distinct agents executed their assigned lanes, without further delegation: `/root/create_eval_verifier`, `/root/create_eval_environment`, and `/root/create_eval_contract`. Each completed two attempts. No confirmed scoring bypass, lifecycle defect, or new specification gap was reproduced. No repair or additional attack round was performed. The [report](REPORT.md) links the results and reproductions.

The coordinator established a [legitimate baseline](evidence/round-1/coordinator/baseline.json) through the original helper's HTTP path: two distinct scoped reviews, an append-only amendment, and restart recovery. The [replay receipt](evidence/round-1/coordinator/replay.json) independently repeats the environment lane's exact reviewed inline commands in a new directory and records identical observed outcomes. Original guidance hashes remained unchanged. These replays verify helper behavior, not eval-authoring quality.

| Attempted bad pattern | Actual observation | Prevention claim and limit |
| --- | --- | --- |
| Widen a missing-source negative into numerical gold | Existing synthetic source distinguishes the supported source answer from an uncertain probability. Guidance explicitly forbids widening. | Specification defense only; no authoring/grading agent was induced to widen the label. |
| Turn perfect decided-only class rates into a trust verdict | Hypothetical arithmetic yields 100% on both class rates while only 2/202 cases are decided. Guidance requires coverage and rejects an undeclared pass policy. | Reporting defense in the contract; no automated report grader or semantic judge ran on this attack. |
| Carry a review onto a changed output | Real HTTP path returns 400 for an old hash and for reassignment of an existing review ID to a new trace version; correct matching returns after restoring the original input. | Reproduced rejection and legitimate recovery for these version changes only. |
| Collapse separate dissent or overwrite an amendment from a stale tab | Separate reviewer observations survive. A stale amendment returns 409 without changing disk. The earlier verdict and correction remain history after restart. | Reproduced persistence for these independent IDs and amendment paths; reviewer authority and browser behavior are unverified. |
| Promote numerical uncertainty, a shortness preference, or a key-name proxy while authoring | An agent authored one source-naming package, retained the uncertainty separately, kept all gold null, and accepted prose and structured source names. | Narrow same-context development application. Its two PASS and two FAIL observations are not an accuracy score or blind calibration. |
| Promote a handwritten trace and proposed rubric into an actual product run or expert gold | An agent retained handwritten provenance, resolved three events into two current observations, and left the feature unrun. | Narrow development application; no actual feature entrypoint, product execution, or expert authority was available. |

Evidence: [verifier](evidence/round-1/verifier/results.json), [environment](evidence/round-1/environment/results.json), [task contract](evidence/round-1/contract/results.json). The [evidence manifest](evidence/round-1/evidence-manifest.json) preserves original and published hashes and identifies path and formatting projections for publication. All source examples and lifecycle labels are synthetic.

Documentation verification: seven published inline blocks also ran successfully in a fresh local clone, including restored frozen inputs and fixed-artifact inspections. The [receipt](evidence/round-1/public-reproduction.json) is a replay of the recorded mechanics, not another discovery round or a fresh authoring experiment.

## Intent verdict

The observations are consistent with the intended workflow within this small development round. They establish narrower evidence: explicit contract defenses, actual helper lifecycle checks, and one agent's two bounded applications. They do **not** establish reliable end-to-end authoring, broad judge correctness, production performance, or held-out generalization. There is still no end-to-end behavioral verifier for Create Eval.

No confirmed new mechanism warranted a teaching change, so Create Eval and the shared lessons were left unchanged. In particular, this audit did not weaken outcome criteria, require a single reference representation, invent expert labels, or convert packaging success into skill credit. The three-lane dispatch and candidate-authored artifacts establish that this review occurred, not that the skill has a passing benchmark score.
