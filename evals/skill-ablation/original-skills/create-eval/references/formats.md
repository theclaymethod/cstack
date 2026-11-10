# Choose an eval format

Prefer Harbor for new executable agent tasks. Respect an explicit owner choice and an established project format. Existing native runners, DSPy datasets, stored-output review packages and other formats remain supported; format preference does not authorize a migration or a new scoring boundary.

For a new Harbor task, keep agent instructions, environment setup and independent verification separate. The task normally has `task.toml`, `instruction.md`, `environment/` and `tests/test.sh`, with an optional reference solution. The verifier writes its supported reward file under `/logs/verifier/`. Check the project's installed Harbor version and CLI help for the exact schema, environment and reward contract. A matching directory tree is not a successful Harbor run.

Keep source truth, human review material, hidden tests and reference solutions outside the evaluated agent's visible inputs. Validate environment startup/reset, a legitimate result, a valid alternative, an incorrect result, collateral state changes and missing/corrupt evidence through the actual execution path. Distinguish invalid infrastructure from capability failures in the result report.

Use the [stored-output package](../../run-eval/references/package.md) when reviewing retained outputs needs ordinary files rather than an executable environment. Preserve the project's DSPy dataset/metric boundary when optimizing a DSPy program. Record the format and why it fits; retain case authority, lineage, execution evidence and error semantics across formats.

With useful production traces and recoverable project context, consider LangChain's [eval-engineering](https://github.com/langchain-ai/langchain-skills/tree/main/config/skills/eval-engineering). It covers task specs, environments, verifiers and Harbor runs. Read the installed/upstream skill when using that workflow; this is a reference, not a bundled dependency or automatic installation. Its upstream workflow also accepts optional traces; using production traces is C Stack's recommended handoff, not an upstream prerequisite.

Sources: [Harbor task documentation](https://github.com/harbor-framework/docs/blob/main/guides/creating-tasks.mdx), [Harbor task-creation skill](https://github.com/harbor-framework/harbor/blob/main/skills/create-task/SKILL.md). Record the actual versions used; do not infer container isolation or successful execution from these references.
