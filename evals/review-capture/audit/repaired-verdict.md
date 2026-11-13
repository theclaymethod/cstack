# Independent frozen-repair acceptance

## Verdict

**Accepted for the demonstrated archive-adapter defect and its three frozen witnesses.** This is bounded acceptance of the repaired archive checker, not validation of a general capture runtime or malicious-writer containment.

I read the frozen `review-packet-repaired` checker and independently reran it against all four supplied archives. I did not read repair reports, implementation commentary, tuning history or proposed verdicts. Comparing all pre-existing files in each original archive to its repaired counterpart found only `verify_archive.py` changed; the raw evidence used for each replay was preserved.

| Archive | Independent repaired result | Interpretation |
| --- | --- | --- |
| Original valid archive | Exit 0, `verified: true` | Valid capture history, current consent/proposal distinctions and empty current eligible handoff remain accepted. |
| H1 altered original state | Exit 1, `initial-state-mismatch` for `false-claim-v1` | Detects the saved state's disagreement with native input. |
| H2 substituted reviewed output | Exit 1, `native-output-mismatch` for `false-claim-v1` | Detects the saved output's disagreement with the native trace, despite agreeing derivative previews and refreshed hashes. |
| H3 fabricated verbatim statement | Exit 1, `verbatim-source-mismatch` for `capture-forward-signal-1-v1` | Detects that the purported original quote is absent from its retained source. |

The checker now compares copied input, output, initial state, resulting state and stdout against the retained native record for both frozen candidate versions, links record artifact references to their declared frozen version, and checks declared verbatim scripted quotes against their hashed source. The JSON comparisons for native input/output/state preserve insignificant JSON serialization differences. Quote checking is conditional on a verbatim claim, so it does not impose literal quotation on every narrative record. These are appropriate checks for this archive's declared evidence contract.

## Legitimate behavior

I additionally executed the two preserved candidate programs on their retained native inputs, without modifying their evidence. Both exited 0 and reproduced their original parsed native outputs. The false-claim candidate created zero tickets and the legitimate alternative created one. Their retained native FAIL/PASS outcomes remain accepted by the repaired baseline checker. These were two additional local candidate invocations, not new model inference, provider calls or fitted judgments.

The repaired baseline still verifies ten total records, the preserved unrelated record, append-only history and retraction, stopped old scope, separate evidence-only consent for the new scope, unconfirmed agent-proposed labels, inactive Expert Mode, one incomplete candidate, six exclusions, and no current eligible/runtime/human-gold rows. I observed no new restriction on those legitimate outcomes.

## Limits

The three corruptions were operator changes to disposable evidence copies; native candidate authority to make them was not demonstrated. The repair detects inconsistencies against retained native/source anchors, not authenticated replacement of all anchors by a malicious writer. A quote's presence in a source establishes only the checked textual membership; this packet does not establish comprehensive semantic attribution, source-item scope, or authority validation for arbitrary new records.

The archive adapter has a fixed two-version fixture contract. Passing this audit does not establish support for arbitrary future capture schemas, amendments or candidate versions. Historical phase adapters and original raw checker remain historical evidence; this acceptance concerns the new archive checker alone. The current empty eligible set means this audit demonstrates preserved evidence integrity and correct rejection on the supplied probes, not calibrated judge accuracy or release readiness.
