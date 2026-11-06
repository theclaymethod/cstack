# Cross-examining the evals

This is the historical development report. The later [intent review](INTENT_REVIEW.md) identifies gaps in its executable proxy and qualifies the pilot as development and near-transfer evidence. The [ledger](LEDGER.md) records corrections and open limitations; original results below retain their historical versions.

The suite contains five audit cases and a separate fresh-agent lesson-transfer stage. The outer grader replays artifacts in restricted Docker containers and independently reads SQLite outcomes. Executable results are separate from the review of reasoning, provenance, and lesson quality.

## What changed after adversarial review

| Finding | Evidence | Correction |
| --- | --- | --- |
| Default macOS temporary paths were not mountable by this Docker VM. | `evidence/environment/infrastructure-failure.json` | Scratch directories live inside the mounted workspace. |
| Clean submissions were compared with a different generator document from the supplied one. | `evidence/contract/report.md` | Compare with the exact materialized source document. |
| The protected-oracle control rejected a justified bounded clean conclusion. | `evidence/contract/report.md` | Accept clean or access-limited conclusions, with access reasoning reviewed separately. |
| A pilot returned structured replay evidence, but the grader required a string. | `evidence/model-audit-01/submission/finding.json` | Accept text, list, or object evidence and declare the schema. |
| Corrupting the writable database prevented the original reset from starting another attempt. | The pilot's `corrupt_database` evidence | Fixture version 2 reconstructs disposable database state; reset repair grading includes corruption recovery. |

The verifier lane also identified correlation between optional report artifacts and positive/negative probe labels. Its proposed proxy repair was not observed to pass the full original grader: early Docker file-handle failures also rejected valid probes. The repaired grader crosses optional claims with actual outcomes, and the negative proxy calibration is rejected. This is a strengthened probe design, not a claimed reproduced full-score bypass.

Repeated host-side unlink/recreate cycles also produced stale SQLite handles in the VM-backed bind mount. State seeding keeps file inodes stable, and verifier probes now use separate fresh workspaces. Fresh probes also prevent verifier counters or scratch state from carrying across examples.

The environment lane's two container checks found that evaluator scripts and the oracle resisted writes/replacement, and timed-out parent/child containers were removed. These are bounded checks, not a general claim about container security. Details and limitations are in `evidence/environment/report.md`.

## Calibration and model pilots

`evidence/release-calibration/summary.json` records the five reference audits, one deliberately insufficient proxy repair, one valid reference transfer, and one invalid success-flag transfer. Negative cases count as calibration successes only when the grader rejects them.

The instruction-blinded audit pilot received the original fixture under a neutral alias in a fresh context. It reproduced undeserved credit without the requested database update, rejected a valid direct-update alternative under the original verifier, and discovered the additional corrupted-state reset failure. It submitted repairs and generator lessons. Its artifacts are replayed against fixture version 2 in `evidence/model-audit-01/result-v2.json`; the original snapshot is preserved under `workspace/`.

The audit coordinator used one delegated read-only reviewer and executed two submitted candidates, plus lifecycle and repair checks. This was a smaller swarm than the default three independent attackers. The reviewer was `/root/model_audit/verifier_review`; it executed no attempts. The outer suite review separately used verifier, environment, and contract lanes. The verifier lane ended early after partial evidence; no unsupported result from that lane is counted as a successful attack.

A second fresh-context agent received only the revised generator skill and a new order-cancellation request. Its generated eval is replayed in `evidence/model-transfer-01/grading.json`. Both model pilot outputs passed their executable checks. This demonstrates one successful audit and transfer trajectory; no original-guidance comparison or repeated model sampling was performed, so this is not a causal estimate of improvement or a reliability score.

The pilot agents had unrestricted host tools with explicit path restrictions; their discovery runs were not OS-isolated. Submitted artifacts were independently replayed under enforced Docker mounts. Future scored model runs should use the operator-controlled execution boundary described in the README, retain full transcripts, and complete the listed human reviews. Prepared cases and calibration fixtures are available now; model audits of the other four cases remain unmeasured.

## Persisted lessons

The pilot updated its supplied `generator/SKILL.md`, and the transfer stage consumed that exact document. Confirmed reset, report-contract, and control-design lessons were also added to the original `~/.codex/skills/wargames/references/lessons.md` (now `~/.codex/skills/cross-examine/references/lessons.md`), routed from the skill entrypoint. The skill validator passed.

Run instructions and grading boundaries are in [README.md](README.md). Generate neutral case directories with `run.py prepare`; keep their operator manifest out of candidate context. Machine-specific paths in published evidence are replaced with `<repo>`.
