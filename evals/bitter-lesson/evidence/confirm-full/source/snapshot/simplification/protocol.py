"""Execute prompt-removal fixtures through the existing native evaluator."""
import copy
import json
import math
from pathlib import Path
import re
import time

from methods.native import ROOT, Runs, evaluate


# These synthetic cues deliberately encode dependencies and interactions.
# They are not learned model behavior or claims about real prompting.
UNITS = {
    'contract': {'text': 'Apply the complete support-ticket task contract below.', 'protected': True},
    'legacy-auth': {'text': 'LEGACY STEP: explicitly check authorization before answering.'},
    'duplicate-a': {'text': 'DUPLICATE CHECK A: inspect open VPN tickets for the selected account.'},
    'duplicate-b': {'text': 'DUPLICATE CHECK B: reuse an open VPN ticket for the same account.'},
    'plan': {'text': 'PLAN HEADER: organize a preliminary answer plan.'},
    'plan-detail': {'text': 'PLAN DETAIL: elaborate the preliminary plan.', 'requires': ['plan']},
    'example': {'text': 'EXAMPLE: a how-to question receives guidance without changing state.'},
    'conflict-a': {'text': 'CONFLICT A: apply the first synthetic steering convention.'},
    'conflict-b': {'text': 'CONFLICT B: apply the compensating synthetic steering convention.'},
}
MODELS = ('old-fixture', 'new-fixture')
EVIDENCE = ('manifest.json', 'summary.json', 'traces.jsonl', 'candidate.py', 'cases.jsonl')


def configuration(model, retained):
    if model not in MODELS:
        raise ValueError('Only explicitly simulated fixture models are supported')
    if not isinstance(retained, (list, tuple, set, frozenset)) or any(not isinstance(x, str) for x in retained):
        raise ValueError('Retained units must be a collection of names')
    if len(retained) != len(set(retained)) or set(retained) - UNITS.keys():
        raise ValueError('Unknown or duplicate removal units')
    selected = set(retained)
    for name, unit in UNITS.items():
        if unit.get('protected') and name not in selected:
            raise ValueError('Protected task contract must remain')
        if name in selected and not set(unit.get('requires', ())) <= selected:
            raise ValueError('Surviving dependent requires its parent: ' + name)
    return {'model': model, 'retained': sorted(selected)}


def render(config):
    config = configuration(config['model'], config['retained'])
    sections = []
    for name in config['retained']:
        text = UNITS[name]['text']
        if name == 'contract':
            text += '\n' + (ROOT / 'evals/rubric.md').read_text()
        sections.append('### ' + name + '\n' + text)
    return '\n\n'.join(sections) + '\n'


def candidate_source(config):
    """A standalone subprocess consumes the actual rendered prompt text."""
    config = configuration(config['model'], config['retained'])
    source = (ROOT / 'examples/candidates/improved.py').read_text()
    boundary = '\nif __name__ == "__main__":'
    if source.count(boundary) != 1:
        raise ValueError('Conforming candidate entrypoint changed; inspect fixture adapter')
    base = source.split(boundary)[0]
    settings = '\nPROMPT = ' + repr(render(config)) + '\nMODEL = ' + repr(config['model']) + '\n'
    cues = '\nCUES = ' + repr({key: value['text'] for key, value in UNITS.items()}) + '\n'
    worker = '''
conforming_respond = respond

def respond(payload):
    output = conforming_respond(payload)
    has = lambda name: CUES[name] in PROMPT
    # Deliberately fabricated model-dependent behavior, not an LLM.
    if (MODEL == 'old-fixture' and not has('legacy-auth')) or (has('conflict-a') != has('conflict-b')):
        return {'action': 'guidance', 'account': None, 'state': copy.deepcopy(payload['state']),
                'note': 'Deterministic fixture lost a required steering combination.'}
    if not has('duplicate-a') and not has('duplicate-b'):
        request = payload['request']
        account = request['account']
        if account is None and len(request['accounts']) == 1:
            account = request['accounts'][0]
        if account in request['accounts'] and any(t['account'] == account and t['status'] == 'open'
                and t['issue'] == 'vpn' for t in payload['state']['tickets']):
            state = copy.deepcopy(payload['state'])
            ids = {t['id'] for t in state['tickets']}
            sequence = 1
            while 'fixture-' + str(sequence) in ids:
                sequence += 1
            state['tickets'].append({'id': 'fixture-' + str(sequence), 'account': account,
                                    'status': 'open', 'issue': 'vpn'})
            return {'action': 'create_ticket', 'account': account, 'state': state,
                    'note': 'Deterministic fixture omitted duplicate steering.'}
    return output

if __name__ == '__main__':
    print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))
'''
    return base + settings + cues + worker


def sources():
    return {'native': evaluate.identity(), 'catalog': evaluate.json_hash(UNITS),
            'files': {str(p.relative_to(ROOT)): evaluate.digest(p) for p in [
                ROOT / 'methods/native.py', ROOT / 'examples/candidates/improved.py',
                *sorted((ROOT / 'simplification').glob('*.py'))]}}


def quality_gate(original, candidate, max_loss=0.0, allow_pass_regressions=False):
    """Exact finite-case policy, not a statistical non-inferiority test."""
    if (type(max_loss) not in (int, float) or not 0 <= max_loss <= 1
            or not math.isfinite(max_loss) or type(allow_pass_regressions) is not bool):
        raise ValueError('Declare a finite loss margin and regression policy')
    before, after = original['outcomes'], candidate['outcomes']
    if not before or before.keys() != after.keys():
        raise ValueError('Quality comparison needs identical nonempty membership')
    allowed = {'PASS', 'FAIL', 'ERROR', 'UNKNOWN'}
    if any(value not in allowed for value in [*before.values(), *after.values()]):
        raise ValueError('Unrecognized native outcome')
    baseline_score = sum(x == 'PASS' for x in before.values()) / len(before)
    score = sum(x == 'PASS' for x in after.values()) / len(after)
    regressions = [key for key in before if before[key] == 'PASS' and after[key] != 'PASS']
    errors = sum(value in ('ERROR', 'UNKNOWN') for value in after.values())
    return {'admissible': score + 1e-12 >= baseline_score - max_loss
                and (allow_pass_regressions or not regressions) and errors == 0,
            'baseline_score': baseline_score, 'candidate_score': score, 'difference': score - baseline_score,
            'regressions': regressions, 'errors_or_unknown': errors, 'max_loss': max_loss,
            'scope': 'Exact outcomes on the declared finite synthetic cases only'}


class Experiment:
    """One-shot local controls with reserved confirmation; not a resumable optimizer."""
    def __init__(self, directory, limit=200, confirmation_reserve=20):
        if (type(limit) is not int or type(confirmation_reserve) is not int
                or not 0 <= confirmation_reserve <= limit):
            raise ValueError('Execution budget and confirmation reserve must be nonnegative integers')
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=False)
        self.runs = Runs(self.directory / 'native', limit)
        (self.directory / 'candidates').mkdir()
        self.records, self.plan = {}, {}
        self.status = 'search'
        self.reserve = confirmation_reserve
        self.contract = {'sources': sources(), 'limit': limit, 'confirmation_reserve': confirmation_reserve,
            'authority': 'Synthetic task contract and explicit model stand-ins; not human gold',
            'exposure': 'All cases readable; confirmation is a workflow role, not unseen evidence',
            'development': [r['id'] for r in evaluate.load_cases('development')],
            'confirmation': [r['id'] for r in evaluate.load_cases('confirmation')]}
        evaluate.write_json(self.directory / 'contract.json', self.contract)
        self.contract_hash = evaluate.digest(self.directory / 'contract.json')
        self._save()

    def _receipt(self):
        return {'limit': self.runs.limit, 'reserved': self.runs.reserved,
                'actual_completed': sum(call.get('executed', 0) for call in self.runs.calls),
                'calls': self.runs.calls}

    def _state(self):
        return {'status': self.status, 'records': self.records,
            'plan': self.plan, 'reserved_case_executions': self.runs.reserved,
            'remaining_confirmation_reserve': self.reserve, 'contract_hash': self.contract_hash,
            'native_receipt_sha256': evaluate.json_hash(self._receipt())}

    def _save(self):
        evaluate.write_json(self.directory / 'state.json', self._state())
        self.state_hash = evaluate.digest(self.directory / 'state.json')

    def verify(self):
        if (evaluate.digest(self.directory / 'contract.json') != self.contract_hash
                or evaluate.digest(self.directory / 'state.json') != self.state_hash
                or not evaluate.same_json(evaluate.read_json(self.directory / 'contract.json'), self.contract)
                or not evaluate.same_json(evaluate.read_json(self.directory / 'state.json'), self._state())
                or self.runs.limit != self.contract['limit']
                or sources() != self.contract['sources']):
            raise ValueError('Experiment contract, state, or source changed')
        receipt = self.runs.directory / 'executions.json'
        if self.runs.calls or receipt.exists():
            if not receipt.is_file() or not evaluate.same_json(evaluate.read_json(receipt), self._receipt()):
                raise ValueError('Native execution ledger differs from reserved attempts')
        for label, record in self.records.items():
            if record['status'] == 'complete':
                folder = self.runs.directory / label
                if any(evaluate.digest(folder / name) != expected for name, expected in record['evidence'].items()):
                    raise ValueError('Completed native evidence changed')

    def measure(self, label, config):
        self.verify()
        if self.status != 'search':
            raise ValueError('Fitting is closed after confirmation freeze')
        return self._execute(label, config, 'development')

    def _execute(self, label, config, suite):
        config = configuration(config['model'], config['retained'])
        if (not isinstance(label, str) or re.fullmatch(r'[a-z0-9][a-z0-9-]*', label) is None
                or label in self.records):
            raise ValueError('Choose an unused safe run label')
        candidate = self.directory / 'candidates' / (label + '.py')
        if candidate.exists() or candidate.is_symlink():
            raise ValueError('Existing candidate evidence must be preserved')
        cases = evaluate.load_cases(suite)
        protected = self.reserve if suite == 'development' else self.reserve - len(cases)
        if self.runs.reserved + len(cases) + protected > self.runs.limit or protected < 0:
            raise RuntimeError('Budget exhausted or confirmation reserve would be spent')
        code = candidate_source(config)
        candidate.write_text(code)
        record = {'config': config, 'suite': suite, 'status': 'pending',
                  'prompt_utf8_bytes': len(render(config).encode()), 'unit_count': len(config['retained']),
                  'candidate_sha256': evaluate.digest(candidate)}
        self.records[label] = record
        self._save()
        started = time.monotonic()
        try:
            traces = self.runs.run(label, candidate, cases)
            record.update(status='complete', outcomes={row['id']: row['outcome'] for row in traces},
                native_wall_seconds=time.monotonic() - started,
                evidence={name: evaluate.digest(self.runs.directory / label / name) for name in EVIDENCE})
            if suite == 'confirmation':
                self.reserve -= len(cases)
        finally:
            self._save()  # Interrupted executions stay charged in the native reservation ledger.
        return self.checked(label)

    def checked(self, label):
        self.verify()
        record = self.records[label]
        if record['status'] != 'complete':
            raise ValueError('Incomplete result cannot support a comparison')
        manifest, summary = evaluate.checked_run(self.runs.directory / label)
        if (manifest['case_ids'] != self.contract[record['suite']]
                or manifest['candidate_hash'] != record['candidate_sha256']
                or record['outcomes'] != {row['id']: row['outcome'] for row in summary['results']}):
            raise ValueError('Execution differs from the declared candidate or membership')
        return copy.deepcopy(record)

    def compare(self, original, candidate):
        before, after = self.checked(original), self.checked(candidate)
        evaluate.compare_runs(self.runs.directory / original, self.runs.directory / candidate)
        return quality_gate(before, after)

    def freeze(self, plan):
        self.verify()
        if self.status != 'search' or not isinstance(plan, dict) or not plan:
            raise ValueError('Choose a nonempty exact confirmation plan once')
        if any(row['status'] != 'complete' for row in self.records.values()):
            raise ValueError('Incomplete search attempt remains charged; start a new experiment')
        prepared = {}
        for label, config in plan.items():
            if (not isinstance(label, str) or re.fullmatch(r'[a-z0-9][a-z0-9-]*', label) is None
                    or label in self.records):
                raise ValueError('Invalid or already used confirmation label')
            prepared[label] = configuration(config['model'], config['retained'])
        needed = len(prepared) * len(evaluate.load_cases('confirmation'))
        if needed > self.reserve or self.runs.reserved + needed > self.runs.limit:
            raise RuntimeError('Exact final plan exceeds reserved confirmation allowance')
        self.plan = copy.deepcopy(prepared)
        self.reserve = needed
        self.status = 'frozen'
        self._save()

    def confirm(self, label):
        self.verify()
        if self.status != 'frozen' or label not in self.plan:
            raise ValueError('Confirmation requires an exact frozen plan entry')
        return self._execute(label, self.plan[label], 'confirmation')

    def finish(self):
        self.verify()
        if self.status != 'frozen' or any(label not in self.records or
                self.records[label]['status'] != 'complete' for label in self.plan):
            raise ValueError('All planned final executions must complete')
        for label in self.plan:
            self.checked(label)
        self.status = 'finished'
        self._save()
