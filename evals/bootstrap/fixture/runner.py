import argparse
import json
from pathlib import Path


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def run(cases_path, observations_path):
    cases = rows(cases_path)
    observations = rows(observations_path)
    if not cases or len({c['id'] for c in cases}) != len(cases):
        raise ValueError('Cases need unique IDs and at least one case')
    if len({o['case_id'] for o in observations}) != len(observations):
        raise ValueError('Duplicate observations')
    by_id = {o['case_id']: o for o in observations}
    if set(by_id) - {c['id'] for c in cases}:
        raise ValueError('Unknown observation case')
    results = []
    for case in cases:
        expected = case['expected']
        if not expected['allowed_actions'] or type(expected['ticket_delta']) is not int:
            raise ValueError('Invalid expectation')
        observed = by_id.get(case['id'])
        if observed is None or 'action' not in observed or type(observed.get('ticket_delta')) is not int:
            results.append({'id': case['id'], 'verdict': 'ERROR'})
            continue
        accepted = observed['action'] in expected['allowed_actions'] and observed['ticket_delta'] == expected['ticket_delta']
        results.append({'id': case['id'], 'verdict': 'PASS' if accepted else 'FAIL'})
    return {'boundary': 'stored-observation', 'results': results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cases', required=True)
    parser.add_argument('--observations', required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.cases, args.observations), indent=2))
