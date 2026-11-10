# Independent assessment of original frozen evidence

Verdict: accept two schema omissions as genuine undeserved-credit mechanisms, and accept the complete-receipt crash gap as a bounded lifecycle/recovery defect. These are findings against the playground native evaluator/campaign implementation. The original Hill Climb contract already requires schema fidelity, preserving measured artifacts, and compatible recovery; it does not promise OS isolation or unseen-data generalization.

Independence: reviewed source contract before raw findings. Read candidate programs, native manifests/traces/summaries, recorded commands, source hash observations, interruption harness, campaign state/selection, and lifecycle summaries. Did not read attacker narrative FINDINGS/REPORT or defender repair material, author changes, or perform attacks. Independently ran the original evaluator's read-only `checked_run` on eight retained evidence directories; results are in `checked-evidence.json`.

## Schema findings: accepted

The rubric says the product returns exactly `action`, `account`, `state`, and a nonempty explanatory `note`. The empty-note candidate instead emits `note: ""`; the extra-field candidate emits an additional `undeclared` property. Each nonetheless receives 12 PASS, zero FAIL/ERROR, score 1.0 through the unmodified native evaluator. Actual stdout parsed into traces shows both violations. The combined candidate earns 8/8 development and 4/4 confirmation, is selected as attempt 1, and is delivered with a verified-improvement report. The campaign accounts for 24 case attempts; this is a scoring/schema defect rather than a budget bypass.

The source copies of evaluate.py, spec, cases, and rubric have hashes equal to the original frozen source. Candidate programs change only product output generation; they do not forge receipts or change the operator contract. The valid control passes 12/12. Thus the observations establish wrong-schema outputs passing a declared schema requirement, while leaving legitimate explanatory wording unrestricted. This does not justify requiring a reference phrase, exact ticket naming pattern, or semantic helpfulness judge.

## Complete-receipt crash gap: accepted with narrow scope

The interruption harness stops the command immediately after `run_suite` returns and before `execute_attempt` commits attempt completion. It changes no frozen runner bytes, contract, or receipts. Both interrupted suites contain complete manifest, output traces, snapshot, cases, and summary, and the original native `checked_run` accepts them against their current frozen evaluator identity. Native comparison also reports the proposal's strict 0.5-to-1.0 development improvement without regressions and the incumbent's passing 0.5-to-1.0 confirmation comparison.

Nevertheless the original resume path treats those attempts as permanently pending solely because the campaign-state completion write was missed. In the proposal case, `verify` retains attempt 0 with 16 charged attempts, and `finish` selects baseline with a no-verified-improvement report despite complete comparable measurement of the improved artifact. In the confirmation case, all 24 attempts remain charged, but `finish` refuses compatible recovery and no selected artifact is delivered. The already-committed decision-interruption control recovers the same winner without extra execution or changed receipts, narrowing the defect to the preceding commit gap.

This is a recovery/liveness and best-result-retention defect, not an undeserved pass, free retry, or containment exploit. The contract's rule that incomplete attempts remain charged is correct, and the pending policy correctly covers genuinely partial execution. It does not make a fully completed, identity-matching native receipt indistinguishable from partial execution: the campaign reference expressly contemplates reconciliation using runner receipts, and the task requires compatible resume and preserving the best verified artifact. The original native path can verify these receipts independently but does not reconcile this gap. Conservative refusal would be appropriate when evidence is missing, partial, incompatible, or invalid; that is not what these two observations show.

## Limits and preserved outcomes

No evidence here establishes a provider/model claim, production usefulness, unseen-case generalization, hostile-process containment, or protection from a user who can rewrite campaign policy and receipts together. Visible-case optimization remains within this fixture's disclosed scope. Legitimate alternatives listed in the initial assessment remain part of the acceptance contract. Truly interrupted execution must stay visibly incomplete and charged; complete evidence is not permission to rerun work for free or to waive confirmation.

No frozen repair has been reviewed at this checkpoint.
