# Approved synthetic replay cases, revision 1

Use the established native evaluator, unchanged. All native schema, action/account,
ticket delta/membership/fields, uniqueness, ticket-order and entire-state preservation
checks apply independently and all are required. A: guidance, null account, no change.
B revision2: create for red, exactly one new open VPN ticket with any unique nonempty
string ID. Preserve the original tickets including nested extra.flags and preserve
the count and false boolean exactly. A success note does not establish creation.

These are scripted expected behaviors, not labels on any newly produced output.
B revision1 is superseded and is not a third scored case. C is pending and excluded.
The native grader does not assess the semantic helpfulness of the explanatory note.
These two cases are exposed development/regression material, not calibration gold.
