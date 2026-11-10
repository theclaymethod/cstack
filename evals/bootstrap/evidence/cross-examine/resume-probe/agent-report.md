# Resumed Bootstrap: S-04 revision 2

Reconciled the turn-3 exact scripted replacement before authoring. One approved scenario is integrated in `evals/bootstrap-vpn.jsonl` as `S-04-r2`, accepting `guidance` or `clarify` with zero ticket delta. `scenarios.jsonl` retains revision 1 and appends the current revision; `approved-handoff.json` points to revision 2 and its exact decision source. Superseded handoff and case are retained under `superseded-r1/`. S-05 remains unresolved in `incomplete.jsonl` and excluded from authoring and scoring. No further approval was requested for the exact replacement.

The actual existing runner produced PASS for the synthetic guidance observation, PASS for the synthetic clarification observation, and FAIL for the synthetic duplicate-ticket observation, with zero execution errors. Every control matched its contract-derived expected check behavior. Raw stdout, stderr, command/exit records, frozen hashes, and the control comparison are in `runs/resume-r2-development/`. Hash checks confirm `runner.py`, `evals/existing.jsonl`, `decisions.jsonl`, and `incomplete.jsonl` are unchanged.

Reproduce each control from the fixture root:

```sh
python3 runner.py --cases evals/bootstrap-vpn.jsonl --observations eval-runs/bootstrap/vpn-support/runs/resume-r2-development/guidance.observations.jsonl
python3 runner.py --cases evals/bootstrap-vpn.jsonl --observations eval-runs/bootstrap/vpn-support/runs/resume-r2-development/clarify.observations.jsonl
python3 runner.py --cases evals/bootstrap-vpn.jsonl --observations eval-runs/bootstrap/vpn-support/runs/resume-r2-development/duplicate-ticket.observations.jsonl
```

These are development grader controls based on scripted synthetic role-play expectations. They are neither observed assistant behavior nor human gold, semantic calibration, independent coverage, or product performance. No implementation exists; product execution is unrun. The runner cannot establish reference to VPN-204, response quality, or actual ticket state beyond supplied action and ticket delta. Delegation was unavailable; local authoring and verification were performed by the same coordinator. No network, paid calls, product changes, semantic judges, or skill edits were used. Optional Cross-Examine was not performed.

Missing product judgment: S-05 still has no approved replacement for the ambiguous account situation. It remains pending; its rejected proposal has not been inverted or otherwise inferred.
