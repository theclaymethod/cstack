# Verifier lane: no confirmed bypass in two attempts

Original: C Stack v0.3.0, revision `a7fc7cf2cc2716e474143b7e85bfbda6d1ef2d62`. Frozen Create Eval/Run Eval guidance was reviewed. The relevant source/evidence hashes are in `observations.json`.

Both attempted shortcuts are explicitly excluded by the frozen instructions. No full-skill authoring agent, semantic judge, package runner, comparison harness, or product feature was executed. The actual executable paths were Python standard-library JSON parsing and arithmetic. Therefore this receipt does **not** establish that an automated grader rejected either attack, and it does not establish behavioral robustness of Create Eval. No new specification ambiguity was confirmed.

## V1: widen a scoped source failure into numerical gold

Attempt: use the synthetic finding's missing-source negative as calibration gold for probability correctness, or for an aggregate containing both source naming and probability correctness.

Actual observation: the source-naming answer is `no`, with a current passing answer of `yes`; the probability judgment remains `uncertain`. The negative finding has no replacement correction. Its capture is marked ready, but this export's replay readiness is false. This separates a potentially useful scoped negative from an unsupported numerical claim and from replay readiness.

Independent true outcome: a source-naming FAIL is supported for that scoped assertion. Numerical correctness remains unknown; the missing-source label cannot settle it. The export does not independently establish sufficient replay context. A missing replacement probability alone is not a reason to discard the scoped source negative.

Baseline: retain the current criterion-0002 version-2 scope and FAIL, preserve the numerical uncertainty, and leave replay readiness unresolved. The local calculation recovered that scoped FAIL from the captured answer and passing direction; it did not newly grade the original output.

The shortcut fails at the specification level: [package.md:57](https://github.com/theclaymethod/cstack/blob/a7fc7cf2cc2716e474143b7e85bfbda6d1ef2d62/skills/run-eval/references/package.md) requires gold to cover precisely the aggregated checks, and line 59 keeps uncertain/incomplete cases separate. Create Eval and From Findings also explicitly preserve assertion scope and supported negatives without replacement answers. An author who widens this label would violate the instructions; this lane did not observe such an author.

Minimal reproduction (read-only; source fact extraction and passing-direction calculation):

```sh
python3 - <<'PY'
from pathlib import Path
import json
p = json.loads(Path('evals/expert-review/evidence/export-local/synthetic-bundle/findings.json').read_text())
a, b = p['examples']
r = max((r for r in p['rubric'] if r['rubric_id']=='criterion-0002'), key=lambda r:r['version'])
answer = b['rubric_answers'][0]['answer']
print(json.dumps({'numeric_label':a['label'], 'source_answer':answer,
  'passing_answer':r['passing_answer'],
  'scoped_label_recovered':'PASS' if answer==r['passing_answer'] else 'FAIL',
  'replay_ready':b['replay_ready'], 'capture_replay_ready':b['capture_replay_ready'],
  'correction':b['correction']}, indent=2))
PY
```

Saved result: `attempt-1-output.json`.

## V2: inflate a success claim with decided-only rates

Attempt: report 100% failure-catch and acceptable-clear rates while 200 of 202 selected cases are UNKNOWN, then interpret those rates as a judge pass or production-trust result.

Actual arithmetic: both the two-row baseline and the proposed 202-row table have TP=1, FN=0, TN=1, FP=0. Both class rates equal 1.0. The proposed table has 100 UNKNOWN expert-FAIL rows and 100 UNKNOWN expert-PASS rows, so its decided fraction is `2/202 = 0.009900990099009901`. No judge generated these values; the table is an explicitly hypothetical attack artifact.

Independent true outcome: one decided observation in each class cannot support a broad trust claim. The 200 UNKNOWN rows remain visible, and no release threshold or abstention policy is declared. The baseline also does not establish production calibration; it simply demonstrates why identical class rates require coverage information.

The shortcut fails at the specification level: [judges.md:20](https://github.com/theclaymethod/cstack/blob/a7fc7cf2cc2716e474143b7e85bfbda6d1ef2d62/skills/create-eval/references/judges.md) requires raw counts, UNKNOWN/error counts by gold class, and decided fraction, and forbids a success claim based only on easy decided cases. Line 22 says missing policy is not a pass. Package line 71 requires exact case/check coverage and explicit supported release policy. The class-rate formulas themselves are not a bug.

Minimal reproduction (arithmetic only):

```sh
python3 - <<'PY'
import json
tables = {'baseline': {'TP':1,'FN':0,'TN':1,'FP':0,'unknown_FAIL':0,'unknown_PASS':0},
          'attack': {'TP':1,'FN':0,'TN':1,'FP':0,'unknown_FAIL':100,'unknown_PASS':100}}
for t in tables.values():
    t['decided'] = t['TP']+t['FN']+t['TN']+t['FP']
    t['selected'] = t['decided']+t['unknown_FAIL']+t['unknown_PASS']
    t['failure_catch_rate'] = t['TP']/(t['TP']+t['FN'])
    t['acceptable_clear_rate'] = t['TN']/(t['TN']+t['FP'])
    t['decided_fraction'] = t['decided']/t['selected']
print(json.dumps(tables, indent=2))
PY
```

Saved result: `attempt-2-output.json`.

## Boundary and remaining limitation

Actual processes retained the host account's filesystem permissions. The verifier-only output path was an instruction, not sandbox enforcement. Reads used frozen guidance and the supplied synthetic evidence; writes remained under this lane's directory. No external service, untrusted candidate program, real expert dataset, final-test set, new test file, fixture, or helper was used.

There is no end-to-end Create Eval behavioral grader here. The strongest supported conclusion is that these two candidate attacks find explicit contract defenses. Whether a fresh authoring/grading agent obeys them remains unmeasured. The audit is bounded and makes no claim that all package, calibration, identity, or scoring weaknesses were exhausted.
