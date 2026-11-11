# Independent original-source verdict

## Basis and independence

I wrote `intended-capability.md` before receiving replay material. I then read only the coordinator-supplied `review-packet-original`: its intent statement, raw replay script/observations, frozen archive verifier, original phase-2 capture serializer, final phase driver, capture guidance, candidate source and native trace. I did not read attacker or repairer reports, their verdicts, or proposed repairs. I made no source/packet edits and no provider/network calls.

I independently executed `python3 <archive>/verify_archive.py` for `archive-baseline`, `h1-initial-state-mismatch`, `h2-reviewed-output-mismatch`, and `h3-unsupported-source-quote`. All four exited 0 and returned `verified: true`, `eligible: 0`, `runtime_items: 0`, and `human_gold_rows: 0`. The raw replay preserves native traces and the verifier while changing disposable capture evidence and refreshing its locally supplied hashes.

## Verdict

**Confirmed, narrowly: semantic evidence-provenance verification is incomplete.** The three observations support one common verification weakness with distinct state, output and quote witnesses. They do not establish three independent end-to-end capture failures or an adversarial native candidate exploit.

| Observation | Independently observed divergence | Intent assessment |
| --- | --- | --- |
| H1 initial state | Captured `initial-state.json` contains ticket `never-in-native-input`; preserved native input has `tickets: []`. The verifier accepts it after dependent hashes are refreshed. | This is invalid evidence for the claimed exact original state. Legitimate alternate implementations may represent state differently, but cannot assert an extra ticket existed in the original run. The verifier does not establish that copied state matches its native anchor. |
| H2 reviewed output | Captured `output.json` substitutes the note with text never emitted by the native candidate; the preserved trace still contains `Opened a VPN support ticket.`. Historical phase-2/3 runtime previews are changed to agree with the substituted copy, and verification passes. | Exact reviewed-output identity is a substantive requirement even when the substituted output happens to warrant the same FAIL criterion. Matching derivative copies and hashes does not establish identity with the native output. This is an undeserved archive-verification pass, not a demonstrated wrong current calibration outcome. |
| H3 original quote | The captured row labeled `verbatim-scripted-quote` contains an invented sentence absent from the unchanged source snapshot. The verifier accepts it after hashes are refreshed. | This contradicts the record's declared verbatim provenance. A paraphrase or proposed interpretation would be a legitimate alternative if accurately declared and supported; inventing the reviewer's words is not. The observation does not show promotion of a human or synthetic authority. |

## Scope and non-findings

The mutation script acts as an operator with write access to disposable artifact files, review-store snapshots, preview derivatives and checkpoint/hash annotations. That is broader than the native ticket candidate's demonstrated stdin/stdout behavior. The native candidate in this packet reads a request/state JSON and prints a JSON response; it does not perform the corruptions. Host permissions are explicitly not a containment boundary. Classify these probes as operator-artifact-corruption resilience checks and checker defects, not as evidence that a candidate crossed a protected boundary.

The phase-2 serializer and final phase driver are historical fixture adapters, not a promised general-purpose capture runtime. Their hardcoded handling of these scripted phases, or failure to accept hypothetical unrelated scenarios, is not independently an intent violation. The shown baseline capture and store remain valid on these probes; the variants were deliberately corrupted after capture.

The final original FAIL has been retracted and all final candidates are excluded/incomplete. The accepted corrupted archives therefore do not demonstrate a wrongly eligible current row, human-gold leakage, fitting, ongoing Expert Mode activation, ignored stop consent, or duplicate append. The output note change also leaves the ticket-creation failure intact. Those limits materially narrow the finding.

Refreshing self-supplied hashes demonstrates that checksum consistency alone does not prove semantic lineage to separately retained native/source evidence. It does not demonstrate that the archive checker promised authenticated resistance to a writer who may rewrite every authority anchor. Here the raw native/source anchors remained unchanged and were available for comparison, so failing to detect their disagreement is a useful bounded gap in a checker used to support an exact-evidence claim.

## Required meaning of repair validation

Independent acceptance of any repair must retain the valid baseline, detect the three demonstrated disagreements with the preserved native/source anchors, and preserve legitimate declared representations or paraphrases rather than requiring universal byte equality. Repair validation should not be described as protection against a malicious writer who can replace all anchors. Current consent, authority, append-only history and final exclusion results remain requirements rather than demonstrated failures from this packet.
