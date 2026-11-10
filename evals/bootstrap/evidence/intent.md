# VPN support intent — revision 1 (provisional)

Source: fixture user request, turn 1: “Bootstrap evals for our IT assistant. I want it to handle VPN support without creating unnecessary tickets.”

Trigger: an employee asks the IT assistant for VPN support.
Success: the assistant handles the request while avoiding unnecessary ticket creation. The conditions requiring a ticket remain a product decision.
Failures: unnecessary tickets; the definition of necessary escalation is unresolved.
Alternatives: guidance, clarification, or ticket creation, subject to reviewed scenarios.
Preserved behavior: existing-howto remains unchanged: asking for the VPN setup guide permits guidance and requires ticket_delta 0.

## Evidence and implementation

The project README says the assistant is not implemented and has no production traces. Use synthetic scenario proposals grounded in the user's requirements. Product execution is unavailable. No external calls are authorized or needed.

Existing format: JSONL in evals/, each row with unique id, input, family, and expected.allowed_actions plus expected.ticket_delta. Action vocabulary: guidance, create_ticket, clarify.
Existing runner: python3 runner.py --cases evals/cases.jsonl --observations observations.jsonl
Runner boundary: stored action and ticket-count observations only. It cannot establish guidance quality, successful VPN recovery, ticket contents, or other resulting-state preservation. Preserve runner.py and evals/existing.jsonl.

## Pending product decisions

1. For an ordinary VPN connection failure, what should happen before a ticket is necessary?
2. When a request is ambiguous, should the assistant clarify first? Which urgent or security-related situations require escalation?
3. Does an explicit employee request to open a ticket override normal troubleshooting? What if a ticket already exists?

## Proposed first scope

After intent clarification, propose a small first batch (about six cards) covering guidance, the ticket boundary, clarification, and one adjacent regression. The user may change review volume or priorities. Expectation approvals will remain distinct from labels on actual outputs. No expectation cards have been approved.

## Work status

Inspected the project and sibling Bootstrap references. Intent interview is pending. No eval authoring or product execution has occurred. Existing suite and runner are untouched.

# Intent revision 2 — confirmed boundaries

Source: fixture user reply, turn 2 (verbatim): “For how-to questions or a generic 'VPN won't connect,' give troubleshooting guidance; that alone isn't permission to file a ticket. An explicit request to open a ticket is enough unless they already have an open VPN ticket: then guide them to that ticket and don't create a duplicate. If they ask you to act but it's unclear which account they mean, clarify first. Focus on those routing boundaries and preserving the existing how-to case; six cards is good. No extra urgency/security rules for this batch. No cross-examine for this run.”

R1: How-to and generic connection failures require guidance with ticket_delta 0.
R2: An explicit request for a ticket, with an unambiguous account and no existing open VPN ticket, requires create_ticket with ticket_delta 1.
R3: An existing open VPN ticket overrides the explicit new-ticket request: guide the employee to it and do not duplicate; ticket_delta 0.
R4: A request for action with an unclear target account requires clarification before action; ticket_delta 0.
R5: Preserve the existing setup-guide case.

Supported alternatives: wording and troubleshooting contents may vary; this runner checks only action category and ticket count. Detailed response semantics are outside the runner's observable evidence.
Excluded: urgency/security escalation rules, production execution, paid runs, cross-examination.
Scope: six proposed review cards, awaiting exact expectation approvals.

Revision 1 questions have been resolved for this batch. Current approved-card count: 0. Next step: independent scenario proposals, merge, and user review.

## Scenario proposal checkpoint

Two independent scenario authors produced three proposals each. Initial parallel dispatch hit capacity; a second independent author ran once a slot freed, without reading the first author or coordinator drafts. Original scratch outputs are preserved. The unused local boundary draft remains in scratch as lineage, excluded from the six-card batch.

Merged six proposed cards as S-01 through S-06, all revision 1 and pending. Grouped related explicit-ticket variants and account contrast pairs conservatively by construction family. There are no unsupported external factual claims: account/ticket states are explicitly synthetic. Runner feasibility is limited to stored observations; product execution is unavailable. No gold output labels exist.

Review-card semantics include directing to the existing ticket and targeting the correct account; those details exceed the current runner. The handoff must preserve that verification gap rather than claim semantic coverage.

# Intent revision 3 — reviewed subset

User turn 3: Approve S-01, S-02, and S-03 revision 1. For S-04, correction: either guidance to the existing ticket or asking a clarifying question about following up on that existing ticket is acceptable; create no new ticket in either case. That is my approved replacement expectation. Disapprove the S-05 proposal, but I haven't decided its replacement yet. Defer S-06. Build and validate the approved subset now using our existing format and runner. Keep the existing suite unchanged. No product implementation, semantic judge calibration, or cross-examine for this run.

R3 amended for S-04: either guidance to the existing ticket or a clarifying question about following up on it is acceptable; no new ticket. Record S-04 revision 2 as approved by the explicit correction, without asking the user to approve their own exact words again. S-04 revision 1 is superseded.

Approved: S-01 r1, S-02 r1, S-03 r1, S-04 r2. Pending: S-05 r1 disapproved with replacement undecided; S-06 r1 deferred. S-05 disapproval does not approve the inverse or settle a revised account-ambiguity requirement. Current batch has 4 approved, 2 pending. No actual output labels exist.

Frozen authoring handoff: approved-handoff.json. Independent author ownership scopes have been separated. All validation is synthetic development controls through the existing deterministic runner; product execution and semantic calibration are excluded.

## Completion checkpoint

Authored and integrated 4 approved cases into evals/bootstrap-vpn.jsonl using two evaluator authors. The original existing-howto JSONL row is preserved byte for byte in the standalone approved package; evals/existing.jsonl itself is untouched. S-04 r2 allows both guidance and clarify with ticket_delta 0.

Ran validate_controls.py r1: 14 existing-runner invocations, 56 case/control verdicts. Actual results: 5 PASS on legitimate pairs, 43 FAIL on invalid pairs, 8 ERROR for deliberately missing/noninteger observations. All 56 matched the contract-derived expectations. Both permitted S-04 alternatives were accepted. Frozen runner/case/observation/stdout hashes and run details are in validation-r1/. Preservation hashes confirm runner.py and evals/existing.jsonl unchanged.

No product ran, and no semantic calibration, independent holdout, or cross-examination occurred. Guidance/referral/clarification quality, ticket account assignment, actual resulting ticket state, and reset remain execution/observability gaps. These results validate the deterministic stored-observation grading path only.

Partial batch completion: 4 approved authored/validated; 2 pending excluded: S-05 rejected with no approved replacement, S-06 deferred. No new product decision is inferred from either. report.json contains paths, run commands, counts, and limitations.
