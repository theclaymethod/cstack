# C Stack

C Stack contains five skills for Claude Code, Codex, Cursor, and other coding agents. They record expert corrections, turn those records into repeatable evals, and check whether the evals measure the intended behavior.

C Stack replaces the standalone [Cross-Examine](https://github.com/theclaymethod/cross-examine) and [Eval Creator](https://github.com/theclaymethod/eval-creator-skill) repositories. Both archives retain their history and link here. [SOURCES.md](SOURCES.md) lists what moved and which project-specific tools remain in the archives.

| Skill | When to use it |
| --- | --- |
| [Expert Mode](skills/expert-mode/SKILL.md) | Invoke `/expert-mode` at session start. The agent keeps replies short and records the expert's explicit judgments, corrections, and yes/no criteria as they work. |
| [Distill Me](skills/distill-me/SKILL.md) | Invoke `/distill-me` to extract expert judgments from the session and merge them with saved records without creating duplicates. |
| [Create Eval](skills/create-eval/SKILL.md) | Write cases and grading criteria from expert findings or traces. Collect and review early runs when a feature has no relevant production traces. |
| [Run Eval](skills/run-eval/SKILL.md) | Run the project's evals or grade saved outputs. Save verdicts before comparing them with expert labels. |
| [Cross-Examine](skills/cross-examine/SKILL.md) | Set a review budget. Have an attacker seek scoring gaps, a defender propose repairs, and an independent reviewer check both against the original intent. Record confirmed flaws and lessons. |

Expert Mode stays active for the session until you stop it. Distill Me reviews the session once. Installing or discussing either skill does not activate capture. The records distinguish expert judgments from agent suggestions, uncertainty, preferences, and fixes the expert has not reviewed.

## Install

Run the [Skills CLI](https://github.com/vercel-labs/skills) in the project where you want the skills:

```bash
npx skills add theclaymethod/cstack \
  --skill expert-mode distill-me create-eval run-eval cross-examine \
  -a codex -a claude-code -a cursor --copy
```

Keep the five skill folders together because they link to each other's references. Start a new agent session after installation. In Codex, invoke `$expert-mode`, `$distill-me`, `$create-eval`, `$run-eval`, or `$cross-examine`. Direct skill installations in Claude Code and Cursor use the corresponding slash commands.

To install without Node, clone the repo and copy the five folders into your agent's skill directory. For a Codex project, run:

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

Use `.claude/skills/` for Claude Code or `.cursor/skills/` for Cursor. Check existing folders before copying to preserve local edits. Use one installation method per agent to avoid duplicate skills.

### Claude Code plugin

To install the Claude Code plugin:

```text
/plugin marketplace add theclaymethod/cstack
/plugin install cstack@cstack
```

All five plugin commands use the `cstack` prefix, such as `/cstack:create-eval` and `/cstack:run-eval`. See the [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins-reference).

### Cursor plugin

The root `plugin.json` follows the Agent Plugins standard. `.cursor-plugin/plugin.json` defines the Cursor plugin, as it does in [Pstack](https://github.com/cursor/plugins/tree/main/pstack). C Stack has not been submitted to the public Cursor marketplace. Install the skills with the commands above, or import the repo into a team marketplace with [Cursor's plugin instructions](https://cursor.com/docs/plugins).

## Local files and exports

The skills save records in local JSONL and Markdown by default. The capture workflow needs no database, Docker, hosted service, or separate model API. Python runs code checks, the optional local trace reviewer, and the export helper. Cross-Examine uses SQLite or an isolated execution environment when the eval task requires it.

Create Eval uses the project's existing eval runner or defines a [small local package](skills/run-eval/references/package.md). Run Eval uses that runner and the active agent to judge criteria that require interpretation. The judge receives case evidence without the expert's calibration labels. Reports distinguish grading saved outputs from running the product again. They include unknowns and execution errors, and report judge agreement separately from product performance.

Expert Mode and Distill Me can [export findings for eval authors](skills/expert-mode/references/export.md). The export contains selected judgments, corrections, rubric versions, the context needed for replay, and unresolved gaps. The [Privacy Filter reference](skills/expert-mode/references/privacy-filter.md) explains how to set up [OpenAI Privacy Filter](https://huggingface.co/openai/privacy-filter) for local use. Keep the originals private. Review the export for remaining identifiers and check that masking preserves the eval's meaning. Model filtering does not certify anonymization. The skills do not upload or publish expert data automatically.

## Before production traces

For a new product or a feature without relevant traces, follow [the early-development workflow](skills/create-eval/references/early-development.md). Define realistic scenarios from the feature's requirements and run the implementation. Review the traces with an expert, then turn supported findings into repeatable checks. Synthetic inputs can produce real execution traces. Mark mocked outputs as mocked. Keep existing regression cases when adding feature coverage.

Inspect a small batch before generating more traces. Use your project's viewer or start the included [local trace reviewer](skills/create-eval/references/trace-review.md):

```bash
python3 /path/to/cstack/skills/create-eval/scripts/review_traces.py \
  eval-runs/feature/traces.jsonl \
  --reviews eval-runs/feature/reviews.jsonl
```

The reviewer displays expandable JSON and messages. An expert can record an observation about a specific part of an output, pass or fail it, defer judgment, add a correction, or propose rubric questions. Edits append to the local review history. The tool uses Python 3.10+ and the standard library. It displays all supplied trace fields, so it is not a blind judge. It does not run the product or infer expert labels.

Use [AI Evals Course's Evals Skills](https://github.com/ai-evals-course/evals-skills) for synthetic input generation, error analysis, and custom review interfaces. Start with `generate-synthetic-data`, `error-discovery`, or `build-review-interface`. The collection also has skills for code checks and judge calibration. [The reference guide](skills/create-eval/references/ecosystem.md) links to them and gives optional install commands. C Stack does not bundle or require these skills. Review production traces with the same workflow when they become available. Use synthetic inputs for cases the traces do not cover.

## Evals and limits

The [expert-review suite](evals/expert-review/README.md) has six synthetic conversation cases and 19 calibration controls. All 19 controls passed. The initial agent pilot passed five of six artifact graders. A focused rerun later passed after a reproduced grader defect was fixed. These development results do not establish performance on unseen cases or domain expertise. The [report](evals/expert-review/REPORT.md) and [ledger](evals/expert-review/CROSS_EXAMINE_LEDGER.md) describe the incomplete review coverage and other limits.

```bash
python3 evals/expert-review/calibration.py eval-runs/expert-calibration
```

The [Cross-Examine suite](evals/cross-examine/README.md) has five audit cases, 11 calibration controls, and exercises that check whether a generator applies a learned lesson to a related task. All 11 controls passed. Local calibration needs Python 3.11+ with standard-library SQLite serialization support. Local execution uses the host user's permissions. Docker is optional for isolated execution. The capture skills do not require it.

The [workflow chart and model checks](evals/cross-examine/workflow/README.md) describe the attacker, defender, and independent intent reviewer. Five weakened model configurations produced counterexamples when safeguards for independent judgment, observed replay, valid alternatives, or original intent were removed. The model checks do not prove that agents follow the playbook.

```bash
python3 evals/cross-examine/calibration.py eval-runs/cross-calibration
```

These 30 controls check the original suites' grading machinery. They do not evaluate Create Eval or Run Eval. Installation, reference, and local workflow checks passed for both skills. Fresh end-to-end agent behavior remains unverified.

| Component | Recorded checks | Limits |
| --- | --- | --- |
| Create Eval | A [Create Eval review](evals/create-eval/REPORT.md) covered three review areas and six attempts against v0.3.0 without reproducing a confirmed flaw. It checked trace changes, review amendments, and restarts, and included agent-authored development examples. | The verifier review analyzed the specification. These checks do not establish end-to-end skill performance. The [ledger](evals/create-eval/CROSS_EXAMINE_LEDGER.md) records the remaining gaps. |
| Local trace reviewer | Seventeen HTTP and persistence checks passed with synthetic data. Python and JavaScript syntax checks passed. | Browser access was disabled during validation, so rendering and browser interaction remain unverified. |
| Export helper | Local checks used synthetic data and a simulated model adapter. | Actual Privacy Filter inference and PII-detection performance remain unverified. |

The repo contains no patient records or real expert-session datasets. Historical evidence keeps its original versions, source records, and repository names. Use the installation commands above for the current pack.

## Credits and license

Clayton Kim created C Stack. Expert Mode and Distill Me use patterns from Lauren Tan's [Pstack](https://github.com/cursor/plugins/tree/main/pstack), especially Poteto Mode, Automate Me, and Reflect. Create Eval and Run Eval adapt earlier skills in Clayton's repositories. [SOURCES.md](SOURCES.md) records their source paths, revisions, and changes. C Stack is a separate package. See [NOTICE](NOTICE) and [LICENSE](LICENSE).
