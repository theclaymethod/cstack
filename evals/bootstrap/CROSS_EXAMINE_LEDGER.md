# Bootstrap Cross-Examine ledger

## 2026-11-10 — bounded development audit

The user authorized Cross-Examine and fixes for confirmed issues. Original intent: interview for behavior, generate feasible scenarios with subagents, let the user approve/correct/defer guessed expectations, then have evaluator authors use the target project's format. Evidence gathering remains project specific. Expected behavior, actual outcome labels, and product performance are separate claims. Supported alternatives must survive authoring and validation.

The existing fixture checks four approved routing cases using stored action/count observations. It explicitly lacks an assistant implementation, ticket-state execution, response/account/referral semantics, semantic judge calibration, and independent held-out evidence. Those missing capabilities were not treated as defects by themselves.

### Roles, access, and budget

The coordinator acted as defender. Two fresh attackers separately investigated package validation and resumed review decisions. A fresh non-forked intent reviewer first established the contract, assessed raw original observations without competitor conclusions, then reviewed one frozen repair and independently replayed controls. The reviewer did not author, repair, coordinate, or attack the artifact.

The package attacker had an isolated source copy and could change authored case rows. Replay, original runner/suite, user decisions, handoff, case mapping, and preservation receipts were outside its permitted edits and verified unchanged. Operator receipts were kept separately. All processes nevertheless shared host filesystem permissions: these were instructed work scopes, not OS-enforced containment or hidden-label isolation. No such security claim is made.

Budget: one search round, up to three package mutations and three workflow probes. The package attacker exercised three mutations; the workflow attacker prepared one resume probe and the coordinator dispatched a fresh candidate. Other workflow ideas remained unexecuted hypotheses. Runtime was local Python with standard-library JSON/files; no database, Docker, network, paid campaign, or external mutation was needed.

Original source hashes are in [the frozen manifest](evidence/cross-examine/original-hashes.json). Three reviewed repair-source hashes are in [the repair manifest](evidence/cross-examine/repaired-hashes.json). Earlier results remain unchanged. Everything below is synthetic development evidence.

## Confirmed: an authored input can change the approved decision boundary

**Original requirement:** S-03 authorizes one ticket because the employee explicitly requests one for an unambiguous account with no existing ticket. A generic connection-failure question without authorization instead calls for guidance and zero tickets.

**Allowed reproducer:** change only S-03's authored `input` to the generic help request, including `explicit_ticket_request: false`, while retaining its ID, family, and `create_ticket/1` expectation. The [candidate](evidence/cross-examine/attempt-1-input-substitution.cases.jsonl) leaves all protected files unchanged.

**Original observation:** actual replay exited 0 and reported 5 PASS, 43 FAIL, 8 ERROR, zero control mismatches. It rewarded the retained ticket-creation expectation despite the changed scenario. The coordinator independently reproduced the same result from a clean copy. This is approval-to-case fidelity failure, not an unsupported claim about referral text or real product state.

**Repair:** the frozen replay checks each authored input/family against an eval-owned registry of reviewed representations before scoring. JSON formatting and object-key order may vary. A different semantic input requires source review and a new fixture revision. Bootstrap itself now instructs authors/integrators to validate schema and compare actual inputs, context, initial state, families, and checks with the approved scenario; matching IDs/labels is insufficient. Approved source records remain outside author changes.

**Observed repaired result:** the same candidate exits 1 with `Authored input/family differs from the approved scenario: S-03`. The unchanged baseline, both S-04 output alternatives, and its registered structured representation still succeed. This prevents the demonstrated substitution against this frozen input registry; it is not a universal semantic-equivalence verifier.

## Confirmed: required case fields can disappear without validation failure

**Original requirement:** the fixture's existing project format requires `id`, `input`, `family`, and `expected` per row. Recoverable inputs and construction families are also part of Bootstrap's handoff contract.

**Allowed reproducer:** remove only `input` and `family` from S-02, S-03, and S-04 in the [candidate package](evidence/cross-examine/attempt-2-required-fields-omitted.cases.jsonl). Preserve original decisions, runner, and receipts.

**Original observation:** actual replay again exited 0 with the same 56 expected action/count verdicts. It read only identities and expectations, accepting malformed project records. The coordinator independently reproduced this acceptance.

**Repair:** validate required fields and identity/expectation types before invoking controls, then check scenario input/family fidelity. Schema/setup errors remain errors; they are not product FAIL labels. The general generator lesson is to validate the target project's full required record shape before interpreting favorable grading results.

**Observed repaired result:** the same candidate exits 1 with `Case is missing required project fields: id, input, family, expected`. The baseline and registered alternative representation remain valid.

Both gaps share the faulty premise that matching IDs and expected verdicts establishes a faithful authored eval. The generator lesson is encoded in Bootstrap's integration step, rather than relying only on this incident record.

## Legitimate controls and bounded clean observations

- Removing S-04's approved `clarify` alternative was already rejected by the original replay and remains rejected. No repair was claimed for that control.
- The repaired baseline retains 5 legitimate PASS, 43 intended FAIL, and 8 deliberate ERROR verdicts across the original 14 invocations, with zero mismatches. These are controls, not measured product outcomes.
- A structured S-04 request/context/state representation and reversed allowed-action order also pass all original controls. The fixed registry does not restrict S-04 to one response action.
- A fresh Bootstrap candidate resumed a checkpoint whose latest exact correction approved `guidance` or `clarify` but whose handoff/case still held revision 1. It materialized revision 2, preserved original records and archived artifacts, and kept S-05 unresolved. An independent observer then ran the actual runner: guidance/0 PASS, clarify/0 PASS, duplicate ticket/1 FAIL. This is one clean resume observation, not comprehensive workflow coverage. [Request and observations](evidence/cross-examine/resume-probe/).

## Replay and independent acceptance

From the repository root:

```sh
python3 evals/bootstrap/cross_examine.py
```

The script uses disposable copies, the frozen original replay, the current repaired replay, the three recorded candidates, and legitimate controls. It saves actual commands, code/candidate hashes, stdout/stderr, and expected-versus-observed exits. Specific error checks distinguish the intended prevention from an unrelated crash. Nine artifact-level observations reproduced successfully; this command does not rerun the agent workflow.

[Before/after observations](evidence/cross-examine/before-after.json), [original independent intent assessment](evidence/cross-examine/original-intent-review.md), [frozen-repair assessment](evidence/cross-examine/frozen-repair-intent-review.md), and [independent reviewer controls](evidence/cross-examine/reviewer-controls.json) preserve the checkpoints. The reviewer accepted both defects and the frozen repair within the stated fixture scope. No verdict was used to iteratively tune the repair.

Remaining limits: arbitrary equivalent paraphrases need review before adding registry entries; the registry and source authority are assumed outside candidate edits, not protected by host permissions. Broader live-conflict, low-trust approval-source, and criterion-scope probes were not executed. No new product execution, semantic calibration, independent holdout, production prevalence, or general immunity claim is established. Confirmed prevention is limited to the reproduced mechanisms and tested valid alternatives.
