# Lessons and evidence status

This reference records the operational lessons supplied with Co-Climb. They are guidance, not newly verified campaign findings: no campaign outputs, measurements or adjudication receipts accompanied the supplied skill. Do not cite this file as empirical validation.

## Preserve these checks

- **Missing evidence can reward omission.** Compare the actual target and judge records before treating an unsupported-output finding as a target defect. A parity repair versions the judge.
- **A target win is relative to a judge build.** Re-judge saved outputs after judge changes and revalidate retained edits. Do not pool scores across judge versions.
- **Noise can reverse a small gain.** Keep identical controls on both working sets and replicate a candidate before it becomes the base. A gain on one set alone is a tie.
- **A dominant cluster can hide other failures.** Triage major findings and abstentions, inspect passed outputs for the same defects, and deterministically check a cluster claim before bulk row creation.
- **A proposed label is not an expert answer.** Keep uncertain cases out of calibration, preserve actual authority, and retract rows shown to be wrong without erasing their history.
- **Calibration can drift into easier criteria.** Compare every rebuild with the original judge and trace loosenings to confirmed evidence or an owner decision.
- **A clean in-loop judgment may disagree with final scoring.** Check artifact and evidence identity, then measure repeated judging before attributing the gap to noise or adding passes.
- **Final evidence stops being sealed when used.** Freeze before the once-only comparison and never feed those results back into tuning under an unseen-evidence claim.

The [protocol](protocol.md) gives the execution and evidence requirements for these checks.

## Add a confirmed lesson only with evidence

For a new finding, record the faulty assumption, observed divergence, exact record/output and target/judge versions, reproducer or comparison, adjudication source, and the narrow rule supported by that evidence. Include legitimate controls, contradictory results and limits. State whether evidence is synthetic, agent-derived or human-reviewed.

Keep hypotheses in the project's decision ledger until confirmed. Private records and project-specific runners stay project-local; a portable lesson should link to an authorized evidence location or describe how to reproduce the mechanism without copying private data. If supporting evidence cannot be shared, say what remains unverified for the reader.
