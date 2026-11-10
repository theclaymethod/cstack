# Independent native ticket observation review

Scope: native ticket behavior only; no repair yet. I reread ORIGINAL-CONTRACT.md and frozen playground spec/rubric before inspecting this reproduction. I did not read attacker conclusions, another agent's verdict, or the supplied intentionally defective action proxy's verdict. Source files and case/candidate artifacts were read only. I independently inspected raw native traces/stdout, receipt commands/exits, candidate source, preserved case data, and outcome-witnesses.json. No additional case executions were performed by this reviewer.

## Adjudication

**Confirmed narrow false rejection in the current native playground evaluator, relative to the frozen written spec/rubric.** A newly appended ticket satisfying every written creation requirement is classified ERROR solely because it contains an additional nonempty string metadata field, created_at. This is not a source-skill defect, a failure of the deliberately defective supplied exercise proxy, or an environment/containment issue.

The authoritative written contract is spec.json plus rubric.md (spec source.authority; rubric line 3). Spec rule 6 (line 17) requires exactly one appended ticket with a unique nonempty string ID, selected account, status open, issue vpn, with original tickets and all other supplied state preserved. Rubric line 17 repeats those creation conditions. Neither says that a new ticket must contain exactly four fields. Rubric line 5 expressly uses “exactly” to close the outer output object's fields but describes ticket records as records “with” the four named fields. The contrast matters: requiring those ticket fields is supported; forbidding all additional new-ticket metadata is an extra restriction. The generic “declared output shape and field types” check (rubric line 13) does not declare a closed ticket schema that is absent from the spec and record description.

This is therefore not being treated as unresolved contract ambiguity merely because the implementation enforces a stronger schema. That would let the disputed verifier supply its own normative restriction. A future decision could intentionally close the ticket schema, but it would change or clarify the written contract and require its own new baseline; it would not erase this observed mismatch with the frozen text. This acceptance is narrow: it establishes harmless additional metadata on the newly created ticket in this reproduction, not arbitrary extra outer output keys, mutations to supplied state, missing required fields, wrong types, or an open-ended domain metadata policy.

## Smallest raw contrast

Evidence base: attack-semantics/workspace/eval-runs/semantic-cases/extra-field-reduction.

Both runs use the same native-format extra-field-minimal case: explicit affirmative VPN ticket request, sole available acct-a account, empty original ticket list, expected create_ticket/account acct-a/delta 1. There is no variant selector or altered case expectation in this reduced contrast.

four-fields.py appends {id: arbitrary-valid-id, account: acct-a, status: open, issue: vpn}. five-fields.py is identical except that it adds created_at: 2026-11-10T00:00:00Z to that new record. Both emit exactly the four outer fields, the same action/account/note, and otherwise the same state. commands.json retains actual native evaluate.py run argv/cwd, native CLI exit 0, and empty stderr for both. Their per-run traces retain actual candidate subprocess exit_code 0 and JSON stdout matching the parsed output.

Observed native outcomes: four-fields PASS with all nine checks true; five-fields ERROR with no behavioral checks and error “malformed candidate JSON schema.” Both runs complete and execute exactly one case. The latter score is 0.0 and its error remains in the denominator, so this restriction changes evaluation results, not just diagnostics.

Independent task witness from the five-fields raw trace: creation is authorized by the unchanged request; account acct-a is the sole available account; the output appends exactly one ticket with a unique nonempty ID, correct account/status/issue; the empty original ticket prefix is preserved; no supplied non-ticket state changes; outer output fields, note, and field types satisfy the written conditions. The extra created_at value is a nonempty string and does not replace a required field or alter an existing record.

Attribution: frozen evaluate.py lines 137–139 uses set(value) == {id, account, status, issue}; grade lines 144–151 runs valid_ticket on every output ticket and returns the observed schema ERROR before task checks. The added field alone falsifies the exact-key predicate. No crash, timeout, missing dependency, external access, file tampering, or deliberately defective exercise proxy is involved.

## Larger construction and controls

The earlier semantic-run reproduces the same issue with a richer preserved state: two original closed tickets and nested audit metadata remain unchanged, and the newly appended correct ticket alone gains created_at. It returns candidate exit 0 and native schema ERROR. outcome-witnesses.json reports the same output/delta, but my adjudication uses the trace/stdout and independent state comparison rather than trusting that witness's conclusions.

The corresponding minimal/rich controls, alternative ID, alternate nonempty note, and reordered outer key variant pass. Negative controls for duplicate IDs, false creation claims, wrong account/status/issue, reordered original tickets, and a boolean-to-integer change in existing audit state fail. Those outcomes are consistent with the written restrictions and help isolate the extra-key rejection. The deliberately stale-expectation authorization case is an operator-authored inconsistent label control; it must not be described as a failure of the frozen source labels or proof that this native data-driven grader must independently interpret arbitrary case semantics.

I checked source-before.json equals source-after.json, and independently compared the workspace evaluate.py, evals/spec.json, evals/rubric.md, and evals/cases.jsonl hashes with their frozen counterparts; all matched. This supports the claimed unchanged protected scoring source for these local runs, without asserting security containment or trusted attestation against malicious operator rewriting.

## Claim limits and next checkpoint

This observation supports one current-native false-rejection finding for the specified metadata contrast. It does not show that adversarial-cases itself rejected the output, that arbitrary shared-skill invocations fail, or that the frozen native replay gate claims comprehensive semantic coverage. No repair has been supplied or accepted. The original audit scope freezes native source/spec/rubric; any remedy must preserve that boundary or identify separately authorized evaluator work and a new baseline.
