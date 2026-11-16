# Discover a rule that existing evidence cannot distinguish

The earlier handoff eval supplies the correction. This exercise withholds the pivotal decision. Use the same opening for both owner policies. Grade the first question before selecting a reply. Run with Bootstrap to evaluate a forward scenario index, or Understando to evaluate session reconstruction and proof coverage.

Opening: “When someone shares a collection link, visitors should see its cover. QA shared a collection with a fox cover and immediately opened the link in a fresh browser. The visitor saw the fox. The designer says either a cropped or a full-size image is fine. What happens if a cover is deleted is a decision for later. Help me pin down the remaining behavior.”

Give the interviewer one question. Record whether it describes the owner replacing the cover after sharing and before opening the existing link, or asks an equivalent question distinguishing share-time and view-time identity. A general invitation to list edge cases, repeating the deleted-cover question or asking about dimensions does not qualify. Record the number of independent questions and any expectations asserted before the answer. A discriminating question bundled with five other questions earns discovery credit but fails interview efficiency.

Fork the exact same first response into two continuations. For a qualifying question, the first owner wants the earlier cover and the second owner wants the replacement. Give no policy hint when the question misses. Request the finished artifact. Grade the artifacts side by side:

1. Each confirmed expectation and proposed check for the distinguishing case follows that owner’s answer. The two artifacts must give opposite results for the same sequence.
2. Both preserve the unchanged-cover observation and allow both approved renderings. Deleted covers remain open and outside scored outcomes.
3. For Understando, distinguish what QA actually observed from the missing after-replacement run. Neither branch may claim implementation, execution or owner approval beyond the given evidence.
4. For Bootstrap, the final index supplies stable scenario IDs, starting conditions and observable outcomes. Alternative grouping and wording are acceptable.

A lucky guess on a single branch cannot establish discovery. A miss stays a miss even if the final artifact happens to predict one owner’s choice. This case measures question selection with one synthetic family. It does not measure autonomous tool routing or implementation quality.

## Replay

Run one arm at a time with the installed Codex CLI. Replace the skill path with Understando’s SKILL.md and omit the Bootstrap reference for a standalone Understando run. Use the corresponding revision’s files for baseline arms. The model receives the instructions, not this operator rubric. It returns Markdown to the harness.

```sh
python3 evals/spec-discovery/replay.py /tmp/discovery-arm ask skills/bootstrap/SKILL.md --reference skills/bootstrap/references/discovery-prompts.md
cat /tmp/discovery-arm/question.md
python3 evals/spec-discovery/replay.py /tmp/discovery-arm finish qualified
python3 evals/spec-discovery/replay.py /tmp/discovery-arm settled
```

Use `finish missed` if the first question fails the disclosure rule. Each finish call runs two fresh contexts from the saved identical prefix and question. The settled control starts from the opening and additionally provides both the owner’s replacement decision and QA’s direct observation. Grade whether the interviewer can finish without reopening the decision. Distinguish missing coverage from missing intent.

## Observations

[Full questions, both continuations and settled controls](transcripts.json). Old Bootstrap came from a3d940a, old Understando from 1fcde47. Each arm ran one opening, two continuations and a separate settled control, using gpt-6-astra. The one-question budget was explicit. The Bootstrap candidate received the prompt card inline, so this comparison does not measure whether it retrieves the card autonomously.

| Skill | One distinguishing question | Both branch artifacts | Already settled |
| --- | --- | --- | --- |
| Bootstrap, previous | Yes | Correct | Asked whether an existing link must show the replacement in a previously used browser. That is an untested condition, but the owner had already settled image identity for existing links. |
| Bootstrap, revised | Yes | Correct | Finished with both observations and deletion deferred. |
| Understando, previous | Yes | Correct | Finished. Proposed same-browser coverage as an inference without asking for another decision. |
| Understando, revised | Yes | Correct | Finished. Distinguished the observed image identity from the unobserved rendering variants. |

Both answers to the same question changed only the replacement expectation in substance. Both Understando versions marked the replacement check as proposed until QA actually exercised it. No version invented a deletion policy. The observed Bootstrap difference is one saved question on one exposed family. Understando shows preserved discovery on this case, not a measured speedup.

## Guardrail and novelty scenarios

Give the interviewer a checkout entrypoint, its enforced amount limit, the product promise that total equals quantity times unit price, and existing quantity-one evals. A reviewer suggests checking arithmetic above the limit. In the first scenario the oversized purchase is rejected before calculation. Grade whether the interviewer inspects that path and moves on with zero new product evals and zero owner questions about the rejected amount. In the second, a supported purchase of three two-dollar items yields two dollars and passes the current evaluator. Grade whether the interviewer identifies that distinct failure, proposes the six-dollar check, and still omits the unreachable case. These are scenario specifications awaiting a behavioral replay.
