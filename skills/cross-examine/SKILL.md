---
name: cross-examine
description: Audit eval tasks, environments, and verifiers using isolated attacker, defender, and fresh independent intent-reviewer roles to uncover undeserved passes or rejected legitimate solutions, then feed confirmed root causes back into generator guidance. Use to harden or challenge an eval's scoring integrity.
---

# Cross-Examine

Lead user-facing replies with the result or decision needed. For several points, put each in its own short, plain-language bullet. A single answer can be one sentence. Link detailed evidence. Preserve open questions, approval gates and any requested artifact format.

Pick up the disputed row from the [shared decision ledger](../create-eval/references/decision-ledger.md). Follow its situation ID to the developer’s latest applicable decision, including superseded and still-open expectations. Start with that acceptance rule. Pick a wrong outcome the grader might accept and a legitimate alternative it might reject. Separate attacker, defender, and fresh independent intent-reviewer roles. Read [confirmed lessons](references/lessons.md) and keep a project ledger under [ledger guidance](references/ledger.md).

## Execution architecture

- **Parallel isolated attackers:** Run independent attack hypotheses in separate resettable scratch states or Git worktrees with candidate-equivalent tool permissions; keep operator receipts and hidden oracles out of attacker access.
- **Strictly fresh, non-forked intent reviewer:** Dispatch a read-only subagent with zero shared history from authors, attackers, repairers, or coordinators (optionally on an authorized distinct model/provider). Supply original intent first, then frozen source and raw replay evidence—never persuasion or prior verdicts.
- **Isolated defender & workflow:** Author candidate repairs in an isolated worktree (returning uncommitted patches until explicit user acceptance), replay exploits and legitimate baselines from clean state, and keep pending edits out of the active grader until post-repair intent acceptance and user approval. Deterministic workflow scripts may coordinate rounds without leaking verdicts across roles.
- **Fallback:** Disclose missing separation, serialize scratch writes, and mark formal adjudication **unreviewed**—sequential self-review supplies no independence; see [harness mapping](../run-eval/references/harnesses.md).

## Intent and independent review

Establish the original request/row, source and expert judgment before reading the verifier: capability, valid alternatives/shortcuts, scope and observable success. Ambiguity is not an exploit. Freeze eval, guidance, inputs and identities; revisions preserve earlier development evidence.

The reviewer must be fresh/non-forked and separate from authors, attackers, repairers and optimization coordinators. Supply original intent first, then frozen source and raw replay evidence, without other verdicts/tuning history. Get a verdict before accepting a finding and after freezing a repair. Keep implementation/tuning away from this reviewer. If unavailable, mark review unreviewed; sequential self-review supplies no independence.

## Bounded attacks

Map actual candidate access, scoring, reset and a legitimate baseline. Bound attack/repair work. Attackers work in separate resettable scratch states with independent initial hypotheses; the defender owns the candidate repair and may be the coordinator. Disclose unavailable separation, serializing writes when necessary.

Ask for the cheapest reproducible undeserved pass or environment/verifier defect, including violated intent, actual permissions, reproducer/scoring command and independently observed outcome. Treat wrong-modality and proxy assertions as primary attack targets—such as verifiers that check a UI icon, mock, or enqueue count instead of the user-observed outcome (live rendering, audible playback, or persisted delivery), or test one serial path when the promise is concurrent. Use [Adversarial Cases](../adversarial-cases/SKILL.md) for construction; it returns witnesses/controls, not adjudication. [Synthetic methods](../adversarial-cases/references/synthetic-methods.md) and [failure methods](../adversarial-cases/references/failure-methods.md) support project-local experiments.

Reproduce through actual candidate permissions. Operator faults and extra-access probes are separate resilience experiments. Enforce boundaries needed for isolation claims; local scratch/timeouts retain host permissions. Keep operator receipts protected from competitors. Retain failed attempts, infrastructure limits and unconfirmed hypotheses. A bounded clean result is valid.

## Replay, repair and teach

Replay from clean state on the frozen scoring path, preserving versions, raw observations and actual complete state. A score or competitor's claim is not audit acceptance. Check the audit's own grader: discovery, collaboration and learning require evidence of candidate work, not artifacts or operator reproduction alone. Seed labels cannot dismiss supported new findings.

Repair only within authority while preserving original intent/judgment; changed meaning needs a contract decision. Verification must be observational and compare complete required state, including permitted alternatives. Replay the exploit and legitimate baselines; reject blanket rejection or reference-only acceptance. Require independent intent acceptance before calling a repair validated. Review-only work returns a proposed fix; incomplete checks remain unresolved.

Append the row and grader version, reproducer, wrong and valid outcomes, and review status to the same ledger. Route missing coverage to [Adversarial Cases](../adversarial-cases/SKILL.md) and [Create Eval](../create-eval/SKILL.md), a confirmed generator failure to [Hill Climb](../hill-climb/SKILL.md), and an unsettled expectation to its owner. Keep the audit evidence linked to the original situation.

For each confirmed root cause, propose an update to the generator's existing skill/reference, or this skill's lessons: faulty assumption, divergence, generation rule and reproducer/version. Keep conjectures in the ledger. Record original/repaired outcomes, legitimate checks, independent verdict, lesson-write failures and remaining limits. Claim only demonstrated prevention/coverage; further rounds require remaining or renewed budget.

Before adopting any repair or lesson, show the user what each change does: which case fooled the old grader, how the proposed rule judges it, and what happened to a legitimate alternative on replay. Flag untested behavior. Ask which changes to keep and wait for explicit approval. Independent intent review validates a candidate; only the user authorizes adoption. Keep pending or declined edits out of the active grader, evals and skills. If there is no change to adopt, report the findings.

After corrections or confirmed labels, offer [scoped calibration capture](../expert-mode/references/calibration-capture.md); agent verdicts retain their own authority.

At an automated change checkpoint, offer review now, continue to the agreed stop, or continue for N more rounds. Follow the [change review](../hill-climb/references/change-review.md) rules for inherited cadence and uncommitted experiments. Obtain explicit user acceptance of the proposed changes before any Git commit, including local or worker commits.
