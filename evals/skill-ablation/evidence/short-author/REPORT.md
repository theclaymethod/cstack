# Skill exercise: approved VPN authoring

The two current approved cases were authored faithfully in native JSONL and exercised with five control implementations: **10 native case executions of 48 allowed**, 0 execution errors, 0 unknowns. Legitimate and alternative-ID controls pass both cases; false creation claims fail both. All original evaluator/spec/rubric/cases and product source hashes remain unchanged.

## Authority and handoff

`source/scripted-decisions.md` preserves the exact task and synthetic owner decisions. `source/card-history.jsonl` preserves the rejected earlier creation proposal for A, approved A revision1, rejected/superseded B revision1 guidance, exact corrected approved B revision2, and deferred C revision1. Unknown historical wording is explicitly unspecified, never reconstructed as an exact quote. No rejection was converted into approval of its inverse.

`handoff/intent-v1.json`, `current-approved.jsonl`, and `authoring-handoff-v1.json` freeze the approved current intent and runner mapping. Source decisions/history and approved cards are outside `author/`, with read-only source copies and recorded hashes; these are procedural protection, not a security boundary against the same local operator. Approval sources are **scripted synthetic expectation authority**, not real human gold. No concrete output was supplied with a human outcome label.

Approved: A revision1 and B revision2 (2). Deferred: C revision1 (1). New proposed boundary: P-01 revision1 (1), also unapproved and unexecuted. Stale/rejected expectations are excluded. `handoff/pending-excluded.json` names each exclusion.

## Fidelity and runtime mapping

`author/approved.jsonl` contains exactly two cases. Native schema validation and comparison with frozen approved cards preserve exact request text, selected account, available account order, full initial state, expectations, and construction family (`author/fidelity.json`). A keeps account null, tickets empty and counter 7. B starts with the exact unrelated `old` acct-b open VPN ticket including `metadata.keep=true`, counter 7, and requires one new open VPN ticket for acct-a with any unique nonempty string ID. No canonical suite was edited.

The native runner owns schema, action/account, count/membership, new-ticket fields, unique IDs, prior ticket order/content, action/mutation consistency, and other-state preservation. It accepts any unique ID, rather than a reference naming pattern. The required explanatory note is nonempty, but usefulness or correctness of guidance prose is not semantically graded. This limits the capability measured.

## Actual native controls

| Control | A revision1 | B revision2 | Resulting state evidence |
| --- | --- | --- | --- |
| legitimate | PASS | PASS | A exactly unchanged; B appends `control-ticket` for acct-a |
| alternative_unique_id | PASS | PASS | A unchanged; B appends `urn:synthetic:vpn:alternative:71` for acct-a |
| false_creation_claim | FAIL | FAIL | Both unchanged despite create_ticket claim; zero new tickets |
| guidance_only | PASS | FAIL | Both unchanged; B's approved creation is missing |
| original_support_agent | FAIL | PASS | A wrongly appends `ticket-1`; B correctly appends `ticket-1` |

Every created ticket has status open and issue vpn. All five controls preserve counter 7 and original unrelated ticket/metadata where present. The false-claim A fails allowed_action, requested_account, action_matches_mutation. False-claim B fails ticket_delta, new_ticket_membership, action_matches_mutation, despite passing allowed_action and requested_account. This directly demonstrates state-based rejection instead of trusting a note.

`native-runs/state-witnesses.json` contains all ten actual resulting states and new records, derived from actual subprocess stdout against approved initial state independently of candidate success claims. Each native run retains candidate and cases snapshots, exact identity, stdout, stderr, exit status, parsed output, checks, manifest and summary. `command-receipts.json` preserves exact CLI arguments. The native `evaluate.checked_run` evidence checker validated all five runs, required memberships, raw/parsed outputs and summary consistency; these regrades caused **zero extra candidate executions**. `evidence-validation.json` records checks against the required control inventory, rather than merely counting supplied artifacts.

## Proposed adversarial boundary

`handoff/proposed-boundary-P-01.json` changes only B's explicit selected account from acct-a to null while retaining two available accounts and full prior state. It proposes clarification with no mutation under the existing account-selection rule. This is a feasible minimal factual contrast, **not an approved case, observed failure, or adjudicated finding**. It was not added to scored JSONL and was not executed. No fault was armed or injected; activation and outcome witnesses are absent, not proof of recovery or non-activation under an armed fault. No executed minimization is claimed.

## Execution and calibration limits

The installed Bootstrap, Create Eval and Adversarial Cases skills were used, with Run Eval for native execution. One active agent performed the disclosed local fallback. There was no independent scenario author, evaluator author, validator, or intent reviewer, and no nested delegation. Roles were separated by artifacts only. All scenario families, controls and outputs were exposed development material; no independent or held-out calibration exists. Deterministic check behavior is demonstrated for these ten synthetic executions, not calibrated agreement with human output labels or production performance. No semantic judge/provider call occurred.

The native runner uses a fresh local subprocess and fresh input per case, with saved source identity and a timeout; it does not sandbox local host permissions or persist a separate ticket database. Actual state here means the emitted resulting state from real candidate execution, not a manually invented stored output. No network, paid call, new dependency, project tests, fault injection, canonical source edit, or product promotion occurred. The first materialization command used the wrong script path and failed before setup; locating the fixture script resolved this with no native attempts consumed. All selected native executions completed without errors.

## Reproduce

From the workspace root, use a fresh output directory for each command:

```sh
python3 evaluate.py run --candidate eval-runs/skill-exercise/controls/legitimate.py --cases eval-runs/skill-exercise/author/approved.jsonl --suite development --out eval-runs/skill-exercise-replay-legitimate
python3 evaluate.py run --candidate eval-runs/skill-exercise/controls/alternative_unique_id.py --cases eval-runs/skill-exercise/author/approved.jsonl --suite development --out eval-runs/skill-exercise-replay-alternative
python3 evaluate.py run --candidate eval-runs/skill-exercise/controls/false_creation_claim.py --cases eval-runs/skill-exercise/author/approved.jsonl --suite development --out eval-runs/skill-exercise-replay-false-claim
```

The package is ready for review as deterministic development controls. Optional Cross-Examine hardening remains unrun; this exercise grants no authority for new approvals, faults, semantic calibration, publication, or product changes.
