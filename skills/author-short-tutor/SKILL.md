---
name: author-short-tutor
description: Design a one-hour agent-led course around a decision the learner can make independently. Use when authoring or revising a short tutor.
---

# Author a short tutor

Lead user-facing replies with the result or decision needed. For several points, put each in its own short, plain-language bullet. A single answer can be one sentence. Link detailed evidence. Preserve open questions, approval gates and any requested artifact format.

Start with the finish. Given which artifact, what should the learner be able to decide or do unaided? Inspect the existing course and try a representative exercise. Bring the owner a plausible example and a nearby case that changes the answer.

## Agree on the lesson

Use grilling when available. Establish who enters, what they already know, the independent exit, and what can be supplied or cut. Research the teaching approach. Name the sources, what each contributes, and any disagreement that changes the lesson. Ask the owner which approach to adopt and wait for the choices that affect scope.

For the owner interview:

- State the current topic briefly. Use short bullets, active voice, and one idea per sentence.
- Group related independent decisions into a small round, usually two or three numbered questions. Respect an explicit question budget. Wait for prerequisite answers before asking dependent questions.
- Give each decision two or three choices. Recommend one with a concrete consequence. Accept a custom answer and replies using question numbers and option letters.
- Propose examples and teaching choices from the available context. Ask the owner to resolve uncertainty that changes the course's scope, gates, or accepted answers.
- After each major topic, read back confirmed decisions, assumptions, and open questions in short bullets. Ask for confirmation or correction. Apply corrections and carry unanswered questions forward without reopening settled decisions.

Show a short brief with the entry, exit, exercises, gates, accepted assumptions and deferred topics. Carry earlier decisions forward. Begin construction when the owner confirms the brief.

## Check the path

Use the statechart skill to model the agreed exercises. Track who supplies the decision, what advances the lesson, wrong answers, hints, worked answers, fresh attempts, pause/resume and time running out. Run TLC on the bounded model. Check that independent completion and partial exit are reachable, that assistance requires a fresh attempt, and that resume restores the pending question. Correct counterexamples. If TLC is unavailable, identify the unchecked claims. Show the owner the chart, gate meanings and any decision the check reopened.

## Write the exchanges

Open with an artifact and the evidence needed to interpret it. Work one example aloud. Give the learner a parallel case with one meaningful decision, ask one question and wait. Supply navigation, data and commands unless doing that work is the lesson. Write the tutor's answer key with the deciding evidence and valid alternatives.

For a delivery promised *at or before* 16:30, an arrival at 16:30 tests the boundary. If the learner calls it late, point back to the promise. If they ask for the answer, explain it and use different times for the independent check.

End on a fresh example and save the learner's own decision. On pause, preserve their work, assistance received and pending question. Budget about an hour including a retry. Prepare a labeled fallback output for tools that might fail.

Deliver runnable lesson materials in the host format. Replay a successful path and a missed-answer path against the actual prompts. For every scored decision, check that the learner saw the evidence it requires. Report observed outcomes and label unmeasured timing as an estimate.
