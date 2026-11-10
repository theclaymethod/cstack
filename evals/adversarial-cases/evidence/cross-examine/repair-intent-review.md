# Independent repair intent review

## Decision

**Accept the frozen core repair for the two narrow confirmed issues: native ticket-metadata false rejection, and incomplete/incoherent evidence acceptance in the fixed adversarial replay.** The original shared-skill intent and supported alternatives are preserved. I found no confirmed remaining defect within these reproductions. This decision covers the five files pinned by repair-core-sha256.json; the additional portable harness and final documentation were still being packaged and are outside this checkpoint.

I reread ORIGINAL-CONTRACT.md and used my pre-scoring intent baseline and independently inspected raw reproductions. I inspected the frozen-to-repaired code/guidance diff, the new native regression test, raw repaired replay evidence, original semantic contrast, original corrupted-evidence copies, and attack-execution source/raw lifecycle observations. I did not read attack-execution/findings.md or other reviewer verdicts. All five pinned file hashes match. The repaired spec, rubric and original cases are byte-identical to their frozen versions.

No extra candidate executions or interruptions were performed for this review. Independent verification imported the existing native/replay functions under Python -B and read/regraded retained evidence. Source files were not edited. The root identified the native evaluator repair as separately authorized under the user's instruction to fix confirmed issues and requiring a new native baseline; this review accepts it on that basis, not as an unannounced change during the original frozen campaign.

## Native metadata repair

The evaluator changes only valid_ticket: the four required fields must exist and retain their nonempty string types; the complete key set need not equal those four fields. This removes the extra restriction absent from the written ticket contract. Exact outer output fields, unique IDs, required new-ticket account/status/issue, appended count, and preservation checks remain intact. Existing metadata is retained and compared as part of original ticket state rather than ignored.

I independently regraded the original minimal four-fields/five-fields outputs against the same original case using repaired grade. Both PASS with all nine behavioral checks true; the original native result was PASS versus schema ERROR. Regrading the larger semantic trace set changes only extra-ticket-metadata from ERROR to PASS: alternative ID/note/key-order and legitimate noncreation controls remain PASS, while duplicate ID, state type flip, false creation, wrong account/status/issue and original-ticket order violation remain FAIL. The deliberately stale expectation case remains a deliberately mislabeled operator control, not a source-label defect or a requirement to add natural-language judging to native grade.

I also independently formed a subsequent noncreation case from the metadata-bearing returned state: preserving it passes; changing created_at fails preserved_tickets. These direct computations execute no candidates. The new regression test exercises native run_suite creation, a subsequent native run retaining existing metadata, and rejection of a later metadata mutation. metadata-regression-before.json records the new test failing against the original validator with three ERRORs, consistent with the confirmed cause. Root reports 23 native tests passing on the repaired baseline; the final all-controls logs were not yet part of this checkpoint, so this review's independent evidence is the raw-output regrading and preserved metadata checks rather than an assertion that I reran those tests.

The source rule “preserve original tickets and all other supplied state exactly” remains unchanged. Permitting metadata on a new ticket does not permit mutation of metadata on an existing ticket. The evaluator hash changes, so retained native runs requiring the old grading identity are not silently reused as a current repaired baseline.

## Replay evidence repair

The repaired replay establishes the exact fixed source inventory, compares it with current supplied files, requires one command record per fixed command identity and a matching standalone receipt, validates retained native runs through native checked_run, and requires every fixed lifecycle observation exactly once. These target the confirmed failures directly. They do not make replay a general semantic grader of the shared skill or a security boundary against an operator rewriting the host.

I independently invoked repaired replay.validate on the original operator calibration copies, explicitly providing their original pristine workspace so each is assessed against the correct source version:

| Original evidence copy | Repaired outcome |
| --- | --- |
| clean-copy | Accepts, 103 checks |
| stdout-output-conflict | Rejects: retained output differs from subprocess stdout |
| matched-false-source-inventory | Rejects: complete expected protected source inventory absent |
| missing-one-lifecycle-observation | Rejects: required lifecycle observation membership incomplete |
| empty-lifecycle-observations | Rejects: required lifecycle observation membership incomplete |
| omitted-command-receipt | Rejects: required command receipt inventory incomplete |

I independently reran read-only validation of repaired-replay/workspace/eval-runs/case-build against its actual repaired workspace: 103 checks accepted. Its raw counts retain 38 native case executions and three owned-process interruptions, plus 40 reserved case runs and the early-stop reservation left pending. The repaired validation retains native rejection of false creation claims, legitimate candidate/ID/note controls, successful completed-evidence recovery, noactivation, and incomplete-evidence controls. The result still explicitly claims only replay of constructed synthetic development controls.

The guidance additions point case builders toward the project's evidence checker, frozen expected coverage identities, meaningful source inventories, representation alternatives and later metadata preservation. They preserve the original permissions and honest-outcome distinctions. Requiring these evidence checks applies to executed handoffs; it does not turn contract-only proposed scenarios into failed executions or require a source-skill invocation to manufacture a defect.

## Independent lifecycle attack scope

I inspected attack-execution's inject.py and reproduction/finalization logic, observations.json and raw lifecycle observation/state files, actual activation events, process receipts and native retained runs. Its source-pinned trace hook executes the real frozen evaluate.py, records a boundary event, and sends SIGKILL to that same owned process. Each of the four activated event PIDs matches its independent process receipt PID, and each receipt reports -9. No operator action is relabeled as candidate access.

The four interrupted boundaries support these narrow results:

| Boundary | Actual retained execution | Observed recovery |
| --- | --- | --- |
| Before third case, after two durable trace rows | Two case results; incomplete summary absent | Remains pending, best null, eight reservations charged |
| Published complete baseline summary before durable campaign completion | Eight complete native results | Recovers complete baseline/best 0, charge remains eight |
| complete_attempt returned in memory before durable save | Eight complete native results | Recovers complete baseline/best 0, charge remains eight |
| Proposal decision returned before durable save | Eight baseline plus eight proposal results | Recovers proposal decision/best 1, charge remains sixteen |

The uninstrumented clean and armed attempt-999 unreachable controls complete normally. The unreachable activation log is absent and activation count zero; its outputs exactly match the clean control. Published-summary and memory-boundary outputs also match clean. Repeated status preserves state and all recorded files; pre/post non-state evidence hashes remain unchanged. Native checked_run independently accepts every complete retained lifecycle run and rejects the two-row partial run because summary.json is absent. This is correct incomplete-evidence handling, not a discovered lifecycle failure.

I independently enumerated all raw native trace rows in the execution attack: 76 total, including 50 lifecycle, 26 custom/reduction cases, and two preserved reset-probe setup-error cases. Four -9 interruption receipts exhaust that attack's four-stop budget. Its protected before/after inventories agree and match current supplied source. The original malformed-output, crash and reset import-order errors remain visible; the corrected reset probe is identified separately. The convenience replay_private.py wrapper explicitly remains unexecuted and would consume a fresh budget; I did not run it.

Adjudication: **bounded no demonstrated lifecycle defect**, supported by these actual phases and controls. This does not establish power-loss durability, external dependency retry behavior, confirmation/finish interruption recovery, arbitrary host isolation, or repeated/stochastic recovery quality. The shared skill and original request expressly permit this result; the lifecycle evidence must not be inflated into a new finding to accompany the actual native/evidence-validator repairs.

## Remaining claim boundaries

All accepted evidence is exposed synthetic local development work. No human expectation approval, model-effectiveness comparison, held-out generalization, production reliability or containment result follows. Operator evidence-calibration findings remain operator-only; known supplied proxy flaws remain teaching controls; native metadata and replay consistency are distinct repaired layers. Bootstrap intent approval and Cross-Examine independent adjudication remain parent responsibilities. Final packaged harness portability, completed all-controls logs, and final delivery contents require their own verification and are not implied by this core acceptance.

## Final integration acceptance

**Accept the portable audit harness and wrapper integration.** I inspected repaired/evals/adversarial-cases/cross_examine.py, the updated all/named suite wrapper, the ledger, packaged source snapshots and minimal contrast, and retained audit-repair-replay raw results. No further native runs were launched. The five core pinned hashes remain unchanged.

The harness resolves its source/evidence from its own location, creates a fresh output workspace, executes the real current construction replay, runs the same one-case four/five-field contrast against separately identified original/repaired evaluator versions, and applies the five operator evidence mutations to separate copied artifacts. Packaged original-replay.py and original-evaluate.py are byte-identical to their frozen sources; both portable candidates and their case are byte-identical to the independently reviewed minimal contrast. I independently counted 42 actual trace rows in the retained portable audit's real construction/contrast runs and three -9 owned-process receipts; copied probe artifacts are not double-counted as new execution. All four raw contrast stdout/output pairs agree, with original five-fields ERROR and the other three PASS. Mutation results reproduce the original-validator acceptance and repaired rejection described above.

The wrapper exposes adversarial-audit both as a named suite and in all, records commands/cwd/exits and bounded timeouts, and keeps its output paths fresh. The ledger accurately separates AC-01 native task rejection from AC-02 operator-only evidence calibration, preserves the known defective teaching proxy's scope, distinguishes assertion/case counts, records independent original/repair checkpoints, and retains bounded lifecycle no-defect results. It does not imply model or production reliability. The only missing ledger link at inspection was CROSS_EXAMINE_REPORT.md, which the root explicitly identified as still being assembled; final delivery should include that report. This is a packaging completion item rather than a functional/scoping defect in the frozen harness.

The all-controls run completed during this review. I inspected its actual summary: all eight suites have exit 0 and passed status—expert-review, cross-examine, bootstrap, bootstrap-audit, hill-climb-audit, adversarial-cases, adversarial-audit, and playground. The native stderr log records 23 tests run and OK. The new all-controls adversarial-cases result retains 38 actual cases/three interruptions; adversarial-audit records 42/three and passed. These are additional completed operator control runs, not repeated by this reviewer and not charged to either attacker's separate budget. Acceptance now includes this completed integration evidence; original claim limits remain in force.
