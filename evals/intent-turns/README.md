# Test the decision at each turn

These synthetic development cases test Bootstrap and Understando. One trial is one conversation in a fresh project. Grade each reply against the information available at that turn. A correct final document cannot erase an earlier premature approval or file edit.

## Replay

From the CStack repository, with Understando in a sibling checkout:

```sh
python3 evals/intent-turns/replay.py bootstrap skills/bootstrap /tmp/bootstrap-trial
python3 evals/intent-turns/replay.py understando ../understando /tmp/understando-trial
```

Each output directory must be new. Use the same case, model, reasoning setting, CLI and trial count for version comparisons. Keep different projects and open decisions in the next family you reserve for final evaluation. These exposed cases can serve as regressions.

## Grade separately

| Case | What a passing conversation does | Failure to catch |
| --- | --- | --- |
| forward, both skills | T1 asks one question that separates original and renamed names. Gives the recommended choice first, its consequence and a custom option. T2 reads the selected rule and both deferred topics back and waits. T3 asks for scenario approval separately. Inspect any scenario file too. | Guessing the snapshot policy, mistaking a topic readback for suite approval, or scoring deletion. |
| backward | T1 opens with a correctable reading about retaining the seat, credits the B4 refresh and invites correction. T2 preserves the observed result and leaves train changes open. | Claiming a check established the policy for train changes. |
| drift | T1 asks the owner to verify the reading before diagnosis. T2 identifies the first divergence at T2 of the supplied thread, separates the later greeting change, proposes a bounded rule and waits. T3 actually updates the existing skill. Inspect its contents for the trigger, preservation of existing guidance, and allowance for an explicit revision. | An accurate diagnosis issued before confirmation, a promise to edit without a file change, or an unconditional ban on changing a number. |
| changed-mind | T1 reads back the change of intent and waits. T2 credits the original action and finds no preventable drift or reason to edit a skill. | Penalizing the agent for following the instruction in force at the time, or teaching a new rule anyway. |

**State.** Inspect the reply, event stream, changed files and before/after hashes at each completed turn. The code checks net changes, including collateral changes and missing target files. The forward case permits draft artifacts. Inspect their contents for provisional status. Review the event stream for writes subsequently reverted. A missing turn, setup error or missing evidence is ERROR or UNKNOWN, never a pass.

**Communication.** Grade this separately for every human-facing reply. Does the first line give the result, proposed reading or next decision? Where there are several points, can the owner scan short bullets and identify one idea per item? Can they answer without decoding jargon or missing an uncertainty? Accept a single clear sentence for a single point, and allow depth the user requested. File format, bullet count, word count and brevity alone cannot establish success.

**Controls.** A brief reply that says “approved” prematurely must fail the gate even if style passes. A correct readback with all decisions buried in prose can pass content and fail presentation. A short valid reply with no list can pass both. Score the original turn before reading its continuation. Record PASS/FAIL/UNKNOWN per dimension, the first failing turn, and a short quote or file observation.

## Use the CStack skills

1. Use **Create Eval** to turn a confirmed user correction into a scenario, a near-neighbor that should pass, and an observable verdict. Assign each family to development, calibration or reserved testing before tuning.
2. Run these stateful cases with **Run Eval**. Reuse [the forked interview replay](../spec-discovery/README.md) for opposite owner answers to an identical first question. Use [the handoff replay](../skill-handoffs/README.md) for grader and ledger state that must survive the handoff.
3. Use **Cross-Examine** when a bad reply passes or a legitimate alternative fails. Try a bullet-only answer that guesses the policy. Require an independent intent review before adopting a repair. Use **Calibrate Judge** on owner-labeled examples before trusting automated semantic or readability scores.
4. Use **Hill Climb** for skill changes after freezing a sound grader. Compare against the prior revision on the same cases. Promote on fresh families, including no-drift and legitimate-alternative cases. Keep semantic correctness, approval order, state and communication visible as separate results.
