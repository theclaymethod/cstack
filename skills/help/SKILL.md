---
name: help
description: On explicit /help invocation, inspect the workspace's CStack artifacts and recommend the single next skill. Use when the user asks where they are, what to run next, or which skill fits the current eval work.
---

# Help

Lead user-facing replies with the result or decision needed. For several points, put each in its own short, plain-language bullet. A single answer can be one sentence. Link detailed evidence. Preserve open questions, approval gates and any requested artifact format.

On explicit invocation, answer with the next skill and the workspace observation that made it the next step. Discussion is not invocation. Do not start that skill, edit the product, or run candidates unless the user asks.

## Inspect

Run this skill's `scripts/inspect_workspace.py` with `--root` set to the working project. The script is read-only. It prints one JSON object: what it found, what is stale, and `recommendation.skill` plus `recommendation.why`.

Read [what the scan counts](references/inspection.md) before treating a missing path as absence. Historical files inside a cstack checkout's `evals/` directory are pack evidence, not the user's campaign. A materialized playground keeps user work under `eval-runs/` and `evals/generated/`.

If the script cannot run, follow [the same order](references/next-step.md) by reading the files yourself. Say that the inventory was manual.

## Answer

Lead with the one skill and the reason, naming the evidence paths. Use `/name` in Claude Code and Cursor, and `$name` in Codex. Mention at most one extra stale fact when `stale` is non-empty and the recommendation is not already about it. Do not offer a menu of skills.

If a [shared decision ledger](../create-eval/references/decision-ledger.md) names a pending handoff, follow its evidence link. Recommend the receiving skill when the artifact still needs that work. Leave the ledger untouched during routing.

Explain any override. Two other observations can change the recommendation.

- The current session has explicit user judgments that are not in the saved records. Recommend `/distill-me`. File inspection cannot see unsaved chat.
- You opened a record the script called incomplete and it actually ties a judgment, an input, an output, and a criterion together. Follow the next rule in [the order](references/next-step.md).

An incomplete tutor checkpoint outranks a failing playground baseline. It does not outrank a stale measurement contract, an active or incompatible campaign, an open ledger, or pending scenario cards.

## Limits

The inventory is a file heuristic. A hash mismatch means the bytes changed, not why. A ledger line is not an independent review. Synthetic fixture labels are not human gold. Capture, fitting, publication, and product edits need their own authority.
