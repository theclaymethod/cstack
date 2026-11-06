# Does the eval measure its intended capability?

Partly. The suite independently checks artifact behavior, but the original executable proxy accepted submissions missing work that the skill is meant to perform. That is a conflict with the intent of the automated score. A complete reviewed skill pass was never established, and the existing report's human-review qualification still applies.

## Reproduced conflict

At public commit `41a14e4`, a stale-reset submission with no `attack.py`, a generic report, an unchanged generator skill, and a correct replacement reset received `executable_checks_passed: true`. The grader itself executed the reference solution and second reset to demonstrate the defect. The submission therefore did not have to supply either discovery evidence or a teaching change.

[before.json](evidence/intent-review-2026-11-06/before.json) preserves that result. [after.json](evidence/intent-review-2026-11-06/after.json) preserves the same submission's rejection under grader version 3. The grader now replays a submitted lifecycle artifact on both resets and requires the promised generator update. These checks establish necessary deliverables; they cannot judge a lesson's meaning or prove how discovery occurred.

## Other intent corrections

- Unexpected confirmed findings in clean/access controls now return an unscored result for independent adjudication. Seed labels are expectations, not authority over reproduced evidence.
- Every successful artifact report explicitly leaves `skill_evaluation_complete` false until reasoning, actual swarm use, provenance, and teaching quality are reviewed.
- The original pilot is labelled development evidence because its output influenced the grader and fixture. Its successful replay is not a fresh held-out result.
- Address update to order cancellation is described as near transfer in the same SQLite task family. The evidence does not show broad domain generalization or causal improvement from guidance.
- Transfer instructions allow confirmed source examples inside learned guidance. They withhold raw source artifacts and target answers; copying a lesson containing examples is not described as hiding every source-flaw detail.

## What remains unresolved

The development agents used unrestricted host tools under instructions, while only submitted artifact replay had enforced Docker boundaries. Run provenance and swarm use remain review obligations. No original-guidance baseline, repeated sampling, or fresh held-out variant suite was run. Post-hoc guidance hashes can establish document equality, not what a process actually read or an immutable pre-run commitment.

The [ledger](LEDGER.md) preserves those limits alongside the mechanisms actually tested. Version 3 calibration is machinery validation, not a new model-effectiveness result. Future scored runs must freeze versions before exposure and use fresh candidates and held-out tasks.
