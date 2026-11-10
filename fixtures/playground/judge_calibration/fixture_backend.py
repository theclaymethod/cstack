"""Deterministic response-shape fixture. This is neither Jev nor an LLM."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    envelope = json.load(sys.stdin)
    payload, config = envelope['input'], envelope['config']
    if set(payload) != {'id', 'case', 'output', 'criterion_version'}:
        raise ValueError('Judge receives only declared public evidence')
    if set(payload['case']) != {'request', 'state', 'expected'}:
        raise ValueError('Private annotation/partition fields are not judge inputs')
    if config['policy'] == 'claim-only':
        passed = payload['output'].get('action') == 'create_ticket'
    elif config['policy'] == 'state-witness':
        spec = importlib.util.spec_from_file_location('fixture_native', ROOT / 'evaluate.py')
        native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
        passed = native.grade(payload['output'], payload['case'])['outcome'] == 'PASS'
    else:
        raise ValueError('Unknown predeclared fixture policy')
    if config['backend'] == 'jev':
        # Fixed synthetic scores exercise threshold selection; they are not calibrated probabilities.
        raw = {'model': 'offline-jev-shape-fixture', 'answers': {'criterion': {'type': 'noul', 'noul': .15 if passed else .65}}}
    else:
        raw = {'model': 'offline-llm-shape-fixture', 'text': json.dumps({'verdict': 'PASS' if passed else 'FAIL',
                'reason': 'Deterministic fixture policy; no generated model reasoning.'})}
    print(json.dumps(raw))


if __name__ == '__main__':
    main()
