"""Native-derived synthetic calibration, frozen predictions and final-exposure controls."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import time
from methods.native import ROOT, Runs, evaluate, jsonl, read_rows, write
from .adapters import normalize
from .statistics import agreement, uncertainty, probability_diagnostics


def sources():
    identity = evaluate.identity()
    result = identity['files']
    result['python_runtime'] = identity['python']
    result.update({str(p.relative_to(ROOT)): evaluate.digest(p) for p in (ROOT / 'judge_calibration').glob('*.py')})
    return result


def public_input(row):
    """Expected task behavior is a permitted reference; correctness labels stay private."""
    return {'id': row['id'], 'case': {key: copy.deepcopy(row['case'][key]) for key in ('request', 'state', 'expected')},
            'output': copy.deepcopy(row['output']), 'criterion_version': 'native-support-contract-v1'}


def prepare(directory):
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=False)
    runs = Runs(directory / 'native-source', 24)
    cases = evaluate.load_cases('all'); examples = []
    for candidate in [ROOT / 'support_agent.py', ROOT / 'examples/candidates/improved.py']:
        traces = runs.run(candidate.stem, candidate, cases)
        for index, (case, trace) in enumerate(zip(cases, traces)):
            if trace['outcome'] not in ('PASS', 'FAIL'):
                raise ValueError('Synthetic label requires a completed native verdict')
            examples.append({'id': 'item-' + str(len(examples)).zfill(3), 'case': case,
                'output': trace['output'], 'gold': trace['outcome'], 'family': case['family'],
                'role': 'train' if index < 4 else 'validation' if index < 8 else 'final',
                'authority': 'code-derived synthetic fixture, not human gold',
                'source_trace': str(runs.directory / candidate.stem / 'traces.jsonl')})
    jsonl(directory / 'labels.private.jsonl', examples)
    jsonl(directory / 'inputs.jsonl', [public_input(row) for row in examples])
    write(directory / 'manifest.json', {'labels_sha256': evaluate.digest(directory / 'labels.private.jsonl'),
        'inputs_sha256': evaluate.digest(directory / 'inputs.jsonl'), 'sources': sources(),
        'native_executions': runs.reserved,
        'counts': {role: sum(r['role'] == role for r in examples) for role in ('train', 'validation', 'final')},
        'exposure': 'Fully readable synthetic development fixture; final is a workflow role, not unseen evidence',
        'authority': 'Fixture-derived labels only; no expert approval'})
    return directory


class Campaign:
    def __init__(self, dataset, output, worker_limit=200):
        self.dataset = Path(dataset).resolve(); self.output = Path(output).resolve()
        self.output.mkdir(parents=True, exist_ok=False)
        self.manifest = evaluate.read_json(self.dataset / 'manifest.json')
        self.state = {'phase': 'fitting', 'worker_limit': worker_limit, 'worker_calls': 0,
                      'reserved_calls': 0, 'runs': [], 'exposed_roles': ['train', 'validation']}
        self.save(); self.rows()

    def save(self):
        evaluate.write_json(self.output / 'state.json', self.state)

    def rows(self):
        if evaluate.read_json(self.dataset / 'manifest.json') != self.manifest or sources() != self.manifest['sources']:
            raise ValueError('Calibration source or manifest changed')
        for filename, field in [('labels.private.jsonl', 'labels_sha256'), ('inputs.jsonl', 'inputs_sha256')]:
            if evaluate.digest(self.dataset / filename) != self.manifest[field]:
                raise ValueError('Calibration dataset content changed')
        rows = read_rows(self.dataset / 'labels.private.jsonl')
        if len({r['id'] for r in rows}) != len(rows) or any(r['gold'] not in ('PASS', 'FAIL') for r in rows):
            raise ValueError('Invalid or duplicate calibration labels')
        if not evaluate.same_json(read_rows(self.dataset / 'inputs.jsonl'), [public_input(row) for row in rows]):
            raise ValueError('Public judge projection differs from frozen source')
        family_roles = {}
        for row in rows:
            if row['role'] not in ('train', 'validation', 'final'):
                raise ValueError('Unknown partition')
            if row['family'] in family_roles and family_roles[row['family']] != row['role']:
                raise ValueError('Related source family crossed partitions')
            family_roles[row['family']] = row['role']
        if {role: sum(r['role'] == role for r in rows) for role in self.manifest['counts']} != self.manifest['counts']:
            raise ValueError('Calibration membership changed')
        return rows

    def predict(self, label, config, role):
        if role not in ('train', 'validation', 'final'):
            raise ValueError('Unknown role')
        if self.state['phase'] == 'final_consumed' or (self.state['phase'] == 'confirming' and role != 'final'):
            raise ValueError('Final exposure prevents further fitting')
        if role == 'final' and (self.state['phase'] != 'confirming'
                or self.state['final_plan'].get(label) != config):
            raise ValueError('Freeze this exact final candidate before judging')
        path = self.output / label
        if not label or Path(label).name != label or path.exists():
            raise ValueError('Use a fresh single-component run label')
        rows = [r for r in self.rows() if r['role'] == role]
        if self.state['reserved_calls'] + len(rows) > self.state['worker_limit']:
            raise ValueError('Fixture worker budget exhausted')
        path.mkdir(); self.state['reserved_calls'] += len(rows)
        self.state['runs'].append({'label': label, 'role': role, 'status': 'pending', 'reserved': len(rows),
                                   'config_hash': evaluate.json_hash(config)})
        self.save(); records = []; config = copy.deepcopy(config); write(path / 'config.json', config)
        for row in rows:
            payload = public_input(row); started = time.monotonic()
            try:
                process = subprocess.run([sys.executable, str(ROOT / 'judge_calibration/fixture_backend.py')],
                    input=json.dumps({'input': payload, 'config': config}), text=True, capture_output=True,
                    timeout=5, cwd=path)
                stdout, stderr, code = process.stdout, process.stderr, process.returncode
                try: raw = json.loads(stdout)
                except ValueError: raw = {}
            except subprocess.TimeoutExpired:
                stdout, stderr, code, raw = '', 'fixture judge timeout', None, {}
            self.state['worker_calls'] += 1
            records.append({'id': row['id'], 'input': payload, 'input_hash': evaluate.json_hash(payload),
                'raw': raw, 'stdout': stdout, 'stderr': stderr, 'exit_code': code,
                'elapsed_seconds': time.monotonic() - started, 'decision': normalize(raw, config, code)})
            jsonl(path / 'predictions.jsonl', records); self.save()
        write(path / 'manifest.json', {'config_hash': evaluate.json_hash(config), 'role': role,
            'ids': [r['id'] for r in rows], 'predictions_sha256': evaluate.digest(path / 'predictions.jsonl'),
            'sources': self.manifest['sources'], 'input_dataset_sha256': self.manifest['inputs_sha256']})
        self.state['runs'][-1].update(status='complete',
            predictions_sha256=evaluate.digest(path / 'predictions.jsonl'),
            manifest_sha256=evaluate.digest(path / 'manifest.json'))
        self.save()
        return path

    def compare(self, path):
        path = Path(path).resolve()
        manifest, config = evaluate.read_json(path / 'manifest.json'), evaluate.read_json(path / 'config.json')
        registered = [r for r in self.state['runs'] if r['label'] == path.name]
        if (path.parent != self.output or len(registered) != 1 or registered[0]['status'] != 'complete'
                or registered[0]['role'] != manifest['role']
                or registered[0]['config_hash'] != manifest['config_hash']):
            raise ValueError('Comparison needs a registered completed run and frozen configuration')
        if (registered[0]['predictions_sha256'] != evaluate.digest(path / 'predictions.jsonl')
                or registered[0]['manifest_sha256'] != evaluate.digest(path / 'manifest.json')):
            raise ValueError('Campaign-anchored prediction evidence changed')
        if manifest['role'] == 'final' and self.state['phase'] != 'final_consumed':
            raise ValueError('Freeze all planned final predictions before opening final labels')
        if (manifest['predictions_sha256'] != evaluate.digest(path / 'predictions.jsonl')
                or manifest['config_hash'] != evaluate.json_hash(config) or manifest['sources'] != sources()
                or manifest['input_dataset_sha256'] != self.manifest['inputs_sha256']):
            raise ValueError('Frozen judge evidence changed')
        records = read_rows(path / 'predictions.jsonl'); rows = [r for r in self.rows() if r['role'] == manifest['role']]
        if manifest['ids'] != [r['id'] for r in rows] or [r['id'] for r in records] != manifest['ids']:
            raise ValueError('Missing, duplicate or changed judge case coverage')
        pairs = []
        for row, record in zip(rows, records):
            payload = public_input(row)
            if (not evaluate.same_json(record['input'], payload) or record['input_hash'] != evaluate.json_hash(payload)
                    or not evaluate.same_json(record['decision'], normalize(record['raw'], config, record['exit_code']))):
                raise ValueError('Judge input or decision differs from retained evidence')
            if record['exit_code'] == 0:
                try: raw = json.loads(record['stdout'])
                except ValueError: raw = {}
                if not evaluate.same_json(raw, record['raw']):
                    raise ValueError('Raw response differs from judge stdout')
            pairs.append({'id': row['id'], 'family': row['family'], 'gold': row['gold'], **record['decision']})
        result = {'agreement': agreement(pairs), 'uncertainty': uncertainty(pairs),
                  'probabilities': probability_diagnostics(pairs), 'pairs': pairs,
                  'role': manifest['role'], 'evidence_hash': manifest['predictions_sha256']}
        write(path / 'comparison.json', result)
        return result

    def freeze(self, final_plan):
        if self.state['phase'] != 'fitting' or not final_plan:
            raise ValueError('Final evidence already opened or final plan empty')
        self.state.update(phase='confirming', final_plan=copy.deepcopy(final_plan)); self.save()

    def finish(self):
        complete = {r['label'] for r in self.state['runs'] if r['role'] == 'final' and r['status'] == 'complete'}
        if self.state['phase'] != 'confirming' or complete != set(self.state['final_plan']):
            raise ValueError('Every frozen final candidate needs complete predictions')
        self.state.update(phase='final_consumed', exposed_roles=['train', 'validation', 'final']); self.save()


def config(backend, policy='claim-only', threshold=.8):
    return {'backend': backend, 'policy': policy, 'model': 'offline-response-shape-fixture',
            'question_means_failure': True, 'pass_below': threshold, 'fail_at_or_above': threshold,
            'live_backend': False}


def run(directory):
    directory = Path(directory).resolve(); directory.mkdir(parents=True, exist_ok=False)
    dataset = prepare(directory / 'dataset'); campaign = Campaign(dataset, directory / 'campaign')
    baselines, selected, fitting = {}, {}, {}
    for backend in ['llm', 'jev']:
        baseline = config(backend); initial = campaign.predict(backend + '-baseline-train', baseline, 'train')
        baselines[backend] = baseline
        fitting[backend] = {'baseline_train': campaign.compare(initial), 'candidates': []}
        trials = [config(backend, policy, threshold) for policy in ['claim-only', 'state-witness']
                  for threshold in ([.5] if backend == 'llm' else [.5, .8])]
        for index, candidate in enumerate(trials):
            path = campaign.predict(backend + '-validation-' + str(index), candidate, 'validation')
            fitting[backend]['candidates'].append({'config': candidate, 'result': campaign.compare(path)})
        def loss(candidate):
            stats = candidate['result']['agreement']; table = stats['confusion']
            return stats['attempted'] - table['PASS']['PASS'] - table['FAIL']['FAIL']
        winner = min(fitting[backend]['candidates'], key=loss); selected[backend] = winner['config']
        if loss(winner) or winner['result']['agreement']['coverage'] != 1:
            raise RuntimeError('No fixture candidate meets exact-match/coverage control policy')
    write(directory / 'fitting.json', fitting)
    final_plan = {backend + '-' + name + '-final': candidate for backend in ['llm', 'jev']
                  for name, candidate in [('baseline', baselines[backend]), ('selected', selected[backend])]}
    campaign.freeze(final_plan)
    paths = {label: campaign.predict(label, candidate, 'final') for label, candidate in final_plan.items()}
    campaign.finish(); final = {label: campaign.compare(path) for label, path in paths.items()}
    for backend in ['llm', 'jev']:
        if final[backend + '-selected-final']['agreement']['observed_agreement_decided'] != 1:
            raise RuntimeError('Selected deterministic policy did not reproduce fixture labels')
    try: campaign.predict('forbidden-refit', selected['llm'], 'validation')
    except ValueError: refit_blocked = True
    else: raise RuntimeError('Consumed final evidence was reused for fitting')
    repeatability = {}; payload = public_input(campaign.rows()[0])
    if campaign.state['reserved_calls'] + 6 > campaign.state['worker_limit']:
        raise ValueError('No budget left for repetitions')
    campaign.state['reserved_calls'] += 6; campaign.save()
    for backend in ['llm', 'jev']:
        replies = []
        for _ in range(3):
            proc = subprocess.run([sys.executable, str(ROOT / 'judge_calibration/fixture_backend.py')],
                input=json.dumps({'input': payload, 'config': selected[backend]}), text=True, capture_output=True, timeout=5)
            campaign.state['worker_calls'] += 1; campaign.save()
            if proc.returncode: raise RuntimeError('Fixture repetition failed')
            replies.append(json.loads(proc.stdout))
        repeatability[backend] = {'source_items': 1, 'repetitions': 3,
            'identical': all(r == replies[0] for r in replies), 'raw_replies': replies,
            'limits': 'Deterministic fixture stability, not actual model consistency'}
    result = {'status': 'passed', 'authority': 'synthetic fixture labels, not human gold',
        'selected_configs': selected, 'final': final, 'repeatability': repeatability,
        'native_source_executions': 24, 'fixture_judge_processes': campaign.state['worker_calls'],
        'fixture_worker_budget': campaign.state['worker_limit'], 'final_refit_blocked': refit_blocked,
        'source_families': len({r['family'] for r in campaign.rows()}), 'provider_calls': 0, 'paid_model_calls': 0,
        'probability_calibrator_fit': False,
        'live_backend_status': {'Jev': 'unrun; native response shape simulated', 'LLM': 'unrun; native response shape simulated'},
        'promotion': 'offline mechanics only; no human calibration or production release',
        'scope': 'Bounded selection among predeclared deterministic policies/thresholds; not empirical prompt learning'}
    write(directory / 'selected-judge.fixture.json', {'selected': selected, 'deployable_live_judge': False,
                                                    'owner_release_policy': None, 'authority': result['authority']})
    write(directory / 'results.json', result)
    return result
