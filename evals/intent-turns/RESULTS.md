# Development replay

One low-reasoning gpt-6.2-sol trial per selected scenario and revision. The product received the skill and one owner turn at a time. It could inspect installed skills and the fixture project. During the authorized edit it also consulted the installed writing-for-agents skill. The operator supplied synthetic replies. The same agent that authored the fixtures reviewed the outputs. No owner labels, blinded judge or independent final set were used.

| Check | First run | After revision |
| --- | --- | --- |
| Bootstrap, forward | Asked the distinguishing question, stopped for the readback, then requested scenario approval. | Repeated that order and wrote a proposed scenario index with both deferred decisions. |
| Understando, forward | Summarized the rule at turn 2 and omitted the confirmation question. Its final suite looked correct. | Asked for confirmation at turn 2, then sought approval at turn 3. |
| Understando, backward | Credited B4 and kept train changes deferred. Several points appeared in paragraphs. | Started with a correctable reading and used bullets for the evidence on the opening turn. The follow-up still put several points in prose. |
| Understando, thread drift | Called the replacement a violation before the owner had confirmed the reading. It did wait for permission before editing. | Read the owner’s intent back first. After confirmation, it located the first divergence, proposed a scoped rule, and waited for edit approval. The expected skill changed only at the authorized turn. |
| Understando, change of mind | Credited the action that matched the earlier instruction. No skill edit. | Correctly found a change of mind and made no skill edit. It did overstate a detail: the owner confirmed restoring the number, but never explicitly decided whether the link must also disappear. |

**Communication remains mixed.** The final forward readbacks are scannable. Some backward-review replies still bury several facts in prose. The grader treats that as a presentation miss even when the product judgment is sound. The generic help skill recommended Bootstrap in a direct opening sentence in a separate empty-workspace smoke test. That smoke does not validate the other CStack skills.

**Read the evidence.** [Final replies and observed file changes](sample.jsonl) contains the 13 final turns, with temporary project prefixes removed from links. Only Bootstrap and Understando went through the multi-turn suite. The state tests check net file changes. They do not establish semantic agreement or guarantee future behavior. See [the scoring instructions](SCORING.md) for controls and calibration.

On the rubric for the 13 final turns, the operator marked 12 passing for intent and order, and 10 passing for communication. All 13 passed the file-state checks. The communication misses were the seat follow-up and two thread diagnoses that packed multiple findings into the same paragraph or bullet. These counts describe five conversations across four synthetic case families.
