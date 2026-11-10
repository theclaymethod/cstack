# Adversarial Cases development report

Validated 2026-11-10 against C Stack 0.6.0's synthetic playground. The new shared skill constructed executable cases through the native runner. Independent review found no confirmed issue in its handoff. The observations demonstrate construction, attribution, controls, and reduction on this fixture; they do not measure performance on unseen projects.

## Delivered behavior

[Adversarial Cases](../../skills/adversarial-cases/SKILL.md) accepts the original requirement, raw evidence, actual candidate access, permitted operator injections, and the parent's budget. It returns proposed expectations or an executed challenge with activation evidence and an independent outcome witness. Bootstrap retains scoped user approval; Cross-Examine retains independent intent review and finding/repair adjudication. Neither parent treats a synthetic proposal or an armed but unreached fault as a confirmed finding.

The parent entrypoints load this sibling when constructing adversarial or injected-failure cases. The eight-skill package stays together across plugin metadata and direct installation. The playground has a new [exercise](../../fixtures/playground/exercises/08-adversarial-cases.md); materialization installs all current skills and preserves its no-overwrite behavior.

## Fresh construction exercise

A fresh builder received the installed skill, original fixture source, and a bounded construction request. It did not receive earlier audit conclusions. It wrote only inside its disposable `eval-runs/case-build`, read the original spec/rubric and actual source, and executed the native evaluator. Its complete [evidence handoff](evidence/CROSS-EXAMINE-HANDOFF.md), [proposed cards](evidence/scenario-cards.json), [counts](evidence/counts.json), [commands](evidence/commands.json), and source/artifact hash inventories are retained. All three scenario approvals remain pending; this development task did not request human labeling.

| Case | Observations and controls | Interpretation |
| --- | --- | --- |
| Lifecycle interruption | Two fresh native baselines stopped at `complete_attempt` after eight cases had completed but before ledger completion. Each has an exact trigger event and actual exit -9. Native status recovered the completed measurement and incumbent without adding case executions or changing the eight-case charge; repeated status preserved evidence bytes. | Current native recovery worked at the tested boundary. Operator tracing/self-termination is extra access, distinct from candidate capability. |
| Scoring boundary | Two authorized-creation variants emitted an action claim with unchanged state: zero new tickets. Native grading rejected both; the supplied deliberately defective action-only proxy accepted both. Standard and alternate valid IDs/notes passed all four native controls, preserving prior records and metadata. | A reproduced flaw in the supplied exercise proxy; no new current-native defect. The state witness is independent of the disputed claim/proxy verdict. |
| Non-activation | Identical SIGKILL configuration targeted attempt 99 while only attempt 0 existed. It activated zero times, exited normally, and produced the same eight outputs/outcomes as the clean run. | Instrumentation/non-activation control, not evidence of recovery under the fault. |

Reduction removed unrelated ticket/audit context while retaining the false-creation discrepancy and both legitimate controls. Moving the lifecycle stop earlier to `execute_attempt` removed complete-evidence preconditions; it remained pending/charged with zero case executions. That reduction was rejected and retained as a negative control.

Actual work per construction run: **38 native case executions**, **3 process interruptions**, and **6 supplied-proxy invocations**, within 120/4 exercise limits. Campaign reservations total 40, including the early-stop reservation whose eight cases never executed. Scoring contributes six executions separately. Status reconciliation launches no candidates. No provider/network calls were used.

The [independent review](independent-review.md) checked raw receipts/hashes, revalidated all seven retained native runs through `checked_run` without launching new cases, and checked source wiring and approval boundaries. The original materialized workspace preceded the final addition of exercise 08; its handoff explicitly records that missing file and relied on the supplied construction request. The current factory includes exercise 08. Absolute paths/PIDs in historical evidence identify the original run; use the portable replay for a new run.

## Reproduce

From the owning C Stack checkout:

```sh
python3 evals/adversarial-cases/replay.py --out eval-runs/adversarial-replay
```

Choose an unused output directory. The replay materializes the current fixture with current installed skills, copies the two preserved constructor/injector scripts into its scratch directory, and runs actual native commands. It checks targeted activation plus observed process exits, non-activation, recovery/no-rerun/accounting, exact output replay into the supplied proxy, independent ticket membership/preservation, legitimate alternatives, and execution counts. The initial version had 71 replay assertions; the [subsequent audit](CROSS_EXAMINE_REPORT.md) strengthened the current gate to 103. These checks are replay assertions, not 71 independent scenarios or measurements of skill effectiveness. A future change to the runner may legitimately require updating this source-sensitive instrumentation.

In a generated playground workspace:

```sh
python3 scripts/run_cstack_evals.py --suite adversarial-cases --out eval-runs/adversarial-controls
python3 scripts/run_cstack_evals.py --suite all --out eval-runs/cstack-controls
```

All seven groups passed, including the existing calibration/replay/audit groups, the new replay, and 22 native fixture tests. All eight skill packages also passed frontmatter validation; metadata versions and changed-document links were checked. The saved [control summary](validation/summary.json) and [native test log](validation/playground.stderr.txt) record the local validation. This automation replays constructed cases; it does not invoke a new model or prove a parent skill completes its whole interview/audit workflow. Human-facing cards, construction evidence, independent review, and control results remain separate artifacts.

## Later research

Parallel investigations produced [synthetic-generation pilots](../../research/synthetic-generation-followups.md) and [failure-injection pilots](../../research/failure-injection-followups.md). They cover reachable state sequences, constraint witnesses, relation-preserving shrinking, mutation-guided selection, verified judge challenges, named failpoints, storage faults, subprocess failures, and optional loopback proxy faults. Each specifies a falsifiable pilot, limits, and primary sources. No proposed framework is installed or implemented here. Process interruption does not establish power-loss durability, production reliability, real traffic prevalence, or generalization.

## Subsequent Cross-Examine

The [2026-11-10 audit](CROSS_EXAMINE_REPORT.md) independently confirmed and repaired one native ticket-schema false rejection and one fixed-replay evidence-validation mechanism. Its ledger distinguishes operator calibration from candidate exploits. Historical construction evidence and initial results above remain the original 0.6.0 observations. Current 0.6.1 validation uses eight combined groups and 23 native tests.
