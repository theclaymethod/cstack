# Shared eval decisions

Use one decision ledger per eval project or campaign. On entry or resume, read the latest relevant entries and follow their evidence links. Reuse the ledger named by the caller or already used for that work, including an existing P-Stack decision log. When work first needs a handoff and has no ledger, start `decisions.tsv` beside the eval artifacts. Use the project's existing format. For a new TSV use `ts`, `phase`, `decision`, `why`, `evidence`, and `result`.

Append a short entry when a decision, experiment or challenge changes what someone should do next. Give the reason, link the scenario, situation, row, trace or trial by its existing ID or path, and record the observed result or open question. Keep rejected cases, failed trials and reversals. Correct an earlier entry by appending a superseding decision. On retry, check the previous entry and receipt before repeating work.

The ledger points to evidence. Keep the scenario index, situations, native eval rows, raw receipts and protected labels in their own artifacts. Respect their access boundaries when sharing a pointer. At handoff, give the next skill the same ledger path, relevant IDs and the decision still needed. The receiving skill appends its result there.

For example, Adversarial Cases records why an unselected note must survive archiving. Create Eval follows the situation ID and records the new row and control results. Run Eval appends the actual run receipt. Hill Climb can pick up the failing row without reconstructing the developer's intent.
