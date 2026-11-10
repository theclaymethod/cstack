"""Local serialized capture/merge driver; never executes candidates or providers."""
import argparse
import datetime
import hashlib
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent
SOURCE = OUT / 'source.md'
SESSION = 'controlled-scripted-capture'

def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def read_rows(name):
    path = OUT / name
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

def append(name, rows):
    existing = read_rows(name)
    identities = {row['record_id']: row for row in existing}
    added = []
    for row in rows:
        if row['record_id'] in identities:
            # Stable IDs encode source hash, output reference and assertion.
            continue
        row['captured_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with (OUT / name).open('a') as handle:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n')
        identities[row['record_id']] = row
        added.append(row['record_id'])
    return added

def record(identifier, turn, **fields):
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    return dict(record_id=identifier, session_id=SESSION,
                source={'path': 'source.md', 'sha256': digest, 'turn': turn,
                        'judgment_time': None, 'message_id': None},
                authority='scripted synthetic reviewer; no live expert endorsement', **fields)

def rubric(identifier, turn, words, question, passing, applicability, **fields):
    status = fields.pop('status_override', 'explicit scripted criterion normalized to binary')
    return record(identifier, turn, criterion_id=identifier, version=1,
                  revises=None, expert_words=words, question=question,
                  passing_answer=passing, applicability=applicability,
                  status=status, **fields)

WORDS2 = 'For that how-to request, opening a ticket is wrong. Give guidance and leave existing tickets unchanged.'
WORDS4 = 'That does not follow. An explicit ticket request for a clear account should create a ticket unless an open VPN ticket already exists for that account.'
WORDS6 = 'I have not decided the urgency policy.'
WORDS7 = "For an account-specific duplicate check, an unrelated account's ticket must not block the requested new ticket."

def initial():
    if not SOURCE.exists():
        shutil.copyfile(ROOT / 'exercises/fixtures/review-session.md', SOURCE)
    append('reviews.jsonl', [dict(record_id='prior-local-annotation',
        example_id='unrelated-local-prior', session_id='prior-seeded-local',
        authority='task-authorized synthetic seed', judgment='uncertain',
        expert_words=None, interpretation='An unrelated local layout concern remains unresolved.',
        input=None, reviewed_output=None, replay_ready=False,
        replay_blockers=['Synthetic unrelated seed; no reviewed artifact or expert verdict.'])])
    append('reviews.jsonl', [record('review-howto-v1', 2,
        example_id='narrative-howto', amends=None, capture_mode='expert-mode',
        judgment='incorrect', judgment_kind='correctness', expert_words=WORDS2,
        input={'request_description': 'VPN setup guide', 'exact_input': None, 'state': None},
        reviewed_output={'version': 'source.md:turn-1', 'verbatim_agent_description':
            'For request `VPN setup guide`, the assistant reports that it opened a ticket.',
            'exact_output': None, 'candidate_hash': None},
        correction={'behavior': 'Give guidance and leave existing tickets unchanged.',
                    'scope': 'The source turn-1 how-to request only', 'canonical_answer': None},
        interpretation='Scoped negative and partial behavioral correction, not a canonical replacement.',
        native_association={'receipt': 'native-baseline/traces.jsonl', 'status': 'unproven',
            'reason': 'Executed request differs from the narrative description; source has no run identifier, exact state or exact output.'},
        rubric_answers=[{'criterion_id': 'howto-guidance', 'version': 1,
                         'applicability': 'applies to described source how-to', 'answer': False, 'source_turn': 2}],
        replay_ready=False, replay_blockers=['Original exact narrative input/state/output/version unavailable.',
            'Cannot establish that the scripted reviewer saw native-baseline output.'])])
    append('rubric.jsonl', [rubric('howto-guidance', 2, WORDS2,
        'For the reviewed how-to request, does the response give guidance and leave existing tickets unchanged?',
        True, 'Source turn-1 how-to request; does not govern every VPN problem.'),
        rubric('urgency-unresolved', 6, WORDS6,
        'Should an urgent request bypass clarification?', None,
        'Urgent requests; thresholds and exceptions remain undecided.',
        status_override='proposed unresolved policy', interpretation='Question is an agent formulation; no reviewer decision or item-level answer.')])
    append('observations.jsonl', [record('urgency-observation', 6,
        example_id='urgency-policy', capture_mode='expert-mode', judgment='uncertain',
        expert_words=WORDS6, input=None, reviewed_output=None,
        agent_proposal='I suggest urgent requests should always bypass clarification.',
        proposal_endorsed=False, correction=None, criterion_id='urgency-unresolved',
        replay_ready=False, replay_blockers=['Policy unresolved; no exact reviewed item.'])])
    state = {'session_id': SESSION, 'expert_mode_active': True,
             'pending': ['Urgency policy', 'Exact narrative output association'], 'unsaved': []}
    write(OUT / 'session-state.json', state)
    checkpoint('first')

def stop():
    state = json.loads((OUT / 'session-state.json').read_text())
    state['expert_mode_active'] = False
    state['stopped_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(OUT / 'session-state.json', state)

def retrospective(name):
    assert json.loads((OUT / 'session-state.json').read_text())['expert_mode_active'] is False
    before = {file: len(read_rows(file)) for file in ['reviews.jsonl', 'rubric.jsonl', 'observations.jsonl', 'exclusions.jsonl']}
    append('reviews.jsonl', [record('review-howto-scope-amendment', 4,
        example_id='narrative-howto', amends='review-howto-v1', capture_mode='distill-me',
        judgment='incorrect', judgment_kind='scope clarification; original negative retained',
        expert_words=WORDS4, reviewed_output_reference='source.md:turn-1',
        interpretation='Clarifies distinction from explicit ticket requests; does not retract scoped how-to correction.',
        correction={'howto': 'Original turn-2 correction retained.',
                    'explicit_ticket': 'Create for a clear account unless its open VPN ticket already exists.'},
        rubric_answers=[], replay_ready=False,
        replay_blockers=['Original narrative input/output still missing; no invented execution link.'])])
    append('rubric.jsonl', [rubric('explicit-ticket-account', 4, WORDS4,
        'For an explicit ticket request for a clear account, does the response create a ticket unless an open VPN ticket already exists for that account?',
        True, 'Explicit ticket request; clear account; exception requires open VPN ticket for that account.'),
        rubric('duplicate-account-scope', 7, WORDS7,
        "Does an unrelated account's ticket avoid blocking the requested new ticket during an account-specific duplicate check?",
        True, 'Account-specific duplicate checks; not an independently judged output.')])
    append('exclusions.jsonl', [record('exclude-agent-generalization', 3,
        kind='unendorsed agent proposal explicitly rejected at turn 4',
        words='Then every VPN problem should get guidance only.',
        expected_answer=False, rejection_source_turn=4),
        record('exclude-urgent-bypass', 5, kind='unendorsed agent suggestion',
        words='I suggest urgent requests should always bypass clarification.',
        expected_answer=False, unresolved_source_turn=6)])
    # Verify every existing row survives and duplicate identities are absent.
    after = {}
    for file in before:
        rows = read_rows(file)
        assert len({row['record_id'] for row in rows}) == len(rows)
        after[file] = len(rows)
    write(OUT / (name + '-merge-receipt.json'), {'mode_before': False, 'mode_after': False,
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'counts_before': before, 'counts_after': after,
        'added': {file: after[file]-before[file] for file in before},
        'dedup_key': 'stable record IDs for source identity, output version, and specific assertion'})
    checkpoint(name)

def checkpoint(name):
    path = OUT / 'checkpoints' / name
    path.mkdir(parents=True, exist_ok=True)
    for file in ['reviews.jsonl', 'rubric.jsonl', 'observations.jsonl', 'exclusions.jsonl', 'session-state.json']:
        if (OUT / file).exists():
            shutil.copyfile(OUT / file, path / file)
    hashes = {file.name: hashlib.sha256(file.read_bytes()).hexdigest() for file in path.iterdir() if file.name != 'hashes.json'}
    write(path / 'hashes.json', hashes)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['initial', 'stop', 'merge1', 'merge2'])
    phase = parser.parse_args().phase
    if phase == 'initial': initial()
    elif phase == 'stop': stop()
    else: retrospective(phase)
