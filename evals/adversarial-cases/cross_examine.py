"""Replay the confirmed playground and fixed-construction evidence defects.

Copied-evidence mutations are operator calibration, not candidate exploits.
This launches 42 native cases and three own-process interruptions, with no models.
"""

import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1]
EVIDENCE = HERE / 'evidence/cross-examine'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def acceptance(validator, base, workspace=None):
    try:
        checks = validator.validate(base, workspace) if workspace else validator.validate(base)
        return {'accepted': True, 'checks': len(checks)}
    except (RuntimeError, ValueError, KeyError, OSError) as error:
        return {'accepted': False, 'error': str(error)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    current = module('adversarial_current_replay', HERE / 'replay.py')
    original = module('adversarial_original_replay', EVIDENCE / 'original-replay.py')
    current.invoke([sys.executable, str(HERE / 'replay.py'), '--out', str(out / 'clean-replay')],
                   SOURCE, out / 'clean-replay-receipt.json')
    workspace = out / 'clean-replay/workspace'
    pristine = workspace / 'eval-runs/case-build'

    old_workspace = out / 'original-native'
    shutil.copytree(SOURCE / 'fixtures/playground', old_workspace,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git', 'eval-runs', '.agents', '.claude', '.cursor'))
    shutil.copy2(EVIDENCE / 'original-evaluate.py', old_workspace / 'evaluate.py')
    contrast = EVIDENCE / 'semantic-cases/extra-field-reduction'
    native_results = []
    for version, root in [('original', old_workspace), ('repaired', workspace)]:
        for candidate in ['four-fields', 'five-fields']:
            label = version + '-' + candidate
            run = out / label
            current.invoke([sys.executable, str(root / 'evaluate.py'), 'run',
                            '--candidate', str(contrast / (candidate + '.py')),
                            '--cases', str(contrast / 'cases.jsonl'), '--suite', 'development',
                            '--out', str(run)], root, out / (label + '-receipt.json'))
            summary = read(run / 'summary.json')
            current.require(summary['executed_count'] == 1, 'Native contrast did not execute exactly one case')
            expected = 'ERROR' if version == 'original' and candidate == 'five-fields' else 'PASS'
            current.require(summary['counts'][expected] == 1, 'Unexpected metadata contrast: ' + label)
            native_results.append({'version': version, 'candidate': candidate, 'counts': summary['counts']})

    probes = out / 'evidence-probes'
    probes.mkdir()
    results = []
    for label in ['clean', 'stdout-output-conflict', 'empty-source-inventory',
                  'missing-lifecycle-observation', 'empty-lifecycle-observations', 'missing-native-command']:
        base = probes / label
        shutil.copytree(pristine, base)
        if label == 'stdout-output-conflict':
            path = base / 'native-legitimate/traces.jsonl'
            traces = [json.loads(line) for line in path.read_text().splitlines()]
            output = json.loads(traces[0]['stdout'])
            output['state'] = traces[0]['input']['state']
            traces[0]['stdout'] = json.dumps(output) + '\n'
            path.write_text(''.join(json.dumps(trace) + '\n' for trace in traces))
        elif label == 'empty-source-inventory':
            write(base / 'source-before.json', {})
            write(base / 'source-after.json', {})
        elif label == 'missing-lifecycle-observation':
            path = base / 'lifecycle-observations.json'
            write(path, [row for row in read(path) if row['label'] != 'lifecycle-complete-stop-1'])
        elif label == 'empty-lifecycle-observations':
            write(base / 'lifecycle-observations.json', [])
        elif label == 'missing-native-command':
            path = base / 'commands.json'
            write(path, [row for row in read(path) if row['label'] != 'native-legitimate'])
            (base / 'native-legitimate.receipt.json').unlink()
        before = acceptance(original, base)
        after = acceptance(current, base, workspace)
        result = {'probe': label, 'access': 'Operator-owned copies of current synthetic development evidence',
                  'original_validator': before, 'repaired_validator': after,
                  'new_candidate_executions': 0, 'new_interruptions': 0}
        results.append(result)
        write(out / 'probe-results.json', results)
        current.require(before['accepted'] and after['accepted'] == (label == 'clean'),
                        'Unexpected validator calibration: ' + label)

    result = {'status': 'passed', 'scope': 'Synthetic development replay; operator evidence calibration, '
              'not candidate access, trusted attestation, fresh skill execution, or generalization',
              'native_contrast': native_results, 'evidence_probes': results,
              'actual_native_case_executions': 42, 'owned_process_interruptions': 3,
              'source_versions': 'Original source snapshots retained beside the audit; current checkout for repair'}
    write(out / 'results.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
