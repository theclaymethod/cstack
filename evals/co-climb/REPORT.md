# Co-climb optimization report

Validated 2026-11-13. Original skill: `03eeb4bc95ad89d805b008a8165a89cceafc9cc1`. Selected skill: `a9e3504` (exact identities and hashes in the live manifests).

## Verified result

The improvement is prompt efficiency with preserved decision accuracy, not higher accuracy or proven end-to-end campaign effectiveness.

| Final frozen comparison | Original | Selected |
| --- | ---: | ---: |
| Correct decisions across three batches | 48/48 | 48/48 |
| Full skill-bundle characters, including section paths | 14,347 | 11,475 |
| Measured input tokens across three batches | 65,168 | 63,018 |

The bundle is **20.018% shorter** and measured input use is **3.299% lower**. Each paired run used fewer candidate input tokens: 21,006 versus 21,782 / 21,604 / 21,782. Input totals include host context, so bundle-size reduction and total-input reduction are different measurements. Cache hits differed; no dollar-cost or latency improvement is claimed.

The efficiency gate was declared before the final run: all 48 candidate decisions pass, no regression, at least 20% fewer bundle characters, and fewer input tokens in every pair. The selected candidate passed all conditions. Three repetitions of sixteen cases are not 48 independent source cases.

[Full results](evidence/live/summary.json), [frozen final manifest](evidence/live/paired-v4/manifest.json), and per-run final responses/receipts preserve the comparison. No internal reasoning or environment logs are published.

## Search and eval repairs

1. **Initial comparison (V1):** GPT-6 Astra, high reasoning, three fresh-context pairs. Original and first revision each scored 45/48. No improvement claim or merge followed.
2. **Eval review:** the judge-choice case omitted J2 from its available-ID list; the archive gate rejected retaining A while awaiting regrading. Both were repaired symmetrically. Previous results remain preserved under their original hashes.
3. **Handoff revision (V2):** made unsupported judge selection explicitly unresolved. Original and revised both scored 48/48 on the repaired suite. Accuracy remained tied.
4. **Efficiency phase:** reduced duplicate entrypoint, protocol, prompts and lessons text while preserving the safety/measurement boundaries. A draft V3 failed the declared size threshold and was stopped; its two model turns completed but the second receipt was not finalized. These partial results are excluded from confirmation. The runner now checks the size gate before launching calls.
5. **Final comparison (V4):** the shorter candidate passed the frozen efficiency gate above. Eval data/grader stayed unchanged from V2.

Across all phases, **20 model calls started and 20 model turns completed**. Nineteen received complete grading receipts; the stopped V3 candidate did not. None of the confirmed runs used tools. Final responses, observed usage and incomplete-run status are retained, including non-improving trials.

## Runtime and scope

The CLI was `codex-cli 0.167.0-alpha.4.1`; model `gpt-6-astra`, reasoning `high`. Each batch received the same decision-task prompt, cases and versioned skill bundle in a fresh context. Baseline/candidate order alternated. User config was ignored, shell/web disabled, answer keys excluded, and observed tool use invalidated a run. Each context answered all sixteen scenarios; these are decision tasks, not an adversarial host-isolation test or a native campaign.

The skill now distinguishes exploratory branches from confirmed promotions, bounds branch retention, versions judge changes, requires evidence-backed judge selection, and provides coordinator/target/judge handoffs. It preserves controls, label authority, evidence parity, regrading, fresh execution after in-loop changes, and sealed final confirmation. The shortened entrypoint delegates detailed rules to the protocol instead of repeating them. Installed content remains Markdown only.

## Other validation

Nine grader tests passed: all sixteen reference decisions, legitimate alternatives, unsafe actions, omissions, evidence-order errors, malformed/duplicate responses, incomplete coverage, CLI and prepared-input boundaries. Controls reject 33 offered unsafe-action additions and 35 required-action omissions. The existing playground suite passed 56 tests with one skipped. Skill frontmatter and relative links passed.

## Limits

The sixteen cases are exposed synthetic development scenarios with authored contract answers, not human-gold campaign data. This adaptive optimization and its repeated confirmation do not establish unseen generalization, actual target/judge quality, reliable production optimization, or statistical significance. No native end-to-end co-climb campaign was benchmarked. A fresh-family execution suite is needed for those claims.

## Bounded cycles and case quality

One fresh GPT-6 Astra session per version answered the same expanded 20 decision cases. Both the previous release (0a43994) and the revision passed 20/20. Nine existing grader controls passed. The added decisions cover a judge-first start, an attacker-first repair and generator replay, distinguishing material from cosmetic challenges, and stopping after the agreed cycles even when budget remains. These decision results establish no comparative accuracy gain. [Answers and grades](evidence/cycle-comparison.json)

A separate local exercise ran the revised skill against two Python functions. The starting generator printed the unit price and the evaluator accepted any string beginning with the receipt prefix. The owner permitted all three display forms of a whole-dollar total, authorized two cycles and 80 judgments, and requested no promotion. One reviewer wanted exactly two decimals. Another suspected a calculation error for three items.

The run rejected the formatting restriction, retained all three valid forms as controls, and tightened the evaluator to check the amount. For three items at two dollars it rejected the old generator’s two-dollar receipt. After the generator change, four of four working examples produced accepted correct totals, up from one of four with the same strengthened evaluator. We separately replayed all 38 judgments against the recorded versions. This exercise used deterministic synthetic inputs and no holdout. Its receipt records trials and observations; the final answer supplied the formatting rationale. The harness wrote that answer to the same path the agent linked as its audit summary, so this run alone cannot establish what the original summary contained. [Source snapshots and observations](evidence/receipt-campaign.json)

A second fresh campaign saved the chat reply outside the workspace. Its [actual ledger](evidence/receipt-ledger.md) links the two reviewer suggestions to controls, an admit/reject rationale, generator trials and their replays. It retained a pruned generator trial. It also admitted a one-dollar arithmetic discrepancy at an extremely large price. The unrestricted synthetic arithmetic contract supports that distinction. Its operational priority for a real merchant remains unestablished. The run stayed within two cycles and 52/80 judgments, although one experiment exceeded its own estimate by four judgments.
