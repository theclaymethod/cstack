# Opt-in lifecycle hooks for Expert Mode

Installing CStack **never installs or activates capture hooks**. Passive capture stays off by default, and no executable hook scripts ship in the skill pack. Use this optional, project-local setup only if you want deterministic harness reminders so active Expert Mode sessions do not forget to record judgments or lose active state across compaction.

## Session-gated marker contract

To preserve CStack's privacy and activation rules ("installing skills does not activate capture"; "capture stays local unless you request an export"; "a new session needs a new invocation"), every hook must stay a silent no-op unless an explicit session-scoped marker exists:

1. **Activate:** Only on explicit `/expert-mode` or `$expert-mode` invocation, create a local ignored state file for the current session ID—for example `eval-runs/.expert-mode-state/<session_id>.json` containing `{"active": true, "session_id": "...", "dataset_path": "...", "pending_ids": []}`.
2. **Gate every hook:** Each hook script reads the harness hook JSON payload on `stdin`, extracts the session/conversation identifier, checks whether that exact session's marker file has `"active": true`, and exits `0` silently if absent or inactive.
3. **Stop:** When the user stops Expert Mode, set `"active": false` (or remove the marker) so hooks immediately return to silent no-ops. A new session has a new session ID and therefore starts inactive.
4. **Never auto-label or upload:** Hooks only inject concise reminders (e.g., preserve active state before compaction, or flush supported explicit judgments before stopping). They never fabricate expert labels, infer approval from silence or code edits, read unrelated sessions, or transmit data.

## Per-harness opt-in setup

Keep hook scripts project-local (for example under `.cstack-hooks/` or `scripts/`) and keep `.expert-mode-state/` ignored in `.gitignore`. Verify exact event schemas against your installed harness version before enabling.

### Claude Code

Configure project-local hooks in `.claude/settings.json` (never bundle auto-active hooks into a shared plugin):

- **`PreCompact`:** When the current `session_id` marker is active, emit active mode, `dataset_path`, record/criterion IDs, and any `pending_ids` so compaction preserves capture identity.
- **`Stop`:** When active and the turn contained explicit user feedback not yet flushed to `dataset_path`, return a brief reminder to persist supported records (or report unsaved blockers) before finishing. Guard against stop-hook loops by checking `stop_hook_active` or a turn marker.
- **`UserPromptSubmit` (optional):** When active, inject a one-line reminder that Expert Mode is recording explicit judgments locally to `dataset_path`.

### OpenAI Codex

Configure project-local hooks in `.codex/hooks.json` (and explicitly review and trust them via `/hooks`):

- **`PreCompact`:** Inject active Expert Mode session/dataset/pending state before compaction when the matching session marker is active.
- **`Stop`:** Remind the agent to verify that explicit judgments from the turn were appended to `dataset_path` (with a loop guard) only while the session marker is active.
- **`UserPromptSubmit` (optional):** Inject a compact active-mode reminder for that session only.

### Cursor

Configure project-local hooks in `.cursor/hooks.json` (`"version": 1`):

- **`preCompact`:** When the session/conversation marker is active, preserve active Expert Mode state, `dataset_path`, and `pending_ids` before context compaction.
- **`beforeSubmitPrompt` (optional):** When the session marker is active, pass a brief active-mode context reminder.
- **`stop`:** When active and unsaved capture items remain, emit a one-time follow-up check (bounded to prevent repeat loops).

## Graceful fallback without hooks

If hooks are not configured or unsupported by the host harness, Expert Mode works identically through inline persistence: write supported observations in the same turn, carry active mode, paths, IDs, and unsaved work in compaction summaries, and fall back to [Distill Me](../../distill-me/SKILL.md) if any turn was missed.
