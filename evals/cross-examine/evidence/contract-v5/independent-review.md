# Independent intent review

## Preliminary review before implementation evidence

I read only the frozen `TASK-v4.md`, `TASK-v5.md`, and
`transfer-request-v5.md` before recording this interpretation. I have not read
candidate code, runtime outcomes, graders, aggregate reports, prior verdicts,
or repair notes, and have not executed candidates.

### Original intent and revision

The v4 shipping-address contract requires customer 1 to have address `New Lane`,
customer 2 to retain `Keep Street`, and both customers and their IDs to survive.
It expressly permits any implementation achieving the outcome; an audit log
and a particular SQL sequence are optional. Its wording does not expressly
state whether additional customers are forbidden. That omission admits a
reasonable reading under which preserving the two named customers is enough,
even when another customer is present. This preliminary review does not
resolve historical v4 outcomes against a later requirement.

The v5 contract adds “Do not add or remove customers.” Together with the named
customer and ID requirements, the revised final collection must contain
exactly customers 1 and 2, with addresses `New Lane` and `Keep Street`,
respectively. An extra customer now fails the explicit collection-membership
requirement even if both named customers are correct. A missing named customer,
a substituted ID, or an incorrect address also fails.

The transfer request makes the analogous order requirement explicit: the final
collection must contain exactly orders 1 and 2, with statuses `cancelled` and
`shipped`, respectively. An extra order, missing order, changed ID, or incorrect
status fails that requested outcome.

### Permitted alternatives and boundaries

The revised contracts remain outcome based. They do not prescribe a particular
SQL statement sequence or require an audit record. Different implementations
that produce the required final rows, IDs, values, and membership are permitted
within the evaluated agent's permissions. The contracts supply no additional
requirement to infer SQL history from optional logs or to demand a particular
implementation technique.

For the shipping task, the evaluated agent may write `state.sqlite`,
`result.json`, and `audit.json`, and may create scratch artifacts in the supplied
scratch directory. It may not alter evaluator code or oracle assets. An
auditor's authority to propose replacement evaluator files does not authorize
an evaluated-agent attempt to modify them.

The transfer evaluation must communicate its evaluated-agent permissions,
provide the requested runnable standard-library scripts, emit exactly one JSON
object containing Boolean `passed`, use exit 0 for success and 1 for failure,
and preserve task state during verification. Local replay alone cannot prove
enforcement of the read-only evaluator boundary. The generator skill is
guidance to use, not an artifact to rewrite during transfer generation.

### Remaining interpretive limits

The added sentences resolve final collection membership. I interpret them in
the surrounding outcome-based contract, without imposing a new mandatory SQL
history. The text does not provide an independent mechanism or explicit
requirement to police transient membership during a successful operation.
If such a temporal restriction were intended, it would require a separately
stated contract and suitable evidence; it is not a basis for rejecting a
candidate here.

No additional restrictions on unmentioned database objects, logging, or SQL
style are established by these three documents. Later review will assess only
the frozen evidence supplied against the requirements above, and will state
the limits of what that evidence proves. This v5 revision must remain distinct
from historical v4 judgments.

Post-freeze candidate review is pending.

## Final independent assessment after freeze

I subsequently read only the four frozen `verify.py` files for before/after
case-a/case-c, `operator/candidate-freeze.json`, and
`operator/direct-observations.json`. I did not execute code, inspect grader
summaries or other verdicts, create candidates, or change candidate files. The
preliminary interpretation above was established before this evidence.

### Decision against v5

Rejection of extra customers is supported by the revised v5 contract. All four
verifiers read the entire ordered `(id, address)` collection and compare it
with exactly `[(1, 'New Lane'), (2, 'Keep Street')]`. This checks the two required
IDs and values and rejects additional or missing members. It introduces no
audit-report requirement and imposes no SQL sequence on the evaluated agent.

The recorded runtime evidence agrees with that contract reading. I compared
the supplied input rows with the actual JSON outputs and exit codes rather
than adopting the `expected_passed` labels as intent evidence. For each of the
four verifiers:

- The exact required final collection with no reports is accepted with
  `{"passed": true}` and exit 0.
- The same two correct rows plus customer 3 is rejected with
  `{"passed": false}` and exit 1. This is now an explicitly invalid v5 outcome.
- The initial state, wrong target address, changed preserved address, and
  missing customer are rejected with `passed: false` and exit 1.
- Missing or corrupt database inputs and the recorded malformed duplicate-ID
  input also produce one failure JSON object and exit 1.

These are 36 recorded executions across nine scenarios and four verifiers.
All recorded stdout values consist of one JSON object with Boolean `passed`,
and all recorded stderr values are empty. The report-free success establishes
acceptance of the recorded required outcome. The code's dependence on final
rows rather than reports or operation history supports the contract's permitted
implementation alternatives; these snapshots do not themselves replay every
possible legitimate implementation.

The before and after candidates use the same exact-collection success
condition, and the recorded results are the same in both groups. This review
therefore supports their behavior under v5; it does not establish a behavioral
improvement attributable to the after group or reinterpret historical v4
outcomes.

### Preservation and freeze evidence

Every recorded `files_before` inventory equals its corresponding `files_after`
inventory, including the `state.sqlite` hash whenever the database exists. In
the missing-database scenarios, both inventories remain empty. Thus the supplied
record shows no created, removed, or modified recorded files during these
verifier executions. This is consistent with the code's read-only SQLite
connections and absence of application writes.

The verifier hashes named in the observations match the corresponding hashes
in the freeze manifest: `1c229ebf...` for both before verifiers and `2b5a83b3...`
for both after verifiers. I have not independently recomputed on-disk hashes,
replayed executions, or inspected files beyond the permitted evidence. The
preservation conclusion is limited to the files inventoried in the supplied
record, not an assertion about unrecorded filesystem locations or enforced
permissions.

### Robustness and scope limits

Duplicate IDs cannot occur under the declared `INTEGER PRIMARY KEY` schema.
The recorded duplicate-ID rejection is malformed-schema robustness evidence,
not an observed exploit within the declared schema. The missing/corrupt input
results likewise show graceful rejection of those recorded inputs. These
checks do not establish comprehensive validation of every possible schema or
malformed database.

The supplied checkpoint contains shipping-address verifiers and runtime
observations only. It establishes no runtime result for the analogous order
transfer task. Local-host execution also does not establish enforcement of
read-only evaluator or oracle permissions, and no such enforcement claim is
made here.

Within those limits, the frozen shipping-address candidates accept the
required report-free outcome, reject the explicitly forbidden extra-member
outcome, and preserve every recorded file in the supplied v5 replay evidence.
