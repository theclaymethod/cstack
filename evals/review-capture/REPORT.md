# Review judgments for judge calibration

Reviews now offer to retain corrections and confirmed labels as calibration candidates. The shared [capture guide](../../skills/expert-mode/references/calibration-capture.md) supplies the consent, evidence and authority rules; nine skill entrypoints route to it. Expert Mode and Distill Me reuse their existing records. No new installed runtime or universal dataset schema is added.

A coordinator makes one scoped offer at a natural review checkpoint and continues authorized work while it is pending. Agent-led corrections can be offered as evidence and proposed labels. Consent to save does not confirm those proposals, enable Expert Mode, authorize fitting or publish a dataset. Existing explicit judgments need no second label approval. Original outputs, criteria, authority, source-family exposure and subsequent retractions stay recoverable. Calibrate Judge receives eligible rows plus explicit incomplete/excluded queues; intent approvals and agent findings do not become human gold.

## Fixture evidence

A fresh host-agent context used installed skills in a disposable playground workspace. All reviewer statements were scripted synthetic roles. It ran the native evaluator on two real subprocess candidates: a false ticket-creation claim failed, while an alternative that created a ticket passed. It then exercised six capture phases with project-local serializers and checkpointed artifacts.

| Checkpoint | Store records | Eligible | Incomplete | Excluded |
| --- | ---: | ---: | ---: | ---: |
| Offer before retention consent | 1 existing seed | — | — | — |
| Scoped retention, explicit synthetic-only policy | 6 | 1 | 1 | 3 |
| Exact replay | 6 | 1 | 1 | 3 |
| Label retraction and capture stop | 8 | 0 | 1 | 4 |
| New agent-led scope, offer pending | 8 | 0 | 1 | 4 |
| Evidence-only retention, no label confirmation | 10 | 0 | 1 | 6 |

The first offer left the existing store unchanged. Replay added zero records and reproduced the handoff byte-for-byte. Retraction preserved the historical FAIL but removed its current eligibility. The stopped scope rejected further reusable capture. The new scope did not inherit consent; subsequent evidence-only consent saved two proposals with `label=null`, preserving agent/verifier origin. No phase produced human-gold rows or activated Expert Mode. The initial nonempty runtime preview contained only allowlisted task evidence and an opaque item ID; labels, quotes and private metadata stayed in the comparator. Later empty previews follow an explicit exclusion inventory.

The [raw exercise report](evidence/workspace/eval-runs/capture-forward/final/report.md), [verification](evidence/workspace/eval-runs/capture-forward/final/verification.json), phase snapshots, consent records, offers, original traces and serializers are retained. The read-only verifier checked 99 checkpointed artifact hashes, the native witnesses, append-only history, retractions and runtime projection. Root independently reran verification and inspected the source, handoff queues and native evidence. The [archive manifest](evidence-manifest.json) records raw file hashes. Historical absolute paths are provenance, not portable commands.

From a C Stack checkout, verify the archived evidence without product/model execution:

```bash
python3 evals/review-capture/verify_archive.py
```

This small archive adapter relocates the original read-only verifier and checks archived final guidance instead of its original live workspace/staged paths. The original verifier remains unchanged in the archive. Phase drivers are one-time development fixtures; use a fresh disposable workspace and [exercise 13](../../fixtures/playground/exercises/13-review-calibration-capture.md) for new runs. The serializers are examples of project-local adaptation, not a capture product or installed library.

## Controls and limits

All eleven existing [control groups](evidence/controls/summary.json) passed. Native playground tests: 55 passed, one optional DSPy SDK test skipped. All eleven [skill structural checks](evidence/skill-validation.json) passed. This feature changes Markdown guidance and package metadata; task specs, native evaluator, support agent, supplied cases and graders remain unchanged.

The behavioral run used 2 of 24 permitted native cases, with no paid/provider calls, fitted judges, uploads or releases. Phase 1 used an earlier trigger wording; its preserved guide hash is `0f36c1785a980e21c32d88a7604d469cf0173f70b688ae4d93ebfa325d1f55b7`. Before phase 2, explicit synchronization installed expanded agent-led triggers, final hash `91ad849b5326d80203a3c9fe76c651dfd85a609f15801878fd85ecbac8fc0886`. Both source versions and the boundary are preserved. This is iterative exposed development, not a frozen generalization test or a completed independent Cross-Examine audit. The scripted rows demonstrate mechanics, not real expert calibration, production adequacy or deployed judge quality. No judgments from the actual user chat were captured by implementing this feature.
