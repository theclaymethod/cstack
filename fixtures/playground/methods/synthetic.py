"""Bounded structured generation, reachable replay, shrinking and defect selection."""
import copy
from pathlib import Path
from .native import ROOT, Runs, evaluate, jsonl, write


# Independent contract model over structured facts; text is rendered afterwards.
def case_for(name, intent, account=None, accounts=('acct-a',), tickets=()):
    state = {'tickets': copy.deepcopy(list(tickets))}
    selected = account if account is not None else (accounts[0] if len(accounts) == 1 else None)
    if intent == 'guidance':
        expected = {'allowed_actions': ['guidance'], 'account': None, 'ticket_delta': 0}
    elif intent != 'create':
        expected = {'allowed_actions': ['guidance', 'clarify'], 'account': None, 'ticket_delta': 0}
    elif selected is None or selected not in accounts:
        expected = {'allowed_actions': ['clarify'], 'account': None, 'ticket_delta': 0}
    elif any(t['account'] == selected and t['status'] == 'open' and t['issue'] == 'vpn' for t in tickets):
        expected = {'allowed_actions': ['guidance', 'clarify'], 'account': None, 'ticket_delta': 0}
    else:
        expected = {'allowed_actions': ['create_ticket'], 'account': selected, 'ticket_delta': 1}
    text = {'create': 'Please create a VPN support ticket.',
            'deny': 'Do not create a VPN support ticket.',
            'guidance': 'How do I connect to the VPN?'}[intent]
    return {'id': name, 'suite': 'development', 'family': name.split(':')[0],
            'request': {'text': text, 'account': account, 'accounts': list(accounts)},
            'state': state, 'expected': expected}


def ticket(name, account, status='open'):
    return {'id': name, 'account': account, 'status': status, 'issue': 'vpn'}


def seed_cases():
    return [case_for('authorization:create', 'create'), case_for('authorization:deny', 'deny'),
            case_for('authorization:guidance', 'guidance'),
            case_for('account:ambiguous', 'create', accounts=('acct-a', 'acct-b')),
            case_for('account:unavailable', 'create', account='missing'),
            case_for('scope:other-account', 'create', tickets=[ticket('unrelated', 'acct-b')]),
            case_for('scope:closed', 'create', tickets=[ticket('closed', 'acct-a', 'closed')])]


def candidate_catalog(directory):
    """Frozen, explicit defect operators; no evaluator mutations."""
    code = (ROOT / 'examples/candidates/improved.py').read_text()
    own = code.replace('and ticket["issue"] == "vpn" for ticket in state["tickets"]',
                       'and ticket["issue"] == "vpn" and ticket.get("created_by") != "fixture-agent" for ticket in state["tickets"]')
    own = own.replace('"status": "open", "issue": "vpn"})',
                      '"status": "open", "issue": "vpn", "created_by": "fixture-agent"})')
    denial = code.replace('or not authorized or denied:', 'or not authorized:')
    if own == code or denial == code or 'created_by' not in own:
        raise RuntimeError('Candidate source changed; inspect defect operators before reuse')
    paths = {'ignore-own-created': directory / 'ignore-own-created.py',
             'ignore-denial': directory / 'ignore-denial.py',
             'broad-duplicate': ROOT / 'examples/candidates/regression.py'}
    paths['ignore-own-created'].write_text(own)
    paths['ignore-denial'].write_text(denial)
    return paths


def sequence(runs, candidate, name, initial_tickets=()):
    """Advance only from a fully native-valid actual output; retain failed steps."""
    current = copy.deepcopy(list(initial_tickets))
    steps = []
    for index in range(2):
        case = case_for('sequence:create-repeat-' + name + '-' + str(index), 'create', tickets=current)
        trace = runs.run(name + '-step-' + str(index), candidate, [case])[0]
        steps.append({'case': case, 'trace': trace})
        if trace['outcome'] != 'PASS':
            break  # A bad predecessor never becomes an implicitly valid next input.
        current = copy.deepcopy(trace['output']['state']['tickets'])
    return steps


def reduce_sequence(runs, candidate):
    """Remove records/steps only when actual valid-prefix duplicate creation remains."""
    attempts = []
    retained = None
    noise_b, noise_c = ticket('noise-b', 'acct-b', 'closed'), ticket('noise-c', 'acct-c', 'closed')
    for label, initial in [('rich', [noise_b, noise_c]), ('drop-noise-b', [noise_c]), ('drop-noise-c', [])]:
        steps = sequence(runs, candidate, 'reduce-' + label, initial)
        witness = (len(steps) == 2 and steps[0]['trace']['outcome'] == 'PASS'
                   and steps[1]['trace']['outcome'] == 'FAIL'
                   and not steps[1]['trace']['checks']['ticket_delta']
                   and steps[1]['trace']['checks']['preserved_tickets'])
        attempts.append({'revision': label, 'retained': witness, 'steps': steps})
        controls = sequence(runs, ROOT / 'examples/candidates/improved.py', 'control-' + label, initial)
        if len(controls) != 2 or any(step['trace']['outcome'] != 'PASS' for step in controls):
            raise RuntimeError('Reduction lost a legitimate sequence control')
        attempts[-1]['legitimate_controls'] = controls
        if witness:
            retained = steps
    fresh = case_for('sequence:remove-predecessor', 'create')
    removed_prefix = {'case': fresh, 'trace': runs.run('reduce-prefix-control', candidate, [fresh])[0]}
    attempts.append({'revision': 'remove-creation-predecessor', 'retained': False,
                     'reason': 'One fresh creation passes; duplicate mechanism needs the predecessor',
                     'step': removed_prefix})
    if retained is None:
        raise RuntimeError('No stable duplicate mechanism to reduce')
    return {'status': 'reduced-within-declared-structured-search', 'attempts': attempts,
            'global_minimality_claimed': False, 'family': 'sequence'}


def partition(records):
    """Connected ancestry and exact input identity stay in one development partition."""
    components = []
    for row in records:
        case, metadata = row['case'], row['metadata']
        keys = {'family:' + case['family'], 'input:' + evaluate.json_hash({'request': case['request'], 'state': case['state']})}
        keys.update('ancestor:' + x for x in metadata['ancestors'])
        overlaps = [group for group in components if group['keys'] & keys]
        merged = {'keys': set(keys), 'rows': [row]}
        for group in overlaps:
            merged['keys'].update(group['keys']); merged['rows'].extend(group['rows']); components.remove(group)
        components.append(merged)
    if len(components) < 2:
        raise ValueError('Need at least two independent construction components for a development split')
    result = {'train': [], 'validation': []}
    for index, group in enumerate(sorted(components, key=lambda g: min(g['keys']))):
        result['train' if index % 2 == 0 else 'validation'].extend(group['rows'])
    return result


def run(directory, limit=300):
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=False)
    runs = Runs(directory / 'native', limit)
    catalog = candidate_catalog(directory)
    good = ROOT / 'examples/candidates/improved.py'
    original = evaluate.load_cases('all')
    generated = seed_cases()
    good_static = runs.run('conforming-generated', good, generated)
    if any(row['outcome'] != 'PASS' for row in good_static):
        raise RuntimeError('Generated contract or conforming control disagrees')
    sequence_results = {'conforming': sequence(runs, good, 'conforming')}
    for name, candidate in catalog.items():
        sequence_results[name] = sequence(runs, candidate, name)
    # A conforming trace establishes reachable inputs, but never supplies arbitrary gold outputs.
    generated.extend(step['case'] for step in sequence_results['conforming'])
    matrix = {}
    for name, candidate in catalog.items():
        before = runs.run('seeds-' + name, candidate, original)
        matrix[name] = {'seed_failures': [t['id'] for t in before if t['outcome'] == 'FAIL'],
                        'seed_executions': len(before),
                        'errors': [t['id'] for t in before if t['outcome'] == 'ERROR']}
    # The stateful operator marks its own prior output. The corresponding reachable second
    # step is candidate-specific, so replayed sequence failures are recorded separately.
    sequence_new = sequence_results['ignore-own-created']
    if (matrix['ignore-own-created']['seed_failures'] or matrix['ignore-own-created']['errors']
            or len(sequence_new) != 2 or sequence_new[-1]['trace']['outcome'] != 'FAIL'):
        raise RuntimeError('Stateful pilot failed to isolate additional declared sequence defect')
    reduction = reduce_sequence(runs, catalog['ignore-own-created'])
    # Retain the valid-prefix second input from the faulty candidate: its first step passed.
    candidate_case = copy.deepcopy(sequence_new[-1]['case'])
    candidate_case['id'] = 'sequence:own-created-repeat'
    candidate_control = runs.run('conforming-own-created-repeat', good, [candidate_case])[0]
    if candidate_control['outcome'] != 'PASS':
        raise RuntimeError('Sequence-derived witness rejected by conforming control')
    generated.append(candidate_case)
    if len(generated) > len(original):
        raise RuntimeError('Generated comparison corpus exceeds the declared per-arm case limit')
    # Refresh the matrix on the complete fixed corpus, including this reachable witness.
    vectors = {}
    for name, candidate in catalog.items():
        traces = runs.run('selected-corpus-' + name, candidate, generated)
        vectors[name] = {t['id'] for t in traces if t['outcome'] == 'FAIL'}
        matrix[name]['generated_failures'] = sorted(vectors[name])
        matrix[name]['generated_executions'] = len(traces)
        if any(t['outcome'] == 'ERROR' for t in traces):
            raise RuntimeError('Invalid mutant cannot count as detected behavior')
    uncovered = set(vectors); selected = []
    while uncovered:
        case_id = max(sorted(c['id'] for c in generated), key=lambda cid: sum(cid in vectors[n] for n in uncovered))
        caught = {name for name in uncovered if case_id in vectors[name]}
        if not caught:
            break
        selected.append(case_id); uncovered -= caught
    records = [{'case': c, 'metadata': {'label_status': 'fixture-contract-derived',
                'authority': 'evals/spec.json + evals/rubric.md; not human labels',
                'method': 'reachable-sequence' if c['family'] == 'sequence' else 'structured-contrast',
                'ancestors': [c['family']], 'input_hash': evaluate.json_hash({'request': c['request'], 'state': c['state']}),
                'generator_sha256': evaluate.digest(Path(__file__)),
                'source_identity': evaluate.identity()['files'], 'exposure': 'exposed-synthetic-development'}} for c in generated]
    splits = partition(records)
    jsonl(directory / 'cases.jsonl', generated)
    jsonl(directory / 'records.jsonl', records)
    write(directory / 'splits.json', splits)
    result = {'status': 'passed', 'sequence_results': sequence_results, 'reduction': reduction,
              'matrix': matrix, 'complete_detection_matrix': {n: sorted(v) for n, v in vectors.items()},
              'selected_case_ids': selected, 'surviving_mutants': sorted(uncovered),
              'additional_mechanism': 'ignore-own-created passes static seeds; valid-prefix repeat exposes duplicate creation',
              'selection_limit': 'Declared synthetic fault catalog; no independent held-out mechanism or production claim',
              'comparison': {'seed_cases_per_candidate': len(original), 'final_generated_cases_per_candidate': len(generated),
                             'per_arm_case_limit': len(original), 'adaptive_exposure': 'All selection cases exposed',
                             'scope': 'One frozen corpus run per candidate per arm. Construction/reduction/selection work is separately included in the total; no generation efficiency or unseen improvement claim.'},
              'actual_native_executions': sum(c.get('executed', 0) for c in runs.calls),
              'budget': limit, 'provider_calls': 0}
    if uncovered:
        raise RuntimeError('Declared fault catalog has unaccounted survivors')
    write(directory / 'results.json', result)
    return result
