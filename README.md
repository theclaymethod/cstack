# C Stack

Turn expert feedback into evals you can trust.

C Stack is a portable skill pack for people working with Claude Code, Codex, Cursor, or another coding agent. Capture expert judgments, distill a session, build and run repeatable evals, then challenge whether they measure what you intended.

C Stack replaces the standalone [Cross-Examine](https://github.com/theclaymethod/cross-examine) and [Eval Creator](https://github.com/theclaymethod/eval-creator-skill) skill repositories. Both are archived with migration links here; their history remains available. See [SOURCES.md](SOURCES.md) for what moved and which project-specific tools remain in the archives.

| Skill | When to use it |
| --- | --- |
| [Expert Mode](skills/expert-mode/SKILL.md) | Start a working session with `/expert-mode`. Keep replies short while quietly recording explicit errors, corrections, and yes/no rubric criteria. |
| [Distill Me](skills/distill-me/SKILL.md) | Run `/distill-me` afterward to recover supported judgments from the session and merge them without duplicating live captures. |
| [Create Eval](skills/create-eval/SKILL.md) | Bootstrap traces for a new feature, review early runs, and turn supported findings into cases and validated checks. |
| [Run Eval](skills/run-eval/SKILL.md) | Execute the project's eval runner or review stored outputs locally; freeze judgments before comparing expert labels. |
| [Cross-Examine](skills/cross-examine/SKILL.md) | Challenge eval tasks, environments, and graders with a bounded adversarial review. Preserve confirmed flaws and lessons in an evidence ledger. |

Expert Mode lasts for the current session until stopped. Distill Me makes one retrospective pass. Installing or discussing either skill does not activate capture. Expert judgments remain distinct from agent suggestions, uncertainty, preferences, and unreviewed fixes.

## Install

Run from the project where you want the skills. The [Skills CLI](https://github.com/vercel-labs/skills) can install all five for your selected agents:

```bash
npx skills add theclaymethod/cstack \
  --skill expert-mode distill-me create-eval run-eval cross-examine \
  -a codex -a claude-code -a cursor --copy
```

Keep the five folders together so shared record, package, calibration, and export references resolve. Start a new agent session after installation. Codex uses `$expert-mode`, `$distill-me`, `$create-eval`, `$run-eval`, and `$cross-examine`; direct skill installations in Claude Code and Cursor use the corresponding slash commands.

For installation without Node, clone the repo and copy the five skill folders into one agent skill directory. A project-local Codex example is:

```bash
git clone https://github.com/theclaymethod/cstack.git /path/to/cstack
mkdir -p /path/to/project/.agents/skills
cp -R /path/to/cstack/skills/expert-mode \
  /path/to/cstack/skills/distill-me \
  /path/to/cstack/skills/create-eval \
  /path/to/cstack/skills/run-eval \
  /path/to/cstack/skills/cross-examine \
  /path/to/project/.agents/skills/
```

Use `.claude/skills/` for Claude Code or `.cursor/skills/` for Cursor instead. Inspect existing folders before copying so local edits are preserved. Install with one method per agent to avoid duplicate skill discovery.

### Claude Code plugin

This repository also provides a plugin and marketplace manifest:

```text
/plugin marketplace add theclaymethod/cstack
/plugin install cstack@cstack
```

Plugin commands are namespaced, for example `/cstack:create-eval` and `/cstack:run-eval`. The same prefix applies to the other three. See the [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins-reference).

### Cursor plugin

The root `plugin.json` follows the Agent Plugins standard, and `.cursor-plugin/plugin.json` provides Cursor packaging like [Pstack](https://github.com/cursor/plugins/tree/main/pstack). C Stack has not been submitted to the public Cursor marketplace. Use the skills installation above, or import the GitHub repo into a team marketplace using [Cursor's plugin instructions](https://cursor.com/docs/plugins).

## Work locally, export deliberately

The workflow uses local JSONL and Markdown by default. It needs no database, Docker, hosted service, or separate model API. Python supports deterministic eval mechanics, an optional localhost review UI, and the optional export helper. Cross-Examine adds isolation or SQLite only when the task requires it.

Create Eval reuses an existing project harness or defines a [small local package](skills/run-eval/references/package.md). Run Eval uses that harness and the active agent for semantic judging, keeping expert labels out of the supplied judge payload. It distinguishes reviewing old outputs from running the product anew. Both preserve unknowns and execution errors, and keep judge calibration separate from product performance.

Both capture skills support an [eval-author handoff](skills/expert-mode/references/export.md): selected findings, corrections, versioned rubric, replay context, and unresolved gaps. The [Privacy Filter reference](skills/expert-mode/references/privacy-filter.md) explains optional local setup for [OpenAI Privacy Filter](https://huggingface.co/openai/privacy-filter). Keep the original data private, review the exported bundle for remaining identifiers, and check that masking preserves the eval's meaning. Model filtering does not certify anonymization. Nothing uploads or publishes expert data automatically.

## Before production traces

For a new product or a feature without relevant traffic, use [the early-development workflow](skills/create-eval/references/early-development.md): define realistic scenarios from the feature contract, run the actual implementation, inspect the resulting traces with an expert, and promote supported findings into repeatable checks. Synthetic inputs can produce actual execution traces; mocked outputs remain marked as mocked. Keep old regression coverage while testing the new capability.

Put a viewer in place before generating a large batch. Reuse your project's viewer or start the included [local trace reviewer](skills/create-eval/references/trace-review.md):

```bash
python3 /path/to/cstack/skills/create-eval/scripts/review_traces.py \
  eval-runs/feature/traces.jsonl \
  --reviews eval-runs/feature/reviews.jsonl
```

It supports expandable JSON and messages, scoped observations, pass/fail/defer, optional corrections, proposed rubric questions, and an append-only local history. It uses Python 3.10+ and the standard library. It reviews traces; it does not generate product runs, infer expert labels, or serve as a blind judge.

For richer trace analysis, reference [AI Evals Course's Evals Skills](https://github.com/ai-evals-course/evals-skills), especially `generate-synthetic-data`, `error-discovery`, and `build-review-interface`. Its deterministic-check and judge-calibration skills also complement C Stack. See [the routing guide](skills/create-eval/references/ecosystem.md) for links and optional installation. These are external references, not vendored skills or mandatory dependencies. Use the same review workflow when relevant production data arrives, and use synthetic inputs to fill remaining gaps.

## Evals and evidence

The [expert-review suite](evals/expert-review/README.md) contains six synthetic conversation cases and 19 calibration controls. All 19 calibration controls pass. The initial agent pilot passed five of six artifact graders; a focused candidate later passed after a demonstrated grader defect was repaired. These are development results, not held-out performance or proof of domain expertise. See the [report](evals/expert-review/REPORT.md) and [ledger](evals/expert-review/CROSS_EXAMINE_LEDGER.md) for incomplete review coverage and other limits.

```bash
python3 evals/expert-review/calibration.py eval-runs/expert-calibration
```

The [Cross-Examine suite](evals/cross-examine/README.md) includes five audit cases, calibration controls, lesson-transfer exercises, and preserved historical evidence. Its local calibration needs Python 3.11+ with standard-library SQLite serialization support. Local execution shares host permissions; Docker is an optional isolation boundary, not a capture-workflow dependency.

```bash
python3 evals/cross-examine/calibration.py eval-runs/cross-calibration
```

The export helper has been checked locally with synthetic data and a simulated model adapter. Actual Privacy Filter inference and PII-detection performance have not been verified here. The 30 existing calibration controls cover the original suites, not the newly adapted Create Eval and Run Eval skills. Those additions have installation, reference, and local workflow checks; fresh agent behavior remains unverified. The local trace reviewer passed 17 direct HTTP/persistence checks with existing synthetic evidence, plus Python and JavaScript syntax checks. Browser rendering and interaction remain unverified because browser access was disabled in the validation environment. No patient records or real expert-session datasets are bundled. Historical evidence retains its frozen versions and original provenance; old repository names do not change the current installation path.

A [bounded Create Eval cross-examination](evals/create-eval/REPORT.md) completed three lanes and six attempts against v0.3.0 without reproducing a confirmed flaw. It includes actual helper lifecycle probes and narrow agent-authored development artifacts; the verifier lane's checks were specification analysis. This is not an end-to-end skill score. The [ledger](evals/create-eval/CROSS_EXAMINE_LEDGER.md) separates those claims and preserves the remaining validation gaps.

## Credits and license

Created by Clayton Kim. Expert Mode and Distill Me draw on the working-mode and retrospective review patterns in Lauren Tan's [Pstack](https://github.com/cursor/plugins/tree/main/pstack), especially Poteto Mode, Automate Me, and Reflect. Create Eval and Run Eval are portable adaptations of earlier skills in Clayton's repositories; their exact source paths, revisions, and changes are recorded in [SOURCES.md](SOURCES.md). C Stack is a separate package. See [NOTICE](NOTICE) and [LICENSE](LICENSE).
