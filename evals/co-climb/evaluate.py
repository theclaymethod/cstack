"""Grade co-climb decisions, or prepare answer-free prompts for an external runtime."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIELDS = {'case_id', 'actions', 'archive', 'promote', 'judge'}


def parse_answer(text):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON field: ' + key)
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=unique_keys)


def load_cases():
    return [json.loads(line) for line in (HERE / 'cases.jsonl').read_text().splitlines() if line.strip()]


def grade(case, expected, answer):
    errors = []
    if not isinstance(answer, dict) or set(answer) != FIELDS:
        return ['Answer must contain exactly the five required fields']
    if answer['case_id'] != case['id']:
        errors.append('Wrong case identity')
    for field in ('actions', 'archive', 'promote'):
        values = answer[field]
        if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
            errors.append(f'{field} must be a list of strings')
        elif len(values) != len(set(values)):
            errors.append(f'{field} contains duplicate IDs')
    if errors:
        return errors
    if set(answer['actions']) != set(expected['actions']):
        errors.append('Next actions omit or contradict required decisions')
    elif any(answer['actions'].index(first) >= answer['actions'].index(second) for first, second in expected['before']):
        errors.append('Next actions violate an evidence dependency')
    archives = [expected['archive'], *expected['alternative_archives']]
    if set(answer['archive']) not in [set(value) for value in archives]:
        errors.append('Exploratory archive violates the scenario policy')
    if set(answer['promote']) != set(expected['promote']):
        errors.append('Promotion violates the evidence gate')
    if answer['judge'] != expected['judge']:
        errors.append('Judge selection violates the calibration policy')
    return errors


def prepare(out):
    out.mkdir(parents=True, exist_ok=False)
    sources = [HERE / 'prompt.md', ROOT / 'skills/co-climb/SKILL.md',
               *sorted((ROOT / 'skills/co-climb/references').glob('*.md'))]
    context = '\n\n'.join(f'## {p.relative_to(ROOT)}\n{p.read_text()}' for p in sources)
    for case in load_cases():
        (out / f"{case['id']}.txt").write_text(context + '\n\n## Situation\n' + json.dumps({key: value for key, value in case.items() if key not in {'family', 'source'}}, indent=2) + '\n')
    (out / 'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [*sources, HERE/'cases.jsonl']}, indent=2)+'\n')


def evaluate(answers):
    cases = load_cases()
    expected = json.loads((HERE / 'expected.json').read_text())
    by_id = {}
    for row in answers:
        if not isinstance(row, dict) or not isinstance(row.get('case_id'), str):
            raise ValueError('Each answer must identify its case')
        if row['case_id'] in by_id:
            raise ValueError('Duplicate case answer: ' + row['case_id'])
        by_id[row['case_id']] = row
    unknown = set(by_id) - {case['id'] for case in cases}
    if unknown:
        raise ValueError('Unknown case IDs: ' + ', '.join(sorted(unknown)))
    results = []
    for case in cases:
        answer = by_id.get(case['id'])
        errors = ['No answer submitted'] if answer is None else grade(case, expected[case['id']], answer)
        results.append({'id': case['id'], 'family': case['family'], 'verdict': 'ERROR' if answer is None else 'FAIL' if errors else 'PASS', 'errors': errors})
    return {'scope': 'Synthetic next-step decision eval; not end-to-end campaign performance',
            'total': len(cases), 'counts': {v: sum(r['verdict']==v for r in results) for v in ['PASS','FAIL','ERROR']}, 'results': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prepare', type=Path)
    group.add_argument('--answers', type=Path)
    args = parser.parse_args()
    if args.prepare:
        prepare(args.prepare)
    else:
        try:
            report = evaluate([parse_answer(line) for line in args.answers.read_text().splitlines() if line.strip()])
        except (ValueError, TypeError) as error:
            print(json.dumps({'status':'ERROR','reason':str(error)}))
            raise SystemExit(2) from error
        print(json.dumps(report, indent=2))
        raise SystemExit(0 if report['counts']['PASS']==report['total'] else 1)


if __name__ == '__main__':
    main()
