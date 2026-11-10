# Independent operator coverage observation review

Scope: frozen replay coverage validation of copied, previously generated evidence; no repaired implementation reviewed. I read probe_coverage.py and coverage-receipts.json, inspected the mutated coverage/command data and receipt existence, then independently ran frozen replay.validate on all three copies. No candidate executions, process interruptions, or protected source writes occurred. Attacker conclusions and other agent verdicts remain unseen.

## Adjudication

**Confirmed fixed-replay completeness gap.** Removing required observations or the native legitimate command receipt silently reduces the number of checks and still returns acceptance. The fixed replay explicitly constructs and checks named lifecycle scenarios and native controls; its acceptance should require that fixed coverage rather than iterate over whichever coverage entries remain.

| Copy | Independently observed omission | Independently observed replay result |
| --- | --- | --- |
| missing-one-lifecycle-observation | lifecycle-complete-stop-1 observation removed; three lifecycle observations remain | Accepts 64 checks |
| empty-lifecycle-observations | No lifecycle observations remain | Accepts 46 checks |
| omitted-command-receipt | native-legitimate absent from commands.json, and native-legitimate.receipt.json does not exist | Accepts 70 checks |

The retained receipts report native checked_run(native-legitimate) accepting all three. That is expected rather than conflicting evidence: its native run artifacts remain present, and validating that one legitimate run does not certify lifecycle observation coverage or the separate operator CLI receipt inventory. The reproduced defect is in the replay's broader fixed-construction completeness gate.

## Why the omissions matter

In replay.validate, lifecycle properties are checked only inside a loop over lifecycle-observations.json. The code has no independent required-label/multiplicity condition. Omitting one entry skips that scenario's boundary/recovery checks; an empty list skips all such checks, including activation/action pairing, pre-completion state, recovery, noactivation control and incomplete-evidence control. Final aggregate trace/interruption counts still pass because the probe retains all actual underlying campaign and activation artifacts. Their presence and counts do not substitute for the omitted targeted assertions.

Similarly, command exits are checked only for entries that remain in commands.json. Removing the native-legitimate entry skips its expected process-exit check, and the separate matching receipt is not required by that path. The actual native run still exists, so this does not prove it never executed; it demonstrates that required command/receipt evidence is missing without the validator rejecting incomplete evidence.

These are relevant to the original scope. Exercise08 requires a lifecycle fault, scoring case, clean and legitimate controls, a noactivation control, actual activation/outcome evidence, and reset/replay. The frozen replay is intentionally narrower than a general shared-skill judge, but those exact named controls are its own fixed declared construction. Requiring their coverage therefore preserves its existing question; it does not add an expectation that it semantically judge arbitrary skill behavior.

## Classification and limits

This is extra-operator evidence-calibration, not a candidate exploit. The supplied teaching proxy is not involved. No observation here proves that the original builder omitted a run, that an activation failed, that protected source was changed, or that the shared skill fails to construct cases. The artifacts are deliberate incomplete copies of real generated local development evidence. The honest result for those copies is incomplete validation evidence, even when surviving native data independently remains valid.

This finding is naturally grouped with the source-inventory and stdout/output observations in operator-validator-observation-review.md: all concern the replay accepting incomplete or incoherent proof of its fixed checks. It does not need three separate semantic defect claims merely because three omissions skip different loop bodies.

No repair verdict is issued. A later patch should preserve fixed scenario membership and required command/receipt coverage, reject these incomplete copies, and continue accepting the pristine clean construction with legitimate alternatives and honest noactivation/incomplete lifecycle controls. Merely enforcing a check-count threshold would be a proxy for the missing obligations; the required identities and evidence should drive validation.
