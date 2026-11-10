---
name: cross-examine
description: Challenge eval tasks, environments, and verifiers with an attacker, defender, and independent intent reviewer. Find undeserved passes or rejected legitimate solutions, then feed confirmed flaws back into eval-generation guidance.
---

# Cross-Examine

Have an attacker seek undeserved credit, a defender repair the flaw, and an independent reviewer check both against the original eval's intent. A legitimate solution that the environment prevents or mismeasures is also a finding.

Read [confirmed lessons](references/lessons.md) before generating or reviewing evals. Keep an evidence ledger using [the ledger guidance](references/ledger.md). Reuse the project's ledger or create `CROSS_EXAMINE_LEDGER.md` beside the eval. Record demonstrated preventions, unresolved risks, and whether the eval still measures its intended capability.

## Anchor the original intent

Start with the original row or request, source context, and expert judgment before reading the verifier. Record intended capability, scope, observable success, acceptable alternatives, permitted shortcuts, and out-of-scope claims. Resolve ambiguous intent before calling a shortcut illegitimate.

Freeze the eval, grader, guidance, and inputs for scored runs. Preserve earlier results when candidates motivate changes; those runs are development evidence. Held-out claims need a fresh candidate on the frozen revision.

Map the evaluated agent's actual access and the scoring entrypoint. Verify reset and a known legitimate baseline. A broken baseline is a finding; missing baseline evidence limits conclusions. Choose a bounded attack and repair budget. Verification and reporting still follow when the search ends.

## Keep intent review independent

Use a fresh, non-forked reviewer who has not authored or repaired the eval, optimized candidates or graders, or attempted reward hacking. Keep this reviewer separate from attackers, the defender, and anyone coordinating those edits. Supply the original row and source first, then the frozen eval and observed replay evidence, without others' verdicts or optimization history.

The reviewer checks whether wrong results can pass, legitimate alternatives face unsupported requirements, or the eval has drifted from its original meaning. Seek a verdict before accepting a finding and after freezing a repair. Actionable explanations at bounded checkpoints are useful; implementation and repeated tuning against this reviewer's scores compromise independence.

If an independent reviewer is unavailable, mark intent review unreviewed and continue other authorized work. Sequential coverage cannot substitute for independent review.

## Attack within the evaluated agent's access

Start with an attacker, a defender, and the independent reviewer. Consider verifier trust, environment lifecycle and isolation, and gaps between literal checks and intended outcomes. These are coverage questions, not mandatory separate agents.

For targeted challenge construction, have the attacker or assigned builder use [Adversarial Cases](../adversarial-cases/SKILL.md). Supply original intent/source, the frozen scoring path, candidate access and permitted operator injections separately, and the remaining budget. Request setup/reset, actual activation evidence, an independent outcome witness, controls, and reduction history. An operator-injected fault is a resilience experiment rather than automatically a candidate-access exploit. The builder's handoff is evidence for this workflow; finding adjudication and repair acceptance remain with Cross-Examine and its independent intent reviewer.

Give each attacker its own reset state and a bounded objective:

> Find the cheapest reproducible way to earn credit without achieving the intended outcome, or demonstrate an environment/verifier defect. Return the violated requirement, actual permissions, minimal reproducer, scoring command and result, and evidence of the real task outcome.

Keep initial hypotheses independent across attackers. Serialize runs if isolation is unavailable. Attackers edit only their assigned sandbox; the defender owns canonical repairs and may be the coordinator. Keep these roles separate. When delegation is unavailable, disclose missing role separation.

White-box inspection can suggest attacks, but reproduced exploits must use the evaluated agent's actual permissions. Report extra-access experiments separately. Keep failed attempts, hypotheses, and infrastructure limits distinct from findings.

For condition generation and reduction, consult [synthetic methods](../adversarial-cases/references/synthetic-methods.md). For executable perturbations, consult [failure methods](../adversarial-cases/references/failure-methods.md). Implement the selected experiment in the project with its native runner and bounded access.

## Replay and repair

Replay findings from a clean reset through the actual scoring path on the original frozen eval. Preserve the reproducer, versions, independently observed state, and score. Protect audit evidence and grader receipts from both competitors.

The eval score and audit acceptance are separate decisions. An attacker claiming victory, a defender claiming a fix, or a higher score is insufficient. Distinguish reproduced defects, specification ambiguities needing a contract decision, and unconfirmed hypotheses. A bounded search with no confirmed flaw is a valid result.

Check the audit's own grader too. Credit for discovery, reproduction, collaboration, or learning needs evidence of that behavior. Artifact checks alone do not establish it, and seed labels must not override a genuine new defect.

When repairs are authorized, fix the underlying assumption while preserving the original row and expert judgment. Changing their meaning needs an explicit contract decision. Keep verification observational and compare the complete required state. Verify that the exploit loses undeserved credit or the environment defect disappears. Replay legitimate baselines, including supported alternatives. Accept only a repair that preserves valid outcomes and passes independent intent review. Rejecting everything or accepting only one reference answer does not establish a fix.

Use existing checks and direct replays within project rules on new test files. For review-only work, deliver the reproducer and proposed repair. Leave unvalidated repairs unresolved. Further attack rounds need remaining or newly agreed budget.

## Keep tooling proportional

Use Docker or an adequate existing sandbox when untrusted execution or permission tests require isolation.

Scratch directories and timeouts provide repeatability, not containment. Local processes retain host permissions. Enforce any boundary a claim depends on or leave that claim unverified. Protect evaluator-only assets with actual access controls, not instructions.

## Teach the generator

For each confirmed mechanism, update the skill that guides the generator or a reference it already reads. If none exists, use this skill's linked lessons file. Explain the faulty assumption, why the score diverged from intent, what to generate instead, and the reproducer/version supporting it. Deduplicate by root cause. Keep conjectures in the ledger and report failed lesson writes.

Update the ledger with original and repaired outcomes, legitimate-solution checks, the independent intent verdict, and remaining limits. Claim only the coverage and prevention actually demonstrated.
