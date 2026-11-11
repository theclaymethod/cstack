2026-11-10 — action claim versus actual state

Intent: an explicit account-specific VPN-ticket request appends one unique open VPN ticket and preserves existing records. Alternative wording and unique ID conventions are legitimate. Original intent is defined by the unchanged spec/rubric and exercise 06, not by verify_claim.py's action-only predicate.

Original verifier: copied as verify_claim.original.py with source retained in the workspace. Candidate access: ordinary stdin request/state and stdout JSON from a trusted local subprocess; no containment or protected-host claim. Attacker, defender and independent intent-review roles: unavailable. One active agent performs sequential controls. Bounded allocation: 24 native candidate cases and two stored-output repair replays; all completed.

Observation: supplied-forged-result.json contains an empty ticket list and the original proxy returns passed=true. Executed forged.py similarly preserves all supplied state, emits create_ticket and chooses the target account. Native-forgery/traces.jsonl shows dev-explicit failing ticket count, new membership and mutation consistency while its allowed action and requested account pass. Native results are 0 PASS / 8 FAIL / 0 ERROR. This isolates the actual-state gap from a mismatched account claim.

Local prevention: verify_claim.repaired.py delegates schema and complete state semantics to the frozen native grade function with the original case. replays.json records the forged-output rejection and legitimate-alternative acceptance. The original proxy also accepted the executed legitimate alternative output (commands/17-original-proxy-legitimate.stdout). alternative.py uses alternative-N IDs and different note text; native-alternative passes 8/8 including closed/unrelated preservation. native-malformed records eight schema errors for forbidden extra fields. Canonical fixture verifier and native evaluator were not edited.

Validation scope: the replayed forgery loses credit and the replayed legitimate output passes. No independent reviewer or attacker validated intent, role separation or broader attack coverage. Formal finding adjudication and repair acceptance remain UNREVIEWED. These receipts support only the observed state-versus-action divergence and local replay behavior.

Teaching artifact: GENERATOR_GUIDANCE.md records the root assumption and generated controls under this authorized evidence directory. Installed/canonical skills were not modified; wider lesson adoption is unperformed. No causal generator-improvement or immunity claim is made.
