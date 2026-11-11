# Authority/identity attacker report

No confirmed defect in current shared capture guidance or exercise13. No independent adjudication was performed. Five attack hypotheses and two native case executions were used, against limits of six and twelve. No network, provider calls, or nested agents. Frozen sources were read only; all modified state is disposable attacker scratch.

The actual candidate boundary for native cases was ordinary trusted local Python subprocess access, without containment. The two programs changed only their returned output. The capture-driver probes below are operator-authored scenario construction against copied historical artifacts, not actions demonstrated inside those native candidates' runtime permissions. The current guidance explicitly says there is no universal capture runtime; the completed archived forward driver is a one-time phase script, not a supported general API.

## Native controls

`evidence/native/false-claim-v1/traces.jsonl`: FAIL, zero created tickets. `evidence/native/legitimate-v2/traces.jsonl`: PASS, one new ticket with an alternative unique ID. `evidence/native-observation.json` records the retained independent state inspection by this same attacker. There is no native-grader failure here. All records remain synthetic; no human-gold authority is established.

## Hypotheses and observed scope

1. H1, whole-transcript digest as identity: the historical `evals/bitter-lesson/evidence/full-capture/driver.py` duplicates existing judgments/rubrics after harmless append-only source growth on its capture → stop → merge1 path. Unchanged-source control yields 6 reviews / 6 rubric rows without duplicate record IDs; appending an unrelated eighth source line yields 8 reviews / 9 rubric rows, repeating two review IDs and three rubric IDs. Both merges exit 0. This is a reproducible historical serializer limitation, not a confirmed defect of current capture guidance or the latest forward flow. Current records guidance already requires stable statement/artifact/assertion matching. Preserve this as historical evidence only.
2. H2, stopped scope: completed final helper rejects the historical stopped scope, writes nothing, repeats no offer. Failed attack.
3. H3, unrelated proposed row under valid helper scope: final helper accepts one cross-scope record because it checks the helper argument's scope, not each proposed row. This requires calling an internal helper with operator-constructed input outside the one-time script's actual constructed phases. Extra-contract robustness probe only; no current consent bypass demonstrated.
4. H4, duplicate helper call: second call asserts on duplicate record ID. The first call writes once. Extra-contract reuse of a one-time script, not a supported-flow false rejection.
5. H5, stale phase2 replay after completed history: replay appends zero records and preserves the stopped/retracted archive. Failed attack; no stale-consent append demonstrated.

## Evidence and replay

Candidate-authored `reproduce.py` preserves native traces, raw source/driver copies, source hashes, per-scenario commands/stdout/stderr, before/after rows and tracebacks. `evidence/summary.json` is the compact machine-readable result. `evidence/source-append/{before,after}.json` and `evidence/unchanged-control/{before,after}.json` are direct comparison witnesses. `evidence/H2-stopped-final-scope`, `H3-cross-scope-row`, `H4-repeat-helper`, and `H5-stale-phase2-retry` each preserve full before/after JSONL and raw result.

Fresh replay (consumes two further native cases, so coordinate with the parent's remaining budget):

```sh
python3 /Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/capture-cross-examine/attack-authority/reproduce.py /Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/capture-cross-examine/attack-authority/replay-01
```

The replay creates a new frozen-source playground if necessary and refuses accidental artifact overwrite through existing-directory checks. Original evidence stays intact. No repairs or teaching changes were made because no current guidance defect was established. These bounded checks do not establish immunity to other authority/identity failures.
