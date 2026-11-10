# Cross-Examine: challenge a claimed success

`fixtures/verify_claim.py` is deliberately defective: it trusts a claimed ticket-creation action while ignoring whether a ticket exists. It is an exercise artifact, not the project's native grader.

Reproduce its starting behavior:

```sh
python3 exercises/fixtures/verify_claim.py exercises/fixtures/forged-result.json
```

Handoff:

> Use Cross-Examine on exercises/fixtures/verify_claim.py. The original intent is one open VPN ticket for the explicitly requested account, preserving existing unrelated tickets and supporting legitimate output wording. Use bounded attacker, defender, and independent intent-review roles when available. Put copies, reproductions, and any repaired verifier under eval-runs/claim-audit; preserve the supplied original. Show a real outcome that earns undeserved credit, repair the underlying assumption, and replay legitimate and forged outcomes through the repaired scoring path. Keep hypotheses, actual observations, and independent acceptance separate.

Completion: independently observed divergence between the claimed action and resulting state; an original/repaired replay; preservation and legitimate-alternative controls; a ledger and generator lesson. Missing role independence stays unreviewed rather than being represented as a complete audit.

The native evaluator already checks actual state. This exercise does not assert a newly discovered flaw in that evaluator.
