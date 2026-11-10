# Independent forward-use report

Used Ablation and Bitter Lesson without demo/test solutions. Sole grader: evaluate.py through simplification.protocol.

All cases are synthetic and exposed. This confirms local fixture outcomes and experiment mechanics, not real model performance.

| Run | Model | Units | UTF-8 bytes | PASS / cases |
| --- | --- | ---: | ---: | ---: |
| old-full | old-fixture | 9 | 4193 | 8 / 8 |
| old-no-plan | old-fixture | 7 | 4072 | 8 / 8 |
| old-no-example | old-fixture | 6 | 3990 | 8 / 8 |
| old-one-duplicate | old-fixture | 5 | 3903 | 8 / 8 |
| old-no-conflict-a | old-fixture | 4 | 3828 | 4 / 8 |
| old-no-conflict-b | old-fixture | 4 | 3821 | 4 / 8 |
| old-simple | old-fixture | 3 | 3746 | 8 / 8 |
| old-no-legacy | old-fixture | 2 | 3667 | 4 / 8 |
| old-no-duplicate | old-fixture | 2 | 3663 | 7 / 8 |
| old-alternate-duplicate | old-fixture | 3 | 3750 | 8 / 8 |
| new-full | new-fixture | 9 | 4193 | 8 / 8 |
| new-old-simple | new-fixture | 3 | 3746 | 8 / 8 |
| new-migration-simple | new-fixture | 2 | 3667 | 8 / 8 |
| new-contract-only | new-fixture | 1 | 3584 | 7 / 8 |
| confirm-old-full | old-fixture | 9 | 4193 | 4 / 4 |
| confirm-old-simple | old-fixture | 3 | 3746 | 4 / 4 |
| confirm-new-full | new-fixture | 9 | 4193 | 4 / 4 |
| confirm-new-old-simple | new-fixture | 3 | 3746 | 4 / 4 |
| confirm-old-migration-simple | old-fixture | 2 | 3667 | 2 / 4 |
| confirm-new-migration-simple | new-fixture | 2 | 3667 | 4 / 4 |

The old selected design retains contract, legacy-auth, duplicate-b. The migration design retains contract and duplicate-b.
Original-relative zero loss and zero pass regressions hold for both selected bundles on development and confirmation.
The identical legacy-free design fails old-fixture but passes new-fixture, exposing an actual fixture model/design interaction.
Single conflict removals fail, while deleting both succeeds. Removing both duplicate cues fails; at least one remains useful.
The alternate duplicate-a design is also feasible; duplicate-b wins the UTF-8 byte tie-break.

Accounting: 137/160 native case executions; 112 development + 24 reserved confirmation + 1 malformed-output control. 21 native run invocations. No actual provider, network or paid calls.

No observed skill-guidance error prevented execution. The guidance correctly disallows interpreting offline model names as real migration evidence. No skill ambiguity changed the decision. The native spec's task-score promotion rule also targets ordinary bug fixing; this prompt-ablation campaign explicitly uses the authorized burden objective and original-relative quality gate.
The adapter is deliberately one-shot and has no resumable state loader; this run completed, so recovery advice was not exercised. No operational cost reduction is claimed from prompt-byte changes.

Reproduce from this workspace (fresh output path required):
```sh
python3 eval-runs/forward_driver.py --out eval-runs/forward-repeat
```

Artifacts: owner-contract.json, proposals.json, result.json, rendered *.prompt.txt and *.diff; campaign/candidates contains executable snapshots and campaign/native contains native manifests, summaries, traces, outputs, and ledger. schema-control preserves the malformed native run.

Source identity: copied simplification/protocol.py SHA-256 `8d0abc3274b62c93d753728c09a29de1dfee54bef12d80f1b50b9edaa644cd15`. This isolated copy predates the parent-reported post-freeze live-plan mutation hardening; no live plan/contract/state mutation was used in this successful API execution. The parent fix is outside this observed run and no inference about its verification is made here. All copied source and native evidence remain unchanged.
