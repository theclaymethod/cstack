# Ablation and Bitter Lesson audit

2026-11-10. Original intent, frozen identities and budgets are preserved in [audit/INTENT.md](audit/INTENT.md) and [source hashes](audit/frozen-sha256.json). This audit precedes the separate skill-pack ablation.

## Roles and access

Two fresh attackers used separate disposable playground workspaces. The coordinator defended the canonical repair. A fresh intent reviewer established original criteria and clean controls; an accidental status listing later exposed completed attacker summaries. Its initial verdict had already been frozen. A replacement fresh reviewer received only original intent, source and raw before/after observations, and supplied the final independent checkpoint. Both source records and this limit are preserved.

No provider/model calls, network actions, new dependencies or live production access. Candidate subprocesses have host permissions; no security containment is claimed. Direct ledger/object perturbations are operator experiments, separately classified from candidate-access exploits.

## Finding: contradictory durable execution receipt

Original verification checked source/configuration, final-plan state, candidate artifacts and native verdict evidence, but omitted the durable `native/executions.json` receipt. An operator could replace its attempt counts with zero while `checked()` continued accepting the result. The true native traces and live reservation still recorded eight cases; extra execution remained blocked. This is an accounting-evidence defect, not a demonstrated wrong task score, candidate exploit or budget bypass.

[Minimal operator reproducer](audit/replay_ledger.py), [original observation](audit/defender-before/observation.json), [attacker evidence](audit/runtime/minimal-ledger-replay/observations.json). The defender independently replayed the same mechanism from a clean reset.

The repair binds the live receipt to saved campaign state and compares the persisted receipt's limit, reservations, completed executions and attempt identities against it. Missing or changed receipts invalidate comparisons while preserving the original charges and task evidence. A new regression changes each receipt field and removes the file, then restores it to verify legitimate acceptance.

[Repaired observation](audit/defender-after/observation.json) records rejection after the same perturbation, with eight real cases and eight reserved. [Final intent review](audit/final-review/report.md) confirms the scoped repair and continued acceptance of valid task outcomes. [Repaired identities](audit/repaired-sha256.json) freeze the version reviewed before skill-pack ablation.

Teaching change: Ablation's `references/quality.md` now requires agreement among durable execution receipts, reservations and retained traces; checking candidate/summary hashes alone is insufficient. Bitter Lesson already reaches this reference. The skill-pack ablation preserves this guidance.

## Other observations and coverage

The runtime attacker executed 33 actual cases with 40 reserved, including a targeted interruption with one retained trace and eight charged attempts. Frozen plans, completed trace/source changes, late/duplicate final calls and incomplete-result comparisons were rejected. One audit-only assertion was corrected after detecting a caller-alias error; no product defect was inferred from it. [Runtime report](audit/runtime/REPORT.md).

The semantics attacker executed 180 cases across 25 attempts. Duplicate-reminder alternatives, required combinations, shared-design model comparisons, arbitrary valid ticket IDs, permitted clarify alternatives and optional metadata behaved correctly. Wrong preservation, duplicate IDs and malformed output were rejected. No semantic discrepancy was confirmed. [Semantics report](audit/semantics/REPORT.md).

The initial reviewer executed 48 clean cases. The final fresh reviewer executed 48 cases covering clean full/reduced workflows, frozen confirmation, a legitimate alternative and original/repaired ledger replays. The defender executed 16 targeted replay cases. Regression tests and later full control runs are separate verification counters. [Final reviewer usage](audit/final-review/case-usage.json).

The audit establishes only these deterministic synthetic mechanisms. It does not establish production migration quality, statistical non-inferiority, global minimality, actual model capability, adversarial filesystem containment or general immunity. Confirmation cases remain exposed. No actual candidate-access reward hack or changed task-grading verdict was demonstrated.
