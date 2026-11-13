# Reuse existing eval skills

[AI Evals Course's Evals Skills](https://github.com/ai-evals-course/evals-skills) supplies established workflows for learning from model traces. Reference these for both production traces and locally generated development traces. cstack adds session capture, a small local handoff, early-feature execution guidance, and Cross-Examine; it does not replace their error-analysis methodology.

| Need | Upstream skill |
| --- | --- |
| Find failure modes in traces with expert review | [error-discovery](https://github.com/ai-evals-course/evals-skills/tree/main/skills/error-discovery) |
| Build a review UI suited to graphs, conversations, documents, or other artifacts | [build-review-interface](https://github.com/ai-evals-course/evals-skills/tree/main/skills/build-review-interface) |
| Bootstrap realistic inputs or fill a coverage gap | [generate-synthetic-data](https://github.com/ai-evals-course/evals-skills/tree/main/skills/generate-synthetic-data) |
| Implement an objective failure check | [write-code-eval](https://github.com/ai-evals-course/evals-skills/tree/main/skills/write-code-eval) |
| Turn an interpretive failure rule into a judge prompt | [write-judge-prompt](https://github.com/ai-evals-course/evals-skills/tree/main/skills/write-judge-prompt) |
| Compare a judge with human labels | [validate-evaluator](https://github.com/ai-evals-course/evals-skills/tree/main/skills/validate-evaluator) |
| Inspect an existing eval pipeline | [eval-audit](https://github.com/ai-evals-course/evals-skills/tree/main/skills/eval-audit) |
| Separate retrieval from generation failures | [evaluate-rag](https://github.com/ai-evals-course/evals-skills/tree/main/skills/evaluate-rag) |

Load the installed matching skill when available. Do not install the entire pack or execute another workflow merely because it is linked here. Optional installation of the first three:

```bash
npx skills add ai-evals-course/evals-skills \
  --skill error-discovery build-review-interface generate-synthetic-data \
  -a codex -a claude-code -a cursor --copy
```

Follow project constraints when applying upstream advice. Batch sizes are heuristics, not prerequisites. Match sampling to the decision: diverse discovery samples reveal categories; representative samples support frequency estimates. A new feature can have no relevant traces even when the product has abundant historical traffic. No fixed trace count establishes coverage.

Keep initial discovery open-ended. Introduce binary criteria after the requirement or failure boundary is understood. Do not require an observed failure before checking an explicit schema or safety invariant. Domain-specific synthetic inputs need someone able to assess realism; generated clinical facts or labels are not expert authority. Reuse existing viewers and runners, and avoid unnecessary clustering, databases, hosted tracing, dependencies, or new test files.

Inspected upstream revision: `80d5f7b0127c7572ed9e9339937adbfd7240ffeb`. Links above follow upstream for discovery; record the actual revision when applying its workflow.

## Production-trace task engineering

With recoverable production traces and repository context, use LangChain's [eval-engineering](https://github.com/langchain-ai/langchain-skills/tree/main/config/skills/eval-engineering) for reviewed task specs, controlled environments, independent verifiers and Harbor runs. It also supports optional traces; this is cstack's recommended production handoff. Read the actual installed/upstream workflow when applying it. Do not vendor or install it merely because it is referenced.
