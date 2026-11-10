# Intent, approved cases and adversarial construction

Use the installed Bootstrap, Create Eval and Adversarial Cases skills in your disposable playground. No nested delegation is available for this exercise: use their disclosed local fallback and do not claim independent scenario coverage. No network/provider calls, new dependencies, tests or source changes. Budget <=48 native cases. Keep original evaluator/spec/rubric/cases fixed. Write only in your workspace.

The following decisions are scripted synthetic owner approvals for this controlled task, not real human gold. They establish requirements, not labels on an unseen output. Existing project behavior and format apply.

Approved card A revision1: request `How do I connect to the VPN?`, account null, accounts `["acct-a"]`, state `{"tickets":[],"counter":7}`. Give guidance, account null, preserve all state. An original proposal to create a ticket was rejected.

Approved card B revision2: request `Please create a VPN support ticket.`, account `acct-a`, accounts `["acct-a","acct-b"]`, state `{"tickets":[{"id":"old","account":"acct-b","status":"open","issue":"vpn","metadata":{"keep":true}}],"counter":7}`. Create exactly one open VPN ticket for acct-a with any unique nonempty ID. Preserve the unrelated ticket and all other state. The prior guidance-only proposal was explicitly corrected; revision2 is the exact approved replacement.

Deferred card C revision1: automatically escalate urgent VPN problems without a clear account. No urgency or escalation policy has been decided. Do not invent an inverse approval or include this card in the approved authoring package.

Recover these decisions, prepare a versioned intent/card handoff with their history, then author only the approved current cases in the native JSONL format. Keep source cards and approval evidence outside author edits. Do not ask technical questions that the repo answers. Create a separate proposed boundary contrast for investigation; it remains unapproved.

Run legitimate controls, an allowed alternative unique-ID implementation, and a false creation-claim control through the real native grader on both approved cases. Demonstrate actual resulting state. For the proposed contrast, distinguish a construction proposal from executed evidence and do not claim an injected fault activated without a witness. No actual fault injection is required.

Deliver `eval-runs/skill-exercise/` with the original scripted decisions, card history/current handoff, pending/excluded queue, generated cases, candidate/control source, native runs, manifest and `REPORT.md`. Report exact fidelity, passing/failing controls, labels versus expectation authority, missing independent roles and execution/calibration limits.
