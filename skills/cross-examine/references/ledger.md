# Maintain the reward-hacking ledger

Keep a project-owned record of the mechanisms encountered and the evidence that a prevention works. Use an existing eval ledger when present; otherwise create `CROSS_EXAMINE_LEDGER.md` beside the eval. Keep reusable generation rules in the generator skill or lessons reference, linking to ledger evidence rather than duplicating the incident history.

Use Markdown on local disk by default; no database or service is required for this ledger. Record the chosen runtime, storage, isolation boundary, and why any heavier tool is necessary. Distinguish enforced access restrictions from instructions given to a host process.

Before a run, read the relevant records and write the intended capability independently of the current verifier. Preserve the original contract and artifact versions. For a scored run, record commit IDs or content hashes for the grader, request, and provided guidance, plus whether the run is development, calibration, or held out. Keep operator receipts outside candidate access.

For each distinct mechanism, record:

- **Intent and gap:** what the eval should measure, the shortcut or bad pattern, and why its signal diverges from the intended outcome. Distinguish reward hacking from infrastructure errors and grader false rejections.
- **Observation:** the original version, candidate permissions, minimal reproducer or command, actual task state, verifier result, and evidence location. Record unexecuted ideas as hypotheses.
- **Prevention:** the concrete change and the legitimate behavior it must preserve.
- **Validation:** replay command, repaired outcome, valid-baseline outcome, version tested, and remaining surfaces. Mark a mechanism prevented only for the conditions actually replayed; a proposed correction stays unverified.
- **History:** dated observations and later validation or regression entries. Group by root cause, preserve earlier evidence, and append corrections instead of rewriting a failed run as a success.

Close each run with an intent review. State whether the evidence establishes the intended capability, only a narrower proxy, or a conflict with the contract. Explicitly check candidate-authored reproduction, actual swarm behavior, preserved outcome criteria, access boundaries, teaching artifacts, and claim scope. For transfer, distinguish a related task from broader generalization; a causal improvement claim requires a comparable original-guidance baseline. Learned examples may be provided as instruction, while raw source artifacts and target answers remain outside candidate access.

Record clean controls as bounded observations, not proof of immunity. A no-finding run need not invent a prevention. Keep ledger wording factual: “the replay rejected this forged artifact and accepted the baseline” is supported; “reward hacking eliminated” is not.
