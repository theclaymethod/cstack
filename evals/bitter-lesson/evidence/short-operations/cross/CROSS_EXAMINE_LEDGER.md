# Local action-claim proxy audit

2026-11-10. One operator authored and executed the candidate. Independent attacker and intent reviewer were unavailable. Formal adjudication: **UNREVIEWED**.

The original contract requires real appended state with unrelated tickets preserved, allowing arbitrary unique IDs and legitimate note wording. The frozen proxy checks only `action == create_ticket`. The supplied forged artifact and operator-authored forged program earn proxy credit. On `dev-explicit`, the latter returns the correct account and an unchanged empty ticket list. Native grading rejects it for ticket delta, new membership and action/mutation. This establishes the narrow divergence without assuming a new native-grader flaw.

`legitimate-alternative.py` changes the conforming candidate's ticket ID prefix and note wording. Its actual development executions pass 8/8, including preservation of closed and other-account tickets. The claim proxy accepts its explicit creation too. Native results and raw states are in `state-witness.json` and the two run directories. No canonical verifier was changed; the native grader supplies the demonstrated prevention boundary. No repaired independent audit is claimed.

Proposed generator lesson, not independently confirmed: a success assertion must be paired with complete observable state; test empty false claims, exact state preservation and legitimate alternative identifiers/wording before accepting a verifier. This scoped replay demonstrates native rejection and alternative acceptance, not general immunity or independent discovery.
