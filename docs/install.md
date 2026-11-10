# Install C Stack


Run the [Skills CLI](https://github.com/vercel-labs/skills) in the project where you want the skills:

```bash
npx skills add theclaymethod/cstack \
  --skill expert-mode distill-me bootstrap create-eval run-eval cross-examine hill-climb adversarial-cases calibrate-judge ablation bitter-lesson \
  -a codex -a claude-code -a cursor --copy
```

Keep the eleven skill folders together because they link to each other's references. Start a new agent session after installation. In Codex, invoke `$expert-mode`, `$distill-me`, `$bootstrap`, `$create-eval`, `$run-eval`, `$cross-examine`, `$hill-climb`, `$adversarial-cases`, `$calibrate-judge`, `$ablation`, or `$bitter-lesson`. Direct skill installations in Claude Code and Cursor use the corresponding slash commands.

To install without Node, clone the repo and copy the eleven folders into your agent's skill directory. For a Codex project, run:

```bash
git clone https://github.com/theclaymethod/cstack.git /path/to/cstack
mkdir -p /path/to/project/.agents/skills
cp -R /path/to/cstack/skills/expert-mode \
  /path/to/cstack/skills/distill-me \
  /path/to/cstack/skills/bootstrap \
  /path/to/cstack/skills/create-eval \
  /path/to/cstack/skills/run-eval \
  /path/to/cstack/skills/cross-examine \
  /path/to/cstack/skills/hill-climb \
  /path/to/cstack/skills/adversarial-cases \
  /path/to/cstack/skills/calibrate-judge \
  /path/to/cstack/skills/ablation \
  /path/to/cstack/skills/bitter-lesson \
  /path/to/project/.agents/skills/
```

Use `.claude/skills/` for Claude Code or `.cursor/skills/` for Cursor. Check existing folders before copying to preserve local edits. Use one installation method per agent to avoid duplicate skills.

### Claude Code plugin

To install the Claude Code plugin:

```text
/plugin marketplace add theclaymethod/cstack
/plugin install cstack@cstack
```

All eleven plugin commands use the `cstack` prefix, such as `/cstack:create-eval` and `/cstack:run-eval`. See the [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins-reference).

### Cursor plugin

The root `plugin.json` follows the Agent Plugins standard. `.cursor-plugin/plugin.json` defines the Cursor plugin, as it does in [Pstack](https://github.com/cursor/plugins/tree/main/pstack). C Stack has not been submitted to the public Cursor marketplace. Install the skills with the commands above, or import the repo into a team marketplace with [Cursor's plugin instructions](https://cursor.com/docs/plugins).
