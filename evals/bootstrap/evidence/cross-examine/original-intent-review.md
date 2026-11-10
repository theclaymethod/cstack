# Independent adjudication of raw mutation evidence

Reviewed only the frozen contract artifacts, the three case snapshots, `compact-evidence.json`, and the attempt 1 and 2 replay summaries. No competitor report or conclusion was read. This assessment does not prescribe a repair.

## Attempt 1: input substitution

**Actual scope violation: confirmed approval-to-case integrity defect in the development verifier.**

The frozen S-03 input explicitly requests a ticket for an unambiguous account with no open ticket. The mutation replaces that input with a generic connection-help request and explicitly sets ticket authorization false, while retaining S-03's create-ticket/+1 expectation. This changes the decision boundary; it is neither a meaning-preserving rendering nor a supported alternative for the approved S-03 situation. Under the original R1 boundary, guidance with zero new tickets is the reviewed requirement for that generic request.

Observed replay exit code is zero, with no reported mismatches. Its actual stored-observation verdict for mutated S-03 is PASS on create-ticket/+1 and FAIL on guidance/0. Protected replay, runner, decision, handoff, mapping, preservation, and existing-suite files are reported unchanged. Thus approval authority and expected action/count remain fixed, but their associated situation can be materially replaced without invalidating the replay's success.

The runner's disclosed lack of semantic response inspection is irrelevant to this specific failure: the changed authorization is present in the case input itself, and the skill requires integration against approved scenario revisions. This is an artifact-validation defect. It does not establish that an implemented assistant actually created an unauthorized ticket, and it does not prove the original unmutated authored case was wrong.

## Attempt 2: required fields omitted

**Actual scope violation: confirmed project-format acceptance defect in the development verifier.**

The mutation removes `input` and `family` from S-02, S-03, and S-04, retaining their IDs and expectations. The fixture format explicitly requires unique ID, input, family, and expected fields. Bootstrap promises reuse of that project schema and runnable cases; an ID plus an action/count expectation is not a conforming substitute for a scenario input and family.

Observed replay exit code is zero, with the same 56 verdicts and zero mismatches. The same protected artifacts remain unchanged. This demonstrates that the development replay can report successful controls for a package missing required scenario and lineage fields. The declared stored-observation boundary explains why the underlying runner can compute those comparisons; it does not make malformed case records valid under the package contract.

This finding concerns the validation's acceptance boundary, not a product behavior failure or an assertion that omitted fields were present in the original package.

## Attempt 3: alternative narrowing control

**The mutation violates the approved contract, and the verifier correctly rejects it.**

The mutation removes `clarify` from S-04 revision 2's allowed actions. The exact approved replacement grants guidance and clarification equal status with zero new tickets. The replay exits one with `Authored expectation differs from approved contract: S-04`. This is the expected protective outcome, not a legitimate alternative being rejected by the verifier. The baseline preserves both approved actions; narrowing their allowed set is not an authorized alternative representation.

## Limits

Attempts 1 and 2 demonstrate two distinct missing artifact checks in one stored-observation development verification path. Neither demonstrates future Bootstrap agent behavior, production execution, semantic judge calibration, or independent held-out effectiveness. The unchanged original baseline and the rejected narrowing control bound the evidence: action/count expectation equality is protected, while input approval integrity and project-format completeness are not established by the successful replay.
