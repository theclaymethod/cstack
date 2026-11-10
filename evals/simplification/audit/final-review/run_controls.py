"""Independent finite controls, 32 native cases; no remote calls."""
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
PROJECT = BASE / 'cstack/fixtures/playground'
sys.path.insert(0, str(PROJECT))
from simplification.protocol import Experiment, UNITS, configuration
from methods.native import Runs, evaluate

full = configuration('old-fixture', set(UNITS))
lean = configuration('old-fixture', {'contract', 'legacy-auth', 'duplicate-b'})
experiment = Experiment(OUT / 'clean', limit=24, confirmation_reserve=8)
experiment.measure('original', full)
experiment.measure('reduced', lean)
development = experiment.compare('original', 'reduced')
experiment.freeze({'final-original': full, 'final-reduced': lean})
experiment.confirm('final-original')
experiment.confirm('final-reduced')
experiment.finish()
confirmation = experiment.compare('final-original', 'final-reduced')

# Choose a valid ID unrelated to the reference pattern and exercise the
# explicitly permitted clarify action for generic trouble and duplicates.
source = (PROJECT / 'examples/candidates/improved.py').read_text()
boundary = '\nif __name__ == "__main__":'
alternative = source.split(boundary)[0] + '''
base_respond = respond
def respond(payload):
    output = base_respond(payload)
    if output['action'] == 'create_ticket':
        existing = {t['id'] for t in payload['state']['tickets']}
        ticket_id = 'independent-review-unique'
        while ticket_id in existing:
            ticket_id += '-next'
        output['state']['tickets'][-1]['id'] = ticket_id
    elif ('My VPN connection keeps dropping.' == payload['request']['text']
          or 'An open VPN ticket' in output['note']):
        output['action'] = 'clarify'
        output['note'] = 'Please confirm how you want to proceed.'
    return output

if __name__ == '__main__':
    print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))
'''
candidate = OUT / 'legitimate_alternative.py'
candidate.write_text(alternative)
runs = Runs(OUT / 'alternative-native', limit=8)
traces = runs.run('alternative', candidate, evaluate.load_cases('development'))

result = {'development_gate': development, 'confirmation_gate': confirmation,
          'clean_reservations': experiment.runs.reserved,
          'alternative_counts': {key: sum(t['outcome'] == key for t in traces)
                                 for key in ('PASS', 'FAIL', 'ERROR', 'UNKNOWN')},
          'native_cases': 24 + len(traces)}
(OUT / 'controls.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
