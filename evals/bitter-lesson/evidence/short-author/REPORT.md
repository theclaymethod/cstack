The installed Bootstrap, Create Eval and Adversarial Cases skills were exercised locally to recover decisions, freeze a current handoff, author native cases, construct a pending contrast and execute controls. The approved package has exactly A revision1 and B revision2. Rejected A creation, superseded B guidance-only, deferred C revision1 and proposed P-01 remain outside scored authoring. No inverse approval was inferred. Earlier full proposal text was unavailable and was not invented.

`source/scripted-decisions.md` preserves the original task verbatim. `source/card-history.json` retains amendments and their scope. Read-only source records and hashes are separate from `author/`; these are same-host safeguards, not access isolation. `author/current-handoff.json` maps intent revision1 to the native runner. `verification/fidelity.json` establishes 2/2 exact full approved projections, including request text/account/accounts, counter7, the unrelated ticket and its metadata, family, revision and expected checks. Native schema validation passed. Original evaluator, spec, rubric, case suite and product hashes stayed unchanged.

Each control ran against both approved cases via `evaluate.py run --cases .../author/approved-cases.jsonl --suite development`. Every run passed the existing `evaluate.checked_run` evidence checker. Source, immutable snapshots, raw stdout, parsed output, commands, exit status, checks and summary are retained under `controls/` and `native/`.

| Actual control | A-r1 | B-r2 |
| --- | --- | --- |
| Legitimate implementation | PASS | PASS |
| Alternative unique ID plus harmless metadata | PASS | PASS |
| False creation claim without mutation | PASS | FAIL |
| Original product | FAIL | PASS |

`verification/state-witnesses.json` records every actual resulting state from captured subprocess stdout. Legitimate and alternative A preserve `{tickets: [], counter: 7}`. Their B outputs preserve the original `old` acct-b ticket and `metadata.keep=true`, retain counter7 and append one open VPN ticket for acct-a, with IDs `approved-control` and `another-valid-id` respectively. The alternative also retains its added metadata. False-claim B returns only the old ticket: ticket delta, new membership and action/mutation checks fail despite its success note. Original-product A wrongly adds `ticket-1` for acct-a; original-product B correctly appends `ticket-1` while retaining the original record and counter.

P-01 changes only B's explicit account to null, preserving both available accounts and initial state. Its clarification expectation is a construction proposal supported by the existing account rule, not an owner approval or an executed result. It remains unapproved and unrun; no fault was armed or injected, no activation or outcome witness exists, and no defect or recovery claim follows. No reduction was attempted.

Usage: 8/48 native case attempts, four runs, one fresh subprocess per case, no retries, errors or unknowns. No tests, source changes, added dependencies, nested agents, network, provider or paid calls. Runtime model tokens were unavailable and are not estimated. `usage.json` holds exact commands and accounting.

These are scripted synthetic expectation approvals, not real human gold labels on observed outputs. Native PASS/FAIL verdicts come from fixed deterministic checks. Controls were authored by this same local agent; scenario author, evaluator author, coordinator and validator were not independent. No private labels, held-out outcomes, semantic judge calibration, production prevalence or generalization is established. The native grader checks a nonempty note, not guidance helpfulness. Resulting-state evidence is the fixture's returned state, with no external database. The package is runnable contract-development evidence; pending intent and independent validation remain open.
