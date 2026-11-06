# Create Eval audit

One Cross-Examine round against [C Stack v0.3.0](https://github.com/theclaymethod/cstack/tree/a7fc7cf2cc2716e474143b7e85bfbda6d1ef2d62): three agents, two attempts per lane, no confirmed flaw reproduced. The coordinator independently replayed the two actual HTTP/lifecycle probes with identical outcomes. The skill and helper were left unchanged.

This is a development audit, not a passing end-to-end skill evaluation. No end-to-end Create Eval behavioral grader exists. The verifier lane analyzed source scope and hypothetical arithmetic; the environment lane exercised the trusted helper; the contract lane actually authored a small package and an early-development plan. Those are different forms of evidence.

| Lane | What ran | Result |
| --- | --- | --- |
| [Verifier](evidence/round-1/verifier/report.md) | Existing-evidence parsing and hypothetical low-coverage arithmetic | No contract bypass identified; agent compliance with those rules was not measured. |
| [Environment](evidence/round-1/environment/report.md) | Real HTTP saves, changed trace versions, independent review IDs, amendments, stale writes, and restarts | Old-version and stale writes rejected; matching reviews, dissent, and history retained in these paths. |
| [Task contract](evidence/round-1/contract/report.md) | One source-naming eval package and one handwritten-trace promotion decision | Uncertainty retained, alternative source representations accepted, no invented gold or product-run claim. |

The [source-naming package](evidence/round-1/contract/attempt-1-source-contract/rubric.md) has four development rows. Two named-source representations were judged PASS; absent and empty source names were judged FAIL. The author already knew the source annotations, so these are disclosed development observations, not a blind judge-agreement rate. All case gold is null. The criterion measures naming only; it makes no claim about source reliability, numerical correctness, or clinical truth.

Read the [ledger](CROSS_EXAMINE_LEDGER.md) for intent, access, budget, individual mechanisms, and remaining limits. The [evidence manifest](evidence/round-1/evidence-manifest.json) records guidance and artifact hashes. No Docker, database, paid API, hosted service, untrusted submission program, or new test files/helpers were needed. All data are synthetic.

## Reproduction

Run commands from the repository root. The lane reports contain the exact inline commands, with checkout prefixes converted to project-relative paths. Preserve existing evidence: use a fresh scratch directory or checkout. The commands intentionally stop rather than overwrite earlier attempts.

The environment commands require the frozen guidance and the previously generated local trace projection. Restore those from the pinned commit and the archived synthetic inputs. The contract artifacts are copied for inspection; this does not rerun their authoring agent.

```bash
python3 - <<'PY'
import io, shutil, subprocess, tarfile
from pathlib import Path
revision = 'a7fc7cf2cc2716e474143b7e85bfbda6d1ef2d62'
run = Path('eval-runs/create-eval-cross-examine-v03')
run.mkdir(parents=True, exist_ok=False)
archive = subprocess.check_output(['git', 'archive', revision, 'skills/create-eval', 'skills/run-eval', 'skills/expert-mode/references'])
with tarfile.open(fileobj=io.BytesIO(archive)) as source:
    source.extractall(run / 'frozen', filter='data')
evidence = Path('evals/create-eval/evidence/round-1')
projection = Path('eval-runs/trace-review-20261106T184157')
projection.mkdir(parents=True, exist_ok=False)
for source_name, target_name in [('trace-projection.jsonl', 'traces.jsonl'), ('review-history.jsonl', 'reviews.jsonl')]:
    with (projection / target_name).open('xb') as destination:
        destination.write((evidence / 'inputs' / source_name).read_bytes())
shutil.copytree(evidence / 'contract', run / 'contract')
PY
```

Then run the two inline blocks in the [environment report](evidence/round-1/environment/report.md). The expected observations are in the [coordinator replay receipt](evidence/round-1/coordinator/replay.json). The standard-library checks do not require a browser; rendering and browser interaction remain unverified. The reconstruction uses Python with `tarfile` data-filter support.

The [verifier report](evidence/round-1/verifier/report.md) provides its source-extraction and arithmetic commands; neither is a grading run. The [contract report](evidence/round-1/contract/report.md) provides direct checks against the authored artifacts; matching their hashes or observable contents does not replay a model's authoring behavior.

All seven published inline blocks were replayed successfully in a fresh local clone. The [public reproduction receipt](evidence/round-1/public-reproduction.json) records command hashes, process exits, and actual output. This validates the documentation and these fixed outcomes, not fresh model compliance.
