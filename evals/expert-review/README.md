# Expert-review evals

These synthetic conversations evaluate [Expert Mode](../../skills/expert-mode/SKILL.md) and [Distill Me](../../skills/distill-me/SKILL.md). They measure faithful capture of an expert's judgments, not independent domain expertise. All examples are invented; none contain patient data.

The suite uses local JSONL, Markdown, and Python's standard library. No database, Docker, model API, or third-party package is required. It parses candidate data and never runs candidate programs. A host agent still has its ordinary permissions: the access restrictions below are instructions, not a sandbox.

## Cases

| Case | Behavior being evaluated |
| --- | --- |
| `live-correction` | Immediate negative capture; later expert correction; agent proposals stay unendorsed; preserve the original output; stop capture when asked. |
| `live-uncertainty` | Tentative concern stays uncertain; a scoped criterion becomes a binary question; a missing replacement remains unresolved; a preference is not a factual error. |
| `distill-merge` | Merge existing live capture; preserve history; repeated invocation adds nothing; retraction is linked; retrospective invocation does not activate ongoing capture. |
| `distill-source` | Silence, agent self-repair, and archived instructions do not become expert endorsements. |
| `activation` | Discussing the skill is not activation; starting the mode does not backfill earlier judgments automatically. |
| `partial-context` | Report missing originals honestly; retain at most a clearly provisional summary observation or report the gap without a confirmed row. |

These are development cases. They are public and small; they do not establish held-out performance, probability calibration, or generalization across products or experts.

Current results: **19/19 calibration controls** pass. The first six-case agent pilot passed five artifact graders; a focused rerun exposed and helped repair another false rejection. Its unchanged output passes the current grader. See the [results and limits](REPORT.md).

The companions also support [local exports for eval authors](../../skills/expert-mode/references/export.md), with optional [Privacy Filter setup](../../skills/expert-mode/references/privacy-filter.md). Separate [export receipts](evidence/export-local/receipt.json) cover the real local CLI and simulated redaction adapter; no model weights or PII-detection performance were tested. A [synthetic handoff](evidence/export-local/synthetic-bundle/findings.json) shows the output format and retains an unresolved concern separately from a supported source-naming error.

## Run a case

From the repository root, create two fresh sibling directories:

```bash
python3 evals/expert-review/run.py prepare live-correction \
  eval-runs/expert-pilot/work eval-runs/expert-pilot/operator
```

Give a fresh candidate only `work/REQUEST.md`, the revealed `source.json` and `CURRENT_TURN.md`, the supplied skill guidance, artifacts, and dataset. Do not supply this README, fixture/grader code, calibration answers, prior results, future turns, or the operator directory. The candidate reads the new turn and updates its dataset and `reply.md`. It cannot supply its own checkpoint receipts.

The operator then captures the actual files and reveals the next turn:

```bash
python3 evals/expert-review/run.py capture eval-runs/expert-pilot/operator
```

Continue until `next_turn` is null, then grade:

```bash
python3 evals/expert-review/run.py grade eval-runs/expert-pilot/operator
```

The `capture` command belongs to the operator. Do not let a candidate batch future captures or write fake checkpoints at session end. For retrospective cases, the first revealed source includes the bounded session leading up to invocation. A new directory pair is a clean reset; the runner refuses to reuse an existing pair.

The adapter in `candidate.md` declares the JSONL fields, exact source-quote convention, and correction normalization required by these artifact checks. It is a test adapter, not a required production schema. Keep the installed skills and their relative shared reference together when using them in Claude, Codex, or Cursor.

## Review the actual skill behavior

`artifact_checks_passed` covers records and their observed changes. It is not a full skill verdict. Review each checkpoint's real files and replies, and record yes, no, or unreviewed with evidence for these questions:

1. Does every captured label and correction preserve the expert's actual meaning, scope, conditions, and original reviewed output?
2. Does each rubric question express one supported binary criterion with the correct passing answer and applicability, leaving invented thresholds and inferences provisional?
3. Are replies concise and useful, and are clarifications limited to questions that materially improve the example rather than asking the expert to supply observable facts?
4. Does the execution record support the claimed source coverage, activation state, and any claimed independent review? Were only authorized sources used?
5. Are incomplete and summary-derived observations honest about their provenance and replay blockers? Does any claim of replay readiness have recoverable context and an observable criterion?

An applicable no means the skill did not fully succeed; an unreviewed answer leaves the verdict incomplete. Use checkpoint paths and exact excerpts as evidence. Multiple reviewers agreeing on one expert quote do not create another expert endorsement. Do not give a clinical truth score for this synthetic capture task.

## Calibrate and cross-examine

```bash
python3 evals/expert-review/calibration.py eval-runs/expert-calibration
```

Calibration uses hand-authored references and insufficient-output controls. It validates the grading machinery, not a model. The [ledger](CROSS_EXAMINE_LEDGER.md) records the bounded adversarial round, original and repaired outcomes, and the final intent review. Preserve frozen grader, request, fixture, guidance hashes, candidate artifacts, and operator receipts for each model run. Runs used to revise the grader remain development evidence.

Replay the four preserved reviewer submissions against either revision:

```bash
python3 evals/expert-review/replay.py eval-runs/expert-replay-current
python3 evals/expert-review/replay.py eval-runs/expert-replay-original \
  --grader evals/expert-review/evidence/round-1/frozen/run.py
```

The original grader awards artifact credit to seed deletion and an incomplete rubric, and rejects two valid alternatives. The repaired grader reverses all four outcomes. [Before/after receipts](evidence/round-1/before-after.json) retain those original failures rather than relabeling them as successes.

Replay the pending-criterion alternative and the focused candidate's actual files:

```bash
python3 evals/expert-review/replay.py eval-runs/expert-pending \
  --submissions evals/expert-review/evidence/pending-rubric-v3/submission.json
python3 evals/expert-review/replay.py eval-runs/expert-focused \
  --submissions evals/expert-review/evidence/pilot-v3/pilot.json
```

Replay operates on preserved data; it does not rerun a model. Its command succeeds when replay completes; inspect the per-case grades rather than interpreting its exit status as skill success. To reproduce a model run's original grading, use that evidence directory's `frozen/evals/expert-review/run.py` with `--grader` and its `pilot.json` with `--submissions`.

This suite does not access application conversation databases, publish expert data, or automatically modify product code. Real expert-review datasets stay in the working project's private storage.
