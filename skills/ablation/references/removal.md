# Choosing and interpreting removals

Use this reference for unit selection, structural dependencies, interactions and minimality claims.

## Units and intervention

Choose meaningful atoms: a prompt section, demonstration, context source, tool definition, retrieval stage, reflection pass, or optional program branch. Preserve an exact map from unit IDs to content or execution changes. Count rendered input after assembly, not only the edited template. Whole blocks are often easier to interpret than token deletion.

Record dependencies and protected meaning. Removing a parent with a surviving dependent can be structurally invalid. Either reject that candidate before a call or explicitly remove the dependency closure as one group. A schema or business rule can be expressed more compactly only in a separately identified rewrite experiment; deleting its only expression changes the task.

Literal deletion, masking, disabled execution, summarization and replacement have different effects. For example, removing a retrieved chunk changes information; skipping retrieval also changes tool calls and latency. Keep those interventions distinguishable. [Removal-based explanation framework](https://www.jmlr.org/papers/v22/20-1316.html), [LLMLingua compression method](https://aclanthology.org/2023.emnlp-main.825/).

## Search and interactions

A practical bounded search can try coarse groups, leave-one-out diagnostics, sequential accepted deletions and selected pairs/groups. Delta debugging tests subsets and complements against a chosen predicate. Hierarchical reduction uses structure, but later changes can enable earlier deletions, so revisit survivors if the budget permits. These are methods to adapt, not mandatory dependencies. [Original ddmin paper](https://www.st.cs.uni-saarland.de/publications/files/zeller-tse-2002.pdf), [Original HDD paper](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/hdd.pdf).

Two examples explain why single-unit diagnostics are insufficient:

- Duplicate reminders A and B may each be removable while their joint deletion fails.
- Conflicting groups A and B may each resist single removal while removing both works.

These are illustrative possibilities. Test actual combined artifacts and retain their identities. A component's measured effect is conditional on the model, other components, inputs and protocol. Retained sufficiency is different from universal necessity. [Sufficient Input Subsets](https://proceedings.mlr.press/v89/carter19a/carter19a.pdf), [ERASER sufficiency and comprehensiveness](https://aclanthology.org/2020.acl-main.408.pdf).

## Claims and deliverables

Report the selected unit set and rendered artifact; baseline-relative quality and per-case changes; measured burden; each tested combination; invalid/incomplete attempts; and unexplored interactions.

The deterministic ddmin guarantee is 1-minimality under its oracle, not global minimum size. A search using noisy estimates does not inherit that guarantee. An ordinary hierarchical pass can leave newly removable items behind. Name any completed sweep and its granularity; otherwise report the smallest confirmed candidate found within the declared search and budget.
