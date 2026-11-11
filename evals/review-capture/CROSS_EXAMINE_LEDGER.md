# Calibration-capture audit

Baseline: `b4c084b30052dfaad8a74b585ed10a955eabe796`. Synthetic exposed development. Two independent attackers, root as defender, and a fresh non-forked intent reviewer. Original intent and role/budget boundaries were frozen before discovery in [the audit intent](audit/INTENT.md). Each attacker had six hypotheses and twelve native executions; the defender reserved twelve further native executions. Actual usage: two native cases per attacker plus two reviewer invocations, six total. No provider/model calls, fitting, uploads or actual user labels.

## Confirmed: capture hashes did not bind content to original evidence

The archive checker accepted three separately altered captures: an initial state that differed from native input, a reviewed output that differed from native output, and a declared verbatim reviewer quote absent from the cited source. The attacker kept the verifier and native trace unchanged, altered disposable capture evidence, and regenerated the corresponding local hashes. All three produced exit 0. The original legitimate archive also passed. [Raw observations](audit/attacker_outcomes.json) and [source identities](audit/attacker_versions.json) preserve these results.

The fresh [intent review](audit/original-verdict.md) confirmed a narrow semantic-provenance checking defect. These are operator-corruption resilience probes. Native candidates were not shown to have write authority over review evidence. The current eligible set remains empty, and this audit establishes no successful human-label laundering or product execution exploit.

The repaired `verify_archive.py` compares both saved candidate versions' input/output/state/stdout against retained native traces. Captured artifact references must match their declared version; declared verbatim scripted quotations must occur in their hashed source. The shared capture guide now requires those cross-checks rather than relying only on mutually consistent capture hashes. Historical phase sources and raw verifier remain preserved.

The [independent repair review](audit/repaired-verdict.md) accepted the frozen repair: baseline exit 0; the three faults exit 1 with the corresponding mismatch. The false claim and valid ticket creation retain their native FAIL/PASS outcomes. The reviewer performed two additional local candidate invocations but did not retain their raw subprocess streams; the verdict and receipts disclose that limitation. Attackers' native execution witnesses and original native traces remain available. No later production or generalized capture claim is inferred.

Reproduce the before/after checker results without executing candidates or models:

```bash
python3 evals/review-capture/audit/run_audit.py --out /tmp/cstack-capture-audit-NEW
```

Use a new output directory. This copies the preserved archive, applies the attacker-authored faults, runs frozen original and repaired checkers, and writes raw stdout/stderr and receipts. All eight comparisons match expected behavior. Local consistency checks do not authenticate a malicious writer who replaces the source/native anchors too.

## Bounded clean results and excluded hypotheses

The [authority attacker](audit/authority/REPORT.md) tested five hypotheses. Current stopped-scope capture was blocked, the phase2 stale retry appended nothing, and native false-claim/legitimate controls behaved correctly. Cross-scope helper misuse and duplicate helper calls exceeded the one-time fixture driver's contract. A source-growth duplication in an older Bitter Lesson demonstration was reproduced but remains a historical example limitation, not a current runtime defect. No general capture runtime is bundled or promised.

The replay attacker tested three distinct corruptions. Total attempted hypotheses: eight across the two attackers. This is not comprehensive security review, production calibration, unseen generalization or evidence of malicious-process containment. The flow remains reference-only, with adapters owned by consuming projects.
