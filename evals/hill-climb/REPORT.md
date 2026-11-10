# Hill Climb development verification

On 2026-11-10, the new Hill Climb skill was exercised against an isolated deterministic support-agent project. The native evaluator/campaign tool and exercises were initially built in a separate local `cstack-playground` repository. They now live in the canonical [playground fixture](../../fixtures/playground/README.md), with disposable workspaces generated for agent trials. The skill itself remains a portable procedure with campaign and optimizer references; it does not install an optimizer framework or introduce another project grader.

## Fresh-agent exercise

A fresh agent received the skill, the flawed product, synthetic contract/cases, and native evaluator. Supplied solution candidates were omitted from that isolated project. The request authorized edits only to `support_agent.py`, with 48 case attempts total and 8 reserved for confirmation. The owner policy was strict development-score improvement with no regressions of previously passing cases, followed by baseline/candidate confirmation.

The agent inspected actual baseline failures, wrote a candidate, used the native campaign commands, confirmed it, and left the selected code in the requested target. The changes require explicit ticket authorization, preserve prohibitions, resolve a valid explicit or sole account, and scope duplicate prevention to an open VPN ticket for that account.

| Phase | Baseline | Selected candidate | Regressions/errors |
| --- | ---: | ---: | --- |
| Development | 4/8 PASS | 8/8 PASS | 0 / 0 |
| Confirmation | 2/4 PASS | 4/4 PASS | 0 / 0 |

The campaign used 24/48 case attempts: eight baseline, eight candidate, four baseline confirmation, and four candidate confirmation. It stopped after fully passing confirmation. [The receipt](evidence/forward/receipt.json), [selected code](evidence/forward/best.py), [diff](evidence/forward/best.diff), [selection](evidence/forward/selection.json), and [attempt evidence](evidence/forward/attempts/) retain actual observations.

All twelve cases were opened before fitting. These results demonstrate synthetic development improvement and the reserved-confirmation workflow, not unseen generalization or measured optimizer/model effectiveness. The original execution-module version is retained as `evidence/forward/evaluate-version.py`; it predates the native-runner review fixes below. Historical records preserve their original paths/hashes.

## Native controls and review fixes

The test repository's fifteen behavioral checks exercise actual subprocess code changes, per-case state grading, strict regression gates, no-improvement, protected confirmation reserve, error and interruption charging, exact resume identity, confirmation rejection, custom authored-case identity, and best-artifact/diff delivery.

Independent review reproduced three native-runner defects before delivery:

- A completed candidate could lose its selection decision across an interruption between execution and comparison. Resume now reconciles measured undecided proposals from retained parent/evidence without rerunning or charging again.
- Standalone comparison trusted self-consistent summaries even when their outcomes contradicted the traces. Runs now retain the case-source snapshot; comparison checks exact membership/input/output and reuses the same grader before trusting a summary. Campaign receipts also cover the retained source.
- Python equality treated JSON numbers and booleans as equal during extra-state preservation. Canonical type-aware comparison now preserves JSON types while permitting object-key reordering.

The revised runner also rejects malformed authored-case fields before candidate execution and explicitly reports no verified improvement when the baseline is retained. Source changes invalidate previous campaign identities rather than silently migrating them.

The selected fresh-agent artifact was subsequently executed against the revised runner on all twelve cases: baseline 6/12 PASS, selected 12/12 PASS, no selected errors or regressions. [Post-review observations](evidence/post-review/summary.json) and [run evidence](evidence/post-review/) record the version and actual outputs. This replay checks compatibility of the measured artifact; it is not a second fresh-agent optimization result.

## Existing evals and installation

The playground wrapper invokes existing C Stack commands directly: Expert Review's 19 calibration controls, Cross-Examine's 11 controls, Bootstrap's 56 stored-observation verdicts, and Bootstrap's nine recorded audit observations. It also runs the native playground tests. The commands and stdout/stderr are saved with each invocation; favorable exits are not relabeled as model-performance measurements.

All seven skill folders are copied into the test repo with a content-hash lock and relative Claude Code/Cursor links. The sync helper verifies installed content and refuses to overwrite modified or unmanaged skill folders. Seven exercise cards provide concrete requests and completion criteria. The cards make every skill available to try; this development pass does not claim fresh-agent verification of all seven workflows.

From the C Stack repository root:

```sh
python3 fixtures/playground/scripts/new_workspace.py --out eval-runs/playground
cd eval-runs/playground
python3 scripts/sync_skills.py --check
python3 -m unittest discover -s tests -v
python3 scripts/run_cstack_evals.py --suite all --out eval-runs/cstack-controls
```

Choose fresh output directories. The test repo README documents native runs, candidate comparison, campaign start/try/finish/status/verify, and the seven exercises.

## Limits

The product and every supplied case/conversation/expected outcome are synthetic. No provider/model/paid optimization campaign was run. DSPy, Ax, GEPA, and Halo were source references rather than installed backends. There is no semantic judge calibration or enforced hidden confirmation store. Candidate subprocesses run trusted local code with host permissions; scratch state and timeouts provide repeatability, not security containment.

The campaign example is deterministic and project specific. It does not establish stochastic optimization quality or universal budget/selection defaults. Partial or invalid interrupted confirmation remains charged and cannot support selection. The subsequent Cross-Examine repair reconciles fully completed, identity-matching native evidence across the receipt-commit gap without a new execution or charge. The repos are local and uncommitted, with no remote publication or deployment performed.

## Follow-up audit and fixture consolidation

A bounded [Cross-Examine audit](CROSS_EXAMINE_LEDGER.md) reproduced schema wrong passes and a complete-evidence recovery gap. It preserves original/repaired observations and independent review. The current native suite has 22 behavioral checks, including the repairs and workspace materialization; the original fifteen-check results above remain historical evidence.

`fixtures/playground/` is the canonical source, without nested Git metadata, generated skill copies, or run outputs. `new_workspace.py` creates a disposable local Git workspace and installs the current pack from its owning checkout. The former external checkout is preserved in an ignored legacy archive when this consolidation is applied. Historical receipts retain their original paths and hashes rather than being rewritten to look newly generated.

Replay the recorded original/repaired audit from the C Stack root:

```sh
python3 evals/hill-climb/cross_examine.py
```
