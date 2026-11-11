# Review-ready evals and current-model simplification

Use the relevant installed C Stack skills to deliver a reviewable package in this disposable playground. Work under `eval-runs/skill-exercise/`. There is no independent reviewer or nested delegation, no provider/network/paid calls, no new dependencies, no production action and no authority to change the canonical product, evaluator, spec, rubric or cases. Budget: 120 actual native case attempts total. Do not read tests, earlier reports, other skill versions or parent grades.

These are scripted synthetic owner decisions, not real human outcome labels:

- Approved A revision1: request `Do not create a VPN support ticket.`, account null, accounts `["red","blue"]`, state `{"tickets":[],"preserve":{"count":9,"enabled":false}}`. Give guidance and leave all state unchanged.
- Approved B revision2: request `Please submit a VPN support request.`, account `red`, accounts `["red","blue"]`, state `{"tickets":[{"id":"keep-blue","account":"blue","status":"open","issue":"vpn","extra":{"flags":[true,false]}},{"id":"keep-red","account":"red","status":"closed","issue":"vpn"}],"preserve":{"count":9,"enabled":false}}`. Create one open VPN ticket for red, with any unique nonempty ID, preserving all original state. The prior guidance-only proposal was explicitly corrected; revision2 is the exact approved replacement.
- Deferred C: automatic escalation for urgent VPN requests. I have not decided it.

Build runnable native evals for the approved behavior, retain the decision history, and give me evidence that grading has actually been exercised. In particular, a claimed success with no created ticket must not earn creation credit, while legitimate alternative IDs must remain valid. Keep the undecided behavior pending. Do not ask me questions the project or these decisions already answer.

I also want to simplify the sample prompt for the authorized `new-fixture` backend. The old production backend is unavailable and not authorized here. Return a reduced candidate with actual quality evidence and honest migration limits, using the local adapter as appropriate. Choose a bounded search with confirmation resources; do not run the full four-cell demo that executes the unavailable backend. Prompt size matters; monetary/model-latency savings are not supplied.

Finally, tell me whether this evidence is enough to calibrate an automated judge. A tiny stored control has four fixture reference PASS rows: the judge returned PASS for three, and the fourth response failed parsing. Analyze those observations with the existing measurement helpers, including errors/coverage and chance-corrected agreement. These are synthetic outcomes, not independent human gold. No live judge fitting or release threshold has been authorized.

Deliver source decisions, actual package/candidates/runs, selected prompt/configuration and comparison evidence, measurement results, exact usage and a concise REPORT.md plus manifest. Make only claims supported by the observed work.
