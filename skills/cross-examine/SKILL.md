---
name: cross-examine
description: Proactively red-team generated agent evaluations with a small adversarial swarm. Use when creating or hardening eval tasks, environments, or verifiers to expose ways to pass without fulfilling the intended task and teach eval generators from confirmed flaws.
---

# Cross-Examine

Attack an evaluation before trusting its scores. Seek a concrete counterexample: an agent receives credit without achieving the intended outcome, or the environment prevents or mismeasures a legitimate solution. Feed confirmed design flaws back into the instructions that generate future evaluations.

Before generating or reviewing an eval, read [confirmed design lessons](references/lessons.md) and apply those whose conditions match the task.

Maintain an evidence ledger using [the ledger instructions](references/ledger.md). Reuse the eval project's existing ledger; otherwise create `CROSS_EXAMINE_LEDGER.md` beside the eval. The ledger records what was prevented, what remains unverified, and whether the evaluation still measures its intended capability.

## Use the smallest sufficient setup

Default to ordinary local files: Markdown for the ledger and lessons, JSON or text for task state, and separate scratch directories for attacks and replays. Use the project's existing runtime and checks. Add SQLite when the task requires SQL, transactions, relational constraints, or database lifecycle behavior. Use Docker or another isolation boundary when executing untrusted programs or testing permissions that local processes cannot enforce; reuse an adequate existing sandbox when available. Record why each added dependency is needed.

A disposable directory and subprocess timeout provide repeatability, not containment. Local replay is suitable for trusted calibration or reviewed artifacts, but shares the host user's file, network, and process access. Record that limitation in the ledger and verdict. Test permission-dependent claims in an environment that enforces the claimed boundary; otherwise leave those claims unverified. Keep evidence and grader receipts outside candidate access using the available access controls.

## Establish the game

Start with the original eval row or task request and its source context, including the expert judgment when available. State the intended capability, scope, observable success, and acceptable alternatives before reading the environment, verifier, scoring rules, and generator instructions. Resolve ambiguity in the original intent before declaring a shortcut illegitimate.

Record the intended capability, permitted shortcuts, and out-of-scope claims in the ledger before attacking. Freeze the eval/grader version and the inputs for scored runs. If candidate output motivates changes, preserve the old result and label that run as development evidence; use a fresh candidate on the frozen revision for a held-out claim.

Map what the evaluated agent can actually read, write, execute, and influence, including artifacts, processes, tools, network access, and persistent state. Separate evaluator-only assets from agent-accessible assets. Record the exact verifier entrypoint and how its result becomes a score.

Use disposable copies or isolated runs. Establish that reset works and that a known legitimate outcome receives the expected result. Use an existing reference solution when available; report missing baseline evidence rather than inventing it. A broken baseline is itself a finding and limits conclusions from later attacks.

Choose a bounded attack budget before dispatch, using the user's budget when provided; otherwise default to one parallel round with three attackers and at most two concrete attempts per attacker. Verification and reporting still follow when the attack budget ends. Scope all attempts to the authorized eval sandbox.

## Keep intent review independent

Use a fresh, non-forked agent that has not authored or repaired this eval, hill-climbed candidates or graders, or attempted reward hacking. This reviewer is separate from the attack lanes and the coordinator making those changes. Give it the original row and source context first, then the frozen eval and observed replay evidence, without the others' verdicts or optimization history.

Have it check whether incorrect results can pass, legitimate alternatives face added requirements, or the eval has drifted from the original row's meaning and scope. Seek its verdict before accepting findings and after repairs. It adjudicates evidence; keep it out of candidate tuning and iterative reward feedback. If an independent agent is unavailable, record intent review as unreviewed while continuing other authorized work.

## Dispatch the adversaries

Launch a mini-swarm with separate ownership and environments. Three complementary lanes are a useful default; adapt them to the eval:

- **Verifier:** Obtain credit with a wrong or incomplete result. Probe what the verifier trusts: self-reported success, editable expected answers, forged artifacts, partial matches, empty cases, skipped checks, errors, and score aggregation.
- **Environment:** Exploit lifecycle and isolation. Probe stale state, answer leakage, writable evaluator assets, process interference, reset failures, and contamination between runs.
- **Task contract:** Satisfy the literal checks while violating the intended outcome. Probe proxy metrics, hardcoded answers, output substitution, omitted requirements, and legitimate alternatives the verifier rejects.

Each attacker receives the task, success contract, access boundary, runnable environment and verifier, budget, and this objective:

> Find the cheapest reproducible way to earn credit without achieving the intended outcome, or demonstrate an environment/verifier defect that invalidates the evaluation. Produce the exploit and observed result. Attack the evaluation; repairing it is the coordinator's job.

Keep their hypotheses independent during the first round. Give each agent its own scratch space and reset state; serialize runs if the infrastructure cannot isolate them. Attackers may alter only their assigned sandbox and return findings; the coordinator owns canonical eval and skill edits. If delegation is unavailable, run the lanes sequentially and disclose that limitation.

White-box inspection can expose hypotheses, but a valid exploit must execute with the evaluated agent's actual access. Mark attacks requiring extra access separately. Avoid counting an intended efficient solution as an exploit merely because it differs from a reference trajectory.

Require each attacker to return:

- The violated requirement and the candidate's actual permissions.
- The smallest artifact or exact actions needed to reproduce, including setup and reset.
- Verifier invocation, observed output/score, and independent evidence of the actual task outcome.
- Any unexecuted hypothesis, failed attempt, or infrastructure limitation, clearly distinguished from a reproduced finding.

## Reproduce and adjudicate

Replay candidate findings from a clean reset against the original eval. Preserve the relevant eval/verifier version and exploit artifact. Confirm the result through the actual scoring path; a locally forged success message alone is insufficient.

Have the independent intent reviewer judge the candidate outcome against the original row and task contract. For environment failures, reproduce the broken invariant or legitimate outcome that was mismeasured. Distinguish:

- A confirmed scoring bypass or environment defect.
- A specification ambiguity that needs an explicit contract decision.
- A hypothesis or attack that did not reproduce.

Merge duplicate findings by root cause. Explain the trust boundary or invalid assumption that made each confirmed flaw possible and what it does to score interpretation. A bounded search without findings establishes only what was attempted, not that the eval is secure.

Include the outer grader in that review: can a candidate earn credit without supplying its own reproducer or promised learning artifact? Does a repair weaken the task or reject valid alternatives? Are seed labels overriding a genuine new defect? Distinguish artifact validation from discovery, swarm use, and learning; credit only what the evidence establishes.

## Harden within scope

When eval changes are authorized, fix the faulty assumption at its source. Prefer checking independently observable outcomes, protecting evaluator-owned state, isolating runs, and restoring reliable reset behavior over blacklisting one exploit's spelling.

Replay the confirmed exploit after the fix: it should lose undeserved credit or the environment defect should disappear. Rerun the legitimate baseline and relevant existing checks to show that valid solutions still work. Respect the repository's rules for creating test files; direct replays and existing checks can provide evidence without adding new tests.

If the scope is review-only, deliver the reproducer and proposed correction without modifying the eval. Preserve unresolved findings when repairs or validation cannot be completed. Additional attack rounds require remaining budget or a newly agreed budget.

## Teach the generator

After confirming a flaw, find the skill that actually guides this eval generator. Add or refine one concise lesson there, or in an existing reference it already routes to. Preserve unrelated instructions and deduplicate by mechanism.

If no generator skill exists, create `references/lessons.md` beside this skill when the first confirmed lesson is available, link it from this skill, and instruct future runs to read it before generating or reviewing evals. Keep the reusable lesson with the skill and detailed repro artifacts with the eval. Report any inability to persist the lesson.

Each lesson must explain:

- **Failure:** The design assumption and how it was exploited.
- **Why:** The gap between the measured signal and intended outcome.
- **Generate instead:** A concrete construction rule for future evals, scoped to the conditions that make it necessary.
- **Evidence:** The eval/version and reproducer location, plus the observed result and any verified repair.

Promote only confirmed mechanisms into generation guidance. Keep conjectures in the findings report. For example, if a verifier accepts an agent-writable success flag, teach generators to measure the actual outcome through evaluator-owned evidence; banning that particular filename does not address the flaw.

Update the ledger after replay with original and repaired outcomes, legitimate-solution checks, and remaining limits. Finish with the intent verdict, confirmed findings and evidence, repairs and replay results, exact ledger/lesson files changed, and unresolved limitations. Claim completion only for the attack budget and validation actually performed.
