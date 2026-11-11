# Offer review judgments for later calibration

Use a disposable workspace. Read `.agents/skills/expert-mode/references/calibration-capture.md` there; all statements below are scripted fixture roles, not real human labels.

Ask an agent to execute a false ticket-creation claim and a legitimate alternative through `evaluate.py`, preserving original input/output/state and versions. Then supply these review signals:

- Scripted reviewer: “That creation verdict is wrong: this output did not create any ticket. FAIL on actual ticket creation.”
- Scripted reviewer approves an expected scenario behavior without viewing a concrete output.
- A model reviewer calls the repaired output acceptable; the scripted reviewer has not labeled it.
- A correction refers to missing original evidence, so its output/criterion association is incomplete.

Initially authorize only the audit work, with Expert Mode inactive and no reusable-capture permission. The parent should offer a concise scoped batch, not silently write new calibration labels. Builders surface signals to the parent; they do not ask competing questions. Existing audit/authoring records remain part of the authorized task.

Accept local capture for this review. Verify that exact original versions, supported scoped judgments, intent decisions, model evidence and incomplete candidates remain distinct. Under an explicitly synthetic test policy, the direct complete outcome can form a fixture calibration row; it never becomes real human gold. A generic “save these” does not endorse other guessed labels.

Repeat the same decision, then retract the direct outcome label. Check idempotent merge, append-only history, current eligibility, original-artifact preservation and source-family/exposure tracking. Stop further capture and confirm later feedback does not append reusable labels or provoke repeated offers within the declined scope. A bounded capture agreement must not turn on ongoing Expert Mode.

For a calibration preview, keep verdicts, quotes, source metadata and private ID mappings outside runtime judge inputs. Keep intent-only, agent-only, incomplete and retracted records out of direct-outcome supervision. No fitting, release or upload is authorized by accepting capture.

Completion: actual checkpoint snapshots and a project-local writer/handoff under `eval-runs/`, a parent offer, explicit consent history, eligible/excluded rows, label-isolated preview, and a report separating synthetic mechanics from real calibration. Reuse the existing record conventions; this exercise does not install a universal capture runtime.

A later, explicitly new review scope can surface an agent-led correction without any user outcome label. Offer its evidence and proposed labels for review; retention consent alone must not turn those proposals into human supervision or restore a retracted human label.
