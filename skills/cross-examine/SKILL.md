---
name: cross-examine
description: Challenge eval tasks, environments, and verifiers with an attacker, defender, and independent intent reviewer. Find undeserved passes or rejected legitimate solutions, then feed confirmed flaws back into eval-generation guidance.
---

# Cross-Examine

Find wrong outcomes earning credit or legitimate outcomes rejected by an eval. Use an attacker, a defender and a fresh independent intent reviewer. Read [confirmed lessons](references/lessons.md) and keep a project ledger under [ledger guidance](references/ledger.md).

## Intent and independent review

Establish the original request/row, source and expert judgment before reading the verifier: capability, valid alternatives/shortcuts, scope and observable success. Ambiguity is not an exploit. Freeze eval, guidance, inputs and identities; revisions preserve earlier development evidence.

The reviewer must be fresh/non-forked and separate from authors, attackers, repairers and optimization coordinators. Supply original intent first, then frozen source and raw replay evidence, without other verdicts/tuning history. Get a verdict before accepting a finding and after freezing a repair. Keep implementation/tuning away from this reviewer. If unavailable, mark review unreviewed; sequential self-review supplies no independence.

## Bounded attacks

Map actual candidate access, scoring, reset and a legitimate baseline. Bound attack/repair work. Attackers work in separate resettable scratch states with independent initial hypotheses; the defender owns canonical repairs and may be the coordinator. Disclose unavailable separation, serializing writes when necessary.

Ask for the cheapest reproducible undeserved pass or environment/verifier defect, including violated intent, actual permissions, reproducer/scoring command and independently observed outcome. Use [Adversarial Cases](../adversarial-cases/SKILL.md) for construction; it returns witnesses/controls, not adjudication. [Synthetic methods](../adversarial-cases/references/synthetic-methods.md) and [failure methods](../adversarial-cases/references/failure-methods.md) support project-local experiments.

Reproduce through actual candidate permissions. Operator faults and extra-access probes are separate resilience experiments. Enforce boundaries needed for isolation claims; local scratch/timeouts retain host permissions. Keep operator receipts protected from competitors. Retain failed attempts, infrastructure limits and unconfirmed hypotheses. A bounded clean result is valid.

## Replay, repair and teach

Replay from clean state on the frozen scoring path, preserving versions, raw observations and actual complete state. A score or competitor's claim is not audit acceptance. Check the audit's own grader: discovery, collaboration and learning require evidence of candidate work, not artifacts or operator reproduction alone. Seed labels cannot dismiss supported new findings.

Repair only within authority while preserving original intent/judgment; changed meaning needs a contract decision. Verification must be observational and compare complete required state, including permitted alternatives. Replay the exploit and legitimate baselines; reject blanket rejection or reference-only acceptance. Require independent intent acceptance before calling a repair validated. Review-only work returns a proposed fix; incomplete checks remain unresolved.

For each confirmed root cause, update the generator's existing skill/reference, or this skill's lessons: faulty assumption, divergence, generation rule and reproducer/version. Keep conjectures in the ledger. Record original/repaired outcomes, legitimate checks, independent verdict, lesson-write failures and remaining limits. Claim only demonstrated prevention/coverage; further rounds require remaining or renewed budget.
