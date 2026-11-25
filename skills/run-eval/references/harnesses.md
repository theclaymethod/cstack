# Harness orchestration and isolation

Core CStack skills stay harness-agnostic. Use this reference to map isolated roles, parallel fan-out, Git worktrees, deterministic loops, and model diversity onto your actual harness—without inventing APIs or hiding missing isolation.

## Isolation rules that apply everywhere

- **Fresh subagent vs. forked context:** Blind judges (`run-eval`, `calibrate-judge`, `co-climb`), independent intent reviewers (`cross-examine`), blinded control validators (`create-eval`), and post-redaction export reviewers (`expert-mode`) require a **fresh, non-forked** context receiving only allowlisted inputs. A forked conversation inherits parent history and never establishes blindness or independence.
- **Single coordinator for canonical writes and commits:** Parallel workers write only to their own scratch directory or Git worktree and return **uncommitted** patches or snapshots. One coordinator reserves budget before fan-out, merges outputs, updates the shared decision ledger, runs change-review checkpoints, and obtains explicit user acceptance before any Git commit (including local or worker commits).
- **Worktrees are not security sandboxes:** Git worktrees prevent file collisions and protect the live branch during `hill-climb`, `co-climb`, `ablation`, `bitter-lesson`, `cross-examine`, and `adversarial-cases`, but code still executes with host permissions. Use Harbor/container or OS isolation when containment is part of the claim.
- **Tool scoping:** Restrict reviewers, extractors, and judges to read-only tools where the harness supports it. Keep gold labels, rationales, and operator receipts outside judge and attacker tool access. No custom MCP server is required; if the project already exposes eval or trace tools via MCP, treat them as project tools under the same allowlist boundary.

## Per-harness capabilities

### Claude Code

- **Isolated subagents:** Spawn fresh subagents (or define project roles in `.claude/agents/*.md`) with restricted `tools` (read-only for judges and reviewers) and an explicit `model` when authorized. A local skill may set `context: fork` only when it needs isolated subagent execution without parent conversation history; never treat a conversation fork that inherits parent transcript as blind.
- **Worktree isolation:** Use subagent `isolation: "worktree"` or `--worktree` so parallel candidates, ablation subsets, model-comparison cells, and audit repairs run in separate checkouts under `.claude/worktrees/` (optionally paired with `WorktreeCreate`/`WorktreeRemove` hooks for custom project setup). Return uncommitted diffs to the coordinator rather than committing inside workers.
- **Parallel & deterministic orchestration:** Use parallel subagents for small independent batches (3–5 workers), or **Dynamic Workflows** (script-driven orchestration) for deterministic multi-step loops (`hill-climb`, `co-climb`, `ablation`, `cross-examine`, large `run-eval` suites) where loops and intermediate results stay in code. Reserve **Agent Teams** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) for collaborative peer streams—never use peer-to-peer messaging for blind judges or independent intent reviewers that must not communicate.
- **Explicit-only skills:** `expert-mode`, `distill-me`, `help`, and `tutor` keep portable frontmatter (`name`, `description`). A local Claude Code copy may add `disable-model-invocation: true` in its local frontmatter for strict invocation gating.

### OpenAI Codex

- **Isolated subagents:** Use multi-agent subagents (`/subagents` or TOML role definitions in `.codex/agents/`) to pin read-only sandboxes, tool bounds, and authorized models per role.
- **Worktree isolation:** Create per-candidate or per-cell checkouts with standard `git worktree add` before dispatching parallel editing/execution workers; keep worker changes uncommitted, snapshot results and diffs back to the coordinator, and clean up disposable worktrees afterward.
- **Deterministic loops:** Drive freeze → reserve → fan-out → hash-verify → compare state machines with narrow project-local Python scripts so ledger accounting, budget caps, and exposure checks do not rely on turn-by-turn model memory.
- **Explicit-only skills:** `expert-mode`, `distill-me`, `help`, and `tutor` include `agents/openai.yaml` with `policy.allow_implicit_invocation: false` so Codex requires explicit `$expert-mode`, `$distill-me`, `$help`, or `$tutor` invocation.

### Cursor

- **Isolated subagents:** Use built-in or project-defined subagents (`.cursor/agents/`) running in separate context windows (foreground for blocking verification, background for parallel extraction lenses, scenario slices, or candidate trials).
- **Worktree & cloud isolation:** Use local Git worktrees (configured with `.cursor/worktrees.json` setup scripts) for parallel local candidates, or Cloud Agents (`.cursor/environment.json`) for long-running asynchronous campaigns in isolated remote VMs. Keep proposed edits uncommitted until user acceptance.
- **Deterministic loops:** Pair subagents with project-local Python/shell scripts for allowlist projection, verdict freezing, and campaign ledgers.

## Cross-provider model diversity (optional)

When a project has authorized access to multiple model providers, prefer a **different model family** for blind semantic judging (`run-eval`, `calibrate-judge`, `co-climb`), independent intent review (`cross-examine`), or fixed cross-cell scoring (`bitter-lesson`) than the model generating candidate outputs. This reduces self-preference and correlated blind spots.

- Never silently call unconfigured or paid external APIs.
- Pin and record the exact judge provider/model identifier (or `unknown`) in the frozen run manifest.
- Keep judge model/version fixed across baseline and candidate comparisons.

## Graceful degradation (single-agent or limited harnesses)

If the current harness lacks subagents, parallel execution, or Git worktrees, every CStack skill still runs locally with these required disclosures:

1. **No fresh subagents:** Run extraction lenses or control checks sequentially, keep allowlist projection and verdict hashing in code, and explicitly disclose any prior exposure to generator reasoning or gold labels. For `cross-examine`, mark formal intent adjudication **unreviewed**—sequential self-review never establishes independence.
2. **No parallel fan-out:** Run slices, candidates, or matrix cells sequentially while keeping per-item budget reservations and separate output directories. Disclose local-only coverage where independent parallel authors were unavailable.
3. **No Git worktrees:** Evaluate candidates in disposable temporary copies or serialized snapshots, never editing the canonical target until a candidate is confirmed and authorized by the user.
4. **No lifecycle hooks:** For `expert-mode`, rely on same-turn writes and explicit compaction handoff summaries.
