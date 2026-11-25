# CStack Agent Architecture

This document explains how CStack's 15 skills map onto modern agent harnesses (Claude Code, OpenAI Codex, and Cursor) while preserving single-agent portability, zero external runtime dependencies, local-first privacy, and explicit user-approval gates.

## Why redesign for modern agent harnesses

Earlier versions of CStack compressed strong eval methodology into lean instructions, but several skills still carried **single-linear-chat assumptions**:

- **Self-judging and context contamination:** `run-eval` defaulted to *"the active agent as a judge"*, even when that same session had edited the target or read `cases.jsonl` (including gold labels and rationales). Prose instructions cannot make an already-exposed context blind.
- **Compliance-only capture:** `expert-mode` relied entirely on the model remembering to log judgments on every turn and carry active state across compaction.
- **Sequential bottlenecks on embarrassingly parallel work:** `distill-me` lenses, optional `bootstrap` scenario-expansion slices, `cross-examine` attacker hypotheses, `hill-climb` and `co-climb` candidate branches, `ablation` subsets, and `bitter-lesson` model-by-design cells all benefit from parallel fan-out.
- **Shared-workspace mutation risk:** `hill-climb`, `co-climb`, `ablation`, `bitter-lesson`, and `cross-examine` edits in one working tree risk colliding with concurrent candidates or dirtying the user's live branch.
- **Mixed LLM and code responsibilities:** Deterministic mechanics (allowlist projection, verdict hashing, budget reservations, post-freeze gold comparison, workspace inventory, progress journaling, ddmin sweeps) belong in narrow code/scripts or workflow loops rather than model memory.

## Capability triage: what we adopt and what we leave out

Every modern harness primitive was evaluated against whether it actually improves eval validity, reliability, or speed for these 15 skills:

| Capability | Decision | Where it applies | Why / boundary |
| --- | --- | --- | --- |
| **Fresh (non-forked) subagents** | **Adopt (core)** | `run-eval`, `cross-examine`, `calibrate-judge`, `co-climb`, `create-eval`, `distill-me`, `expert-mode` (export review) | Prevents generator reasoning, tuning history, or gold labels from leaking into judges, intent reviewers, control validators, and privacy reviewers. **Forked** conversations inherit parent history and therefore never establish blindness or independence. |
| **Parallel fan-out & background tasks** | **Adopt (core)** | `distill-me`, `bootstrap` (optional expansion), `run-eval`, `cross-examine`, `hill-climb`, `co-climb`, `ablation`, `bitter-lesson`, `adversarial-cases` | Speeds up independent lenses, scenario slices, attack hypotheses, case batches, and candidate sweeps. Requires a single coordinator for canonical writes, shared decision ledger updates, and pre-reserved budgets before fan-out. |
| **Deterministic code & workflow drivers** | **Adopt selectively** | `hill-climb`, `co-climb`, `ablation`, `bitter-lesson`, `cross-examine`, `calibrate-judge`, `run-eval`, `help`, `tutor`, `author-short-tutor` | Enforces freeze → reserve → execute → hash-verify → compare state machines, workspace inventory (`inspect_workspace.py`), append-only progress (`progress.py`), and formal path checks (TLC) without trusting turn-by-turn model memory. Human interviews and change-review checkpoints stay interactive. |
| **Independent verifier / judge roles** | **Adopt (core)** | `run-eval`, `create-eval`, `calibrate-judge`, `cross-examine`, `hill-climb`, `co-climb`, `ablation`, `bitter-lesson` | Judges and verifiers see only allowlisted runtime payloads or raw replay evidence—never generator reasoning or hidden gold. Matches verifier modality to the promise and splits brittle code checks from semantic judging. |
| **Git worktree isolation** | **Adopt (core)** | `hill-climb`, `co-climb`, `ablation`, `bitter-lesson`, `cross-examine`, `adversarial-cases` | Lets parallel candidate edits, deletion subsets, model-comparison cells, and repair checks run without file collisions or touching the live branch. Workers return **uncommitted** patches/snapshots (no worker commits before explicit user acceptance). Does **not** provide OS/host security containment. |
| **Opt-in session-gated hooks** | **Adopt (reference only)** | `expert-mode` | Deterministic `PreCompact`/`Stop`/`UserPromptSubmit` (or Cursor `preCompact`/`beforeSubmitPrompt`/`stop`) reminders prevent missed captures and compaction amnesia. Reference-only: no executable hook code ships, installing activates nothing, and hooks stay dormant without an explicit per-session activation marker. |
| **Tool & MCP boundaries** | **Adopt role scoping; no bundled MCP** | All delegated roles | Restrict read-only reviewers, extractors, and judges from writing files or reading gold stores; keep attackers within candidate-equivalent permissions. Bundling an MCP server is rejected to preserve zero-dependency portability. |
| **Progressive disclosure** | **Adopt (core)** | All 15 `SKILL.md` files | Keep `SKILL.md` files lean and concise, putting harness-specific details in shared references (`skills/run-eval/references/harnesses.md` and `skills/expert-mode/references/hooks.md`). |
| **Trigger-reliable descriptions** | **Adopt (core)** | All 15 frontmatter `description` fields | Keep strictly portable `name` + `description` keys (Agent Skills standard) with non-overlapping trigger cues; keep `expert-mode`, `distill-me`, `help`, and `tutor` explicit-only (`agents/openai.yaml`). |
| **Harbor-style executable tasks** | **Adopt (core)** | `create-eval`, `run-eval`, `calibrate-judge`, `cross-examine` | Separates `instruction.md` + `environment/` from `tests/test.sh` (mounted only after agent completion to write `/logs/verifier/reward.{txt,json}`), providing real container/filesystem isolation where prose cannot. |
| **Cross-provider model diversity** | **Adopt (optional, authorized)** | `run-eval`, `calibrate-judge`, `co-climb`, `cross-examine`, `bitter-lesson` | Using a distinct model family/provider for judging or intent review reduces self-preference bias. Strictly opt-in when configured and authorized; never trigger silent paid calls. |

## Core architectural patterns

### 1. Fresh isolated context vs. forked context

- **Fresh subagent (no parent transcript):** Required for blind semantic judging (`run-eval`, `calibrate-judge`, `co-climb`), independent intent review (`cross-examine`), blinded control validation (`create-eval`), and post-redaction export review (`expert-mode`). Pass only the allowlisted payload or frozen evidence files.
- **Forked conversation (inherits parent transcript):** Useful only when a worker needs existing conversation state without cluttering the main thread. Never claim blindness or independent adjudication from a forked conversation.

### 2. Code owns mechanics; models own judgment

Across every skill, separate:

- **Deterministic code:** schema checks, allowlist payload projection, deterministic code checks (kept separate from semantic judging when paraphrases/negation arise), content/verdict hashing, budget reservation and reconciliation, post-freeze gold comparison, agreement/error statistics, search/reduction scheduling, workspace inspection (`help`), append-only progress journaling (`tutor`), and statechart checking (`author-short-tutor`).
- **LLM roles:** Socratic intent interviewing, scenario synthesis, hypothesis generation, semantic judging against binary criteria, adversarial hypothesis generation, passing-trace inspection, and independent intent adjudication.

### 3. Single coordinator for canonical writes, ledgers, and human checkpoints

Parallel workers write only to their own scratch paths or Git worktrees and return **uncommitted** patches or snapshots. One coordinator merges outputs, deduplicates records, updates the shared decision ledger (`skills/create-eval/references/decision-ledger.md`), reserves budget before dispatching batches, leads change reviews with user-visible effects, obtains explicit user acceptance before any Git commit or target adoption, and manages human-in-the-loop checkpoints (including `calibration-capture.md` offers).

### 4. Honest isolation and modality boundaries

- **Context isolation** (fresh subagent) prevents accidental leakage of generator reasoning or labels.
- **Git worktree isolation** prevents parallel file collisions and protects the live working branch.
- **Container/OS isolation** (e.g., Harbor/Docker or OS access controls) is still required for hostile-code containment or enforced oracle protection. Never claim security containment from local scratch directories, timeouts, or worktrees alone.
- **Verifier modality:** Do not substitute an eval suite for formal concurrency/ordering verification or live end-to-end UI visual proof; capture actual channel artifacts (screenshots, recordings, audio, resulting state) rather than grading text summaries alone.

## Per-skill assessment and target design

### 1. `expert-mode`

- **Purpose & handoffs:** Capture explicit expert judgments, corrections, and binary rubric criteria during live work into local JSONL (`records.md`), linking permitted pointers in the shared decision ledger; consumed by `distill-me`, `create-eval`, `calibrate-judge`, and optional `export.md`.
- **Changes & architecture:**
  - **Inline (primary session):** Live observation during authorized work and immediate same-turn persistence (single writer or separate concurrent files).
  - **Opt-in lifecycle hooks (`references/hooks.md`):** Reference-only guidance for project-local `PreCompact`, `Stop`, and prompt hooks gated on an explicit per-session activation marker so active mode and unsaved entries survive compaction without activating on install.
  - **Fresh read-only subagent (export only):** When exporting (`references/export.md`), dispatch a fresh read-only reviewer given *only* the redacted bundle (never private originals) to check remaining PII and eval-meaning preservation.
  - **Invocation guard:** Explicit-only (`agents/openai.yaml` `allow_implicit_invocation: false`; optional local Claude Code `disable-model-invocation: true` documented in `harnesses.md`).
- **Graceful degradation:** Without hooks, preserve active state and pending records in compaction handoffs inline. Without subagents, perform export review inline and disclose that the reviewer saw the unredacted source.

### 2. `distill-me`

- **Purpose & handoffs:** One-shot retrospective extraction of expert judgments and binary criteria from the current session, merged into shared local records without duplicates and linked in the shared decision ledger; leaves `expert-mode` state unchanged.
- **Changes & architecture:**
  - **Coordinator (inline):** Identifies bounded authorized current-session source and existing dataset; verifies final quotes against source; executes single serialized merge write and reports summary.
  - **Parallel fresh read-only subagents (3 lenses):** Corrections lens, Rubric lens, and Evidence-quality lens run concurrently in isolated read-only contexts over the bounded source, returning structured candidate records without seeing each other's passes.
  - **Fork boundary:** Never run `distill-me` in a history-less fork unless the current session transcript/excerpts are explicitly passed in.
- **Graceful degradation:** Run the three lenses sequentially in the main session, keeping quote verification and single-pass merge discipline intact, and disclose sequential extraction.

### 3. `bootstrap`

- **Purpose & handoffs:** Run a Socratic interview (aligned with Understando-style boundary discovery) to surface competing product rules, confirm topic readbacks, and build an approved `SCENARIOS.md` index handed off through the shared decision ledger to `create-eval`.
- **Changes & architecture (respecting upstream Socratic redesign):**
  - **Inline (core):** The entire Socratic interview—opening from an incident or ordinary example, finding distinguishing contrast questions, topic readback confirmations, and separate-turn `SCENARIOS.md` approval—stays strictly interactive in the main session.
  - **Parallel scenario-author subagents (optional expansion only):** When expanding approved boundaries into broader scenario proposals under `references/scenarios.md`, fan out independent scenario authors by coverage slice (read-only on repo, scratch-only writes) returning proposed expectations only—never gold or evaluator code—for the coordinator to merge before owner review.
  - **Clean handoff:** Evaluator authoring and isolated control validation live in `create-eval` and `run-eval`, not inside the `bootstrap` interview.
- **Graceful degradation:** Generate optional expansion slices inline and explicitly disclose local-only coverage.

### 4. `create-eval`

- **Purpose & handoffs:** Convert reviewed findings, `SCENARIOS.md`, `situations.md`, or early traces into repeatable eval cases, deterministic checks, and binary rubrics with matching verifier modality, wrong-product controls, and offline verifier replays; hands off to `calibrate-judge`, `run-eval`, and `cross-examine`.
- **Changes & architecture:**
  - **Inline / human checkpoints:** Evidence triage, `review_traces.py` trace review, modality matching, and unresolved clarifications.
  - **Parallel workers (optional):** Early-development trace collection across scenario slices in disposable scratch/worktree states.
  - **Fresh control-runner / leakage-checker subagent:** Executes legitimate, failing, boundary, alternative, and wrong-product controls (right-artifact/wrong-content and always-emit + negative-space guard) plus offline code-check replays through the real grading path, and audits allowlisted judge payloads for label leakage before leaving draft status.
  - **Harbor preference (`references/formats.md`):** New executable agent tasks physically separate `instruction.md` + `environment/` from `tests/test.sh` and `/logs/verifier/reward.{txt,json}`.
  - **Code vs. semantic split (`references/judges.md`):** Preserves splitting brittle code checks from calibrated semantic judges while running semantic judges in fresh isolated contexts.
- **Graceful degradation:** Execute controls and replays inline via deterministic scripts and disclose that the author checked its own draft package.

### 5. `calibrate-judge`

- **Purpose & handoffs:** Fit and validate an automated judge (typed Jev-style or LLM judge) against authoritative labeled outcomes; delivers a frozen judge bundle to `run-eval` after user-visible change review and explicit adoption approval; optionally uses `hill-climb`, `adversarial-cases`, and `cross-examine`.
- **Changes & architecture:**
  - **3-role split:**
    1. **Proposer / tuner (coordinator or worker):** Inspects only exposed development disagreements to refine prompts, examples, or typed questions.
    2. **Blinded judge executor (fresh subagent or separate backend process):** Receives only allowlisted runtime payloads—never gold, rationales, split names, or tuning history. Supports parallel batch/repeat runs under pre-reserved budgets and optional authorized **cross-provider model diversity**.
    3. **Deterministic comparator (code):** Freezes predictions and hashes before reading gold, computes confusion counts, kappa, class errors, coverage, Brier/log-loss, and enforces final-exposure guards.
  - **User approval gate preserved:** Pending candidate judges stay separate and uncommitted until user-visible review and explicit approval.
- **Graceful degradation:** Run sequentially with code-enforced allowlist projection and pre-comparison freeze hashes; explicitly disclose context contamination if the same session already viewed gold labels.

### 6. `run-eval`

- **Purpose & handoffs:** Execute a frozen eval package through the project's trusted runner, freeze verdicts before comparing labels, record run receipts in the shared decision ledger, and report results, errors, coverage, and limits; feeds `cross-examine`, `hill-climb`, `co-climb`, `ablation`, and `calibration-capture.md`.
- **Changes & architecture:**
  - **Code owns mechanics:** Allowlist projection (`package.md`), deterministic checks, hashing/freezing complete verdicts, and post-freeze gold comparison/metrics.
  - **Fresh isolated judge subagent(s) (read-only):** Replaces *"the active agent as a judge"*. Evaluates semantic binary criteria from allowlisted blind payloads only—never inheriting generator reasoning, editing history, or gold labels. Fans out parallel batches across independent cases/criteria when suite size warrants; runs long suites in the background; supports authorized cross-provider model diversity.
  - **Inline coordinator:** Freezes run contract, inspects actual results alongside inputs, surfaces traces/anomalies, reports limits, and offers calibration capture separately from run scores.
- **Graceful degradation:** When subagents are unavailable, fall back to the active agent for semantic judging *only* with explicit disclosure of any prior exposure to generator reasoning or gold labels.

### 7. `cross-examine`

- **Purpose & handoffs:** Adversarial audit of eval tasks, environments, and verifiers (targeting wrong-modality and proxy assertions as primary surfaces) using attacker, defender, and fresh independent intent reviewer; proposes repairs and lessons for explicit user adoption and updates the shared decision ledger.
- **Changes & architecture:**
  - **Parallel isolated attackers:** Independent initial hypotheses in separate resettable scratch/worktree states with candidate-equivalent tool permissions (no operator receipts or hidden oracles).
  - **Strictly fresh, non-forked, read-only intent reviewer:** Never shares context with authors, attackers, repairers, or coordinators; ideally uses an authorized distinct model/provider. Receives original intent first, then frozen source and raw replay evidence—never persuasion or prior verdicts. Runs before accepting a finding and again after freezing a repair.
  - **Isolated defender (worktree):** Authors candidate repairs in an isolated worktree, replays exploits and legitimate baselines from clean state, and returns uncommitted diffs for independent intent review and explicit user adoption (never committing inside workers).
  - **Deterministic workflow script (optional):** Orchestrates freeze → attack → replay → review → repair → re-review → teach without leaking verdicts between roles.
- **Graceful degradation:** Disclose missing role separation, serialize scratch writes, and mark formal intent adjudication **unreviewed** (sequential self-review never establishes independence).

### 8. `adversarial-cases`

- **Purpose & handoffs:** Challenge existing evals with harder situations implied by the product spec (maintaining `situations.md` and appending dispositions to the shared decision ledger for `create-eval`), and construct minimal reproducible fault/boundary cases for `bootstrap`, `cross-examine`, and `co-climb`.
- **Changes & architecture:**
  - **Parallelizable isolated worker role:** Dispatched per boundary or fault hypothesis in a disposable scratch directory or Git worktree; read-only on canonical evals, gold labels, and production targets; traces proposed challenges through product entrypoints to drop already-guarded or duplicate cases.
  - **Deterministic drivers:** Code runs bounded fault activation, clean/no-op/legitimate controls, and delta-debugging reduction loops; agent designs causal hypotheses and inspects activation/outcome witnesses.
  - **Coordinator-owned canonical state:** Parent/coordinator owns canonical `situations.md` merges, expectation approval, owner discovery questions, adjudication, and calibration-capture offers.
- **Graceful degradation:** Runs inline under the parent's serialized scratch state with the same activation/control and entrypoint-tracing requirements.

### 9. `hill-climb`

- **Purpose & handoffs:** Bounded optimization of a prompt, skill, program, or harness against a fixed evaluator; consumes `run-eval`, optional `cross-examine`, inspects a passing trace end to end before proposing adoption, and hands off to `ablation`/`bitter-lesson`.
- **Changes & architecture:**
  - **Worktree isolation per candidate:** Each hypothesis-driven candidate edits and executes inside its own Git worktree (or isolated snapshot directory) against the immutable, hash-verified evaluator, returning uncommitted patches/snapshots (never committing before explicit user acceptance).
  - **Parallel candidate fan-out + deterministic campaign driver:** Coordinator reserves total batch and confirmation spend *before* dispatching parallel proposer/runner worktrees, reconciles native execution receipts into the durable ledger, and runs confirmation on a frozen shortlist in a clean checkout.
  - **Role separation & trace inspection:** Proposers see only permitted development failures; judge/verifier execution stays isolated from proposer reasoning; coordinator reads one passing trace per target end to end and leads change review with user-visible effects before adoption.
- **Graceful degradation:** Snapshot and evaluate candidates sequentially in isolated temp copies; preserve the same pre-run reservations, immutable evaluator checks, confirmation reserve, and explicit-acceptance gates.

### 10. `co-climb`

- **Purpose & handoffs:** Strengthen evals and improve the generator together over bounded cycles (alternating target search, judge calibration, and adversarial case challenges) through the shared decision ledger, with rank-reversal regrading, change-review checkpoints, and a once-only sealed final comparison.
- **Changes & architecture (new since earlier rewrite):**
  - **Single coordinator:** Owns cycle budget, pre-reserved spend and confirmation reserve, shared decision ledger, branch archive cap, cumulative user-visible change-review checkpoints, and sealed final comparison.
  - **Parallel worktree target workers:** Execute competing target hypotheses in isolated Git worktrees against one frozen evaluator, returning uncommitted patches/snapshots (never worker commits before explicit user acceptance).
  - **Fresh blind judge executor + deterministic comparator:** Judge fitting and saved-corpus regrading run in fresh, non-forked, read-only contexts over allowlisted payloads (optionally with authorized cross-provider diversity), while deterministic code freezes predictions/hashes before reading gold, checks evidence parity, and invalidates/recomputes ranks after judge changes.
  - **Isolated adversarial-case workers:** Probe covered promises in scratch/worktree state and return witness-backed candidates for coordinator admission to `situations.md`.
- **Graceful degradation:** Execute target branches, judge rebuilds, and adversarial probes sequentially from snapshotted baselines under the same budget, regrading, exposure, and non-independence disclosures.

### 11. `ablation`

- **Purpose & handoffs:** Remove prompt instructions, examples, context, tools, or workflow steps while meeting original-baseline quality constraints; reuses `hill-climb` campaign mechanics and change-review gates, and pairs with `bitter-lesson`.
- **Changes & architecture:**
  - **Agent owns structure:** Defines semantically coherent removal units, protected meaning, and dependency closures.
  - **Parallel worktree execution + deterministic driver:** Code schedules coarse groups, leave-one-out checks, and combined deletion closures concurrently across isolated worktrees (returning uncommitted candidates), tracks rendered burden (bytes/tokens/tool calls), enforces original-baseline quality gates, and binds execution ledgers to reservations.
  - **Isolated evaluator/judge:** Any semantic judging runs in a fresh context unaware of which units were deleted; permanent removals wait for explicit user approval.
- **Graceful degradation:** Evaluate subsets sequentially from snapshotted baselines, preserving combined-artifact testing, original-baseline gates, and explicit-acceptance gates.

### 12. `bitter-lesson`

- **Purpose & handoffs:** Revisit inherited prompts, context, and scaffolding when upgrading models across the 2×2 Model × Design matrix (A: old/full, B: old/simplified, C: new/full, D: new/simplified); uses `ablation` and `hill-climb` and waits for user-visible bundle approval.
- **Changes & architecture:**
  - **Parallel worktree cell execution:** Freeze and run each authorized cell (A, B, C, D) in its own Git worktree or run directory with pinned model/version, assembled prompt, tools, and settings, returning uncommitted candidates.
  - **Blind fixed judge:** Hold the approved evaluator fixed across all cells; when semantic judging is used, run a fresh isolated (and ideally authorized cross-provider) judge blind to which model/design cell produced each output.
  - **Harness-aware simplification:** Treat replacing fragile prose reminders with deterministic hooks, tool restrictions, or verifier scripts as an explicit candidate intervention (recorded separately from literal deletion).
- **Graceful degradation:** Run available cells sequentially, leave unavailable old-model cells explicitly unrun, and disclose any shared judging context.

### 13. `help` *(no structural change needed)*

- **Purpose & handoffs:** Read-only workspace router invoked explicitly (`/help` or `$help`) to recommend the single next CStack skill.
- **Assessment:** Already implements **"code owns mechanics; model owns judgment"** cleanly: `scripts/inspect_workspace.py` performs deterministic read-only file scanning, hash comparison, and staleness checks, while the inline agent combines that JSON inventory with unsaved session context to name one next skill. Adding subagents, worktrees, or hooks would add latency and complexity with zero validity gain. Kept unchanged (with its existing `agents/openai.yaml` explicit-only policy).

### 14. `tutor` *(no structural change needed)*

- **Purpose & handoffs:** Interactive hands-on course (`/tutor` or `$tutor`) teaching a builder to turn one product boundary into a checked eval or work through the 13-exercise playground.
- **Assessment:** Inherently single-threaded, learner-paced Socratic dialogue backed by deterministic append-only progress journaling (`scripts/progress.py`). Subagent fan-out, worktrees, and capture hooks do not improve an interactive teaching loop. Kept unchanged (with its existing `agents/openai.yaml` explicit-only policy).

### 15. `author-short-tutor` *(no structural change needed)*

- **Purpose & handoffs:** Interactive course-authoring workflow for designing a one-hour agent-led tutor around an independent learner decision.
- **Assessment:** Owner interview + deterministic formal path verification (statechart + TLC model checking) + interactive lesson drafting. Already separates deterministic model-checking mechanics from owner-facing dialogue. While an author may optionally test finished lesson prompts in a fresh subagent cold replay, forcing orchestration boilerplate into this meta-skill is unnecessary. Kept unchanged.

## Cross-harness mapping summary

Harness-specific details live in [the shared harness reference](../skills/run-eval/references/harnesses.md) and [the opt-in hooks reference](../skills/expert-mode/references/hooks.md) so core `SKILL.md` files stay portable and install cleanly via `npx skills add`.

| Architectural primitive | Claude Code | OpenAI Codex | Cursor | Single-agent fallback |
| --- | --- | --- | --- | --- |
| **Fresh isolated subagent** | Subagents / `.claude/agents/*.md` with scoped `tools` & `model`; `context: fork` only for history-less skill isolation (never conversation fork for blindness) | Multi-agent subagents (`/subagents`, TOML roles in `.codex/agents/` with model/sandbox/tool bounds) | Subagents (`.cursor/agents/`, foreground or background) | Inline pass with explicit exposure/non-independence disclosure |
| **Parallel fan-out & deterministic loops** | Parallel subagents or Dynamic Workflows (scripted orchestration); avoid Agent Teams for blind/isolated judges | Parallel subagent threads + local Python driver script | Parallel subagents or Cloud Agents (`.cursor/environment.json`) | Sequential execution driven by local Python scripts |
| **Worktree isolation** | Subagent `isolation: "worktree"` or `--worktree` (`.claude/worktrees/`); workers return uncommitted diffs | `git worktree` per candidate/branch; workers return uncommitted diffs | Local worktrees (`.cursor/worktrees.json`) or Cloud Agent VMs; keep pending edits uncommitted | Disposable temp/snapshot copies; serialize writes |
| **Opt-in passive capture hooks** | Project `.claude/settings.json` (`PreCompact`, `Stop`, `UserPromptSubmit`), gated on session marker | `.codex/hooks.json` (`PreCompact`, `Stop`, `UserPromptSubmit`), explicitly trusted via `/hooks`, gated on session marker | `.cursor/hooks.json` (`preCompact`, `beforeSubmitPrompt`, `stop`), gated on session marker | Inline capture + compaction handoff summary |
| **Explicit-only invocation** | Optional local `disable-model-invocation: true` (outside portable core frontmatter) | `agents/openai.yaml` (`policy.allow_implicit_invocation: false`) | Manual `/` invocation + explicit-only description | Explicit-only description contract |

## Preserved safety, privacy, and portability invariants

1. **Install does nothing passive:** Running `npx skills add ...` or copying the skill folders installs no hooks, activates no capture, and uploads nothing.
2. **Capture stays local:** Expert Mode, Distill Me, and calibration-capture offers write only to local project paths unless the user explicitly requests an export and separately directs sharing.
3. **Explicit user acceptance before commits or adoption:** Automated search, repair, ablation, calibration, and migration workers return uncommitted patches or snapshots; no Git commit (local or worker) or target replacement happens without explicit user acceptance after user-visible review.
4. **Portable skill packaging:** All 15 skill names, portable `SKILL.md` frontmatter (`name` + `description`), shared `../<skill>/references/` relative paths, and the `npx skills add` install command remain working and zero-dependency.
5. **Honest claims:** Worktrees are not sandboxes; sequential self-review is not independent adjudication; synthetic controls are not human gold; unrun cells or missing providers stay explicitly unrun.
