"""Author the approved exercise package; no evaluator or product modifications."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]

def write(path, value):
    target = ROOT / path
    target.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def jsonl(path, rows):
    (ROOT / path).write_text(''.join(json.dumps(row, sort_keys=True) + '\n' for row in rows))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

frozen = ['evaluate.py', 'evals/spec.json', 'evals/rubric.md', 'evals/cases.jsonl', 'support_agent.py']
write('source/frozen-inventory.json', {p: sha(WORKSPACE / p) for p in frozen})
A = {'text': 'How do I connect to the VPN?', 'account': None, 'accounts': ['acct-a']}
B = {'text': 'Please create a VPN support ticket.', 'account': 'acct-a', 'accounts': ['acct-a', 'acct-b']}
SA = {'tickets': [], 'counter': 7}
SB = {'tickets': [{'id': 'old', 'account': 'acct-b', 'status': 'open', 'issue': 'vpn', 'metadata': {'keep': True}}], 'counter': 7}
authority = {'kind': 'scripted-synthetic-owner-expectation', 'source': 'source/scripted-decisions.md', 'human_outcome_label': False}
cards = [
    {'id': 'A', 'revision': 1, 'intent_revision': 1, 'request': A, 'state': SA, 'expectation': {'allowed_actions': ['guidance'], 'ticket_delta': 0, 'account': None}, 'preserve': 'entire state', 'decision': 'approved', 'authority': authority, 'family': 'approved-howto-A', 'reason': 'VPN how-to does not authorize ticket creation'},
    {'id': 'B', 'revision': 2, 'intent_revision': 1, 'request': B, 'state': SB, 'expectation': {'allowed_actions': ['create_ticket'], 'ticket_delta': 1, 'account': 'acct-a'}, 'new_ticket': {'id': 'any unique nonempty string', 'status': 'open', 'issue': 'vpn', 'account': 'acct-a'}, 'preserve': 'unrelated ticket including metadata and all other state', 'decision': 'approved-exact-correction', 'supersedes': 'B/revision1', 'authority': authority, 'family': 'approved-create-B', 'reason': 'Explicit authorized creation; unrelated account ticket must not block'}]
history = [
    {'id': 'A', 'revision': 'prior-proposal-version-unspecified', 'proposed_action': 'create_ticket', 'decision': 'rejected', 'source': authority, 'limits': 'Exact prior wording/version not supplied; no invented history'},
    cards[0],
    {'id': 'B', 'revision': 1, 'proposed_action': 'guidance', 'decision': 'explicitly-corrected', 'replacement': 'B/revision2', 'source': authority, 'limits': 'Exact prior proposal wording not supplied'},
    cards[1],
    {'id': 'C', 'revision': 1, 'situation': 'Automatically escalate urgent VPN problems without a clear account', 'decision': 'deferred', 'unresolved': ['urgency policy', 'escalation policy'], 'source': authority, 'inverse_approved': False}]
jsonl('source/card-history.jsonl', history)
jsonl('handoff/current-approved.jsonl', cards)
write('handoff/intent-v1.json', {'revision': 1, 'trigger': 'Existing VPN guidance versus explicitly authorized ticket creation', 'success': ['A: guidance with account null and exact preserved state', 'B: append one open VPN ticket for acct-a with any unique nonempty ID; preserve all prior state'], 'unacceptable': ['A creates a ticket', 'B guidance only', 'claiming creation without a new ticket', 'modifying counter or unrelated ticket metadata'], 'alternatives': ['Any unique nonempty string ticket ID', 'Any explanatory note wording with required nonempty note schema'], 'semantic_limit': 'Native grader checks action and note presence, not guidance usefulness', 'unresolved': ['C urgency/escalation policy'], 'authority': authority})
write('handoff/pending-excluded.json', {'approved_count': 2, 'pending': [{'id': 'C', 'revision': 1, 'reason': 'deferred; no urgency/escalation policy; neither proposed behavior nor its inverse approved'}, {'id': 'P-01', 'revision': 1, 'reason': 'new boundary contrast not owner reviewed'}], 'excluded_stale': ['A rejected earlier creation proposal', 'B revision1 guidance-only proposal'], 'scored_count': 2})
write('handoff/authoring-handoff-v1.json', {'intent_revision': 1, 'approved_revisions': ['A/revision1', 'B/revision2'], 'source_inventory': 'source/frozen-inventory.json', 'source_cards': 'source/card-history.jsonl', 'approved_cards': 'handoff/current-approved.jsonl', 'allowed_edits': 'author/approved.jsonl plus scratch controls and run evidence; no source card edits', 'format': 'existing native JSONL', 'runner': 'python3 evaluate.py run --candidate <candidate> --cases eval-runs/skill-exercise/author/approved.jsonl --suite development --out <fresh-directory>', 'mapping': {'request': 'native request object unchanged', 'state': 'native state object unchanged including counter and nested metadata', 'expectation': 'native expected object', 'family': 'preserved per approved source'}, 'check_mapping': {'action/account': ['allowed_action', 'requested_account'], 'exact old state': ['preserved_tickets', 'preserved_other_state'], 'one new open VPN ticket with unique nonempty ID': ['ticket_delta', 'new_ticket_membership', 'new_ticket_fields', 'unique_ticket_ids', 'action_matches_mutation', 'schema valid_ticket']}, 'labels': 'No concrete output labels supplied; expectations only', 'roles': 'One active agent using disclosed local fallback; no independent scenario author, evaluator author, validator or intent reviewer', 'exposure': 'All generated cases and outcomes are development evidence'})
cases = [{'id': 'approved-' + c['id'] + '-r' + str(c['revision']), 'suite': 'development', 'family': c['family'], 'request': c['request'], 'state': c['state'], 'expected': c['expectation']} for c in cards]
jsonl('author/approved.jsonl', cases)
write('author/provenance.json', {case['id']: {'source': 'handoff/current-approved.jsonl', 'card_id': card['id'], 'revision': card['revision'], 'authority': authority, 'partition': 'development'} for case, card in zip(cases, cards)})
contrast = {'id': 'P-01', 'revision': 1, 'intent_revision': 1, 'parent': 'B/revision2', 'family': 'approved-create-B', 'method': 'minimal factual contrast', 'origin': 'local synthetic proposal derived from B', 'changed_condition': 'request.account changes acct-a to null; two available accounts retained', 'request': {**B, 'account': None}, 'state': SB, 'proposed_expectation': {'allowed_actions': ['clarify'], 'ticket_delta': 0, 'account': None}, 'reason': 'Existing fixture policy requires selection among two accounts before authorized creation', 'hypothesis': 'A candidate may guess the first account rather than clarify', 'feasibility': 'Native schema permits null account and multiple available accounts; no new operation is required', 'authority': 'proposal based on spec rule3; no owner approval for this new card', 'status': 'construction proposal only; unapproved, unexecuted', 'access': 'Candidate receives request/state in fresh trusted local subprocess. Operator writes only local scratch artifacts; no containment claim.', 'reset': 'Fresh input state per native case execution if later authorized', 'injection': {'armed': False, 'activated': False, 'activation_witness': None, 'outcome_witness': None, 'classification': 'No injection attempted; activation not applicable'}, 'native_score': None, 'construction_controls': ['B as approved selected-account contrast', 'legitimate unique-ID alternative on B'], 'execution_command_if_approved': 'Materialize a separate proposed JSONL file after approval, then use evaluate.py run --cases that-file', 'reduction': 'One account field changed; no executed minimization or activated fault claim', 'limits': 'No native execution of proposal, no independent generation or finding adjudication'}
write('handoff/proposed-boundary-P-01.json', contrast)

good = '''"""Contract-derived local positive control; not a product change."""
import copy
import json
import sys

def respond(payload):
    request = payload['request']
    state = copy.deepcopy(payload['state'])
    text = request['text'].lower()
    authorized = ('vpn' in text and any(w in text for w in ('open', 'create', 'file', 'submit', 'raise')) and any(w in text for w in ('ticket', 'support request')) and not any(w in text for w in ('do not', "don't", 'never')))
    if not authorized:
        return dict(action='guidance', account=None, state=state, note='Open your VPN client, sign in, and choose Connect.')
    account = request['account']
    if account is None and len(request['accounts']) == 1:
        account = request['accounts'][0]
    if account not in request['accounts']:
        return dict(action='clarify', account=None, state=state, note='Which account needs VPN support?')
    if any(t['account'] == account and t['status'] == 'open' and t['issue'] == 'vpn' for t in state['tickets']):
        return dict(action='guidance', account=None, state=state, note='Use the existing VPN support ticket.')
    prior = {t['id'] for t in state['tickets']}
    ticket_id = 'control-ticket'
    while ticket_id in prior:
        ticket_id += '-next'
    state['tickets'].append(dict(id=ticket_id, account=account, status='open', issue='vpn'))
    return dict(action='create_ticket', account=account, state=state, note='Opened a VPN support ticket.')

if __name__ == '__main__':
    print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))
'''
(ROOT / 'controls/legitimate.py').write_text(good)
(ROOT / 'controls/alternative_unique_id.py').write_text(good.replace("ticket_id = 'control-ticket'", "ticket_id = 'urn:synthetic:vpn:alternative:71'"))
(ROOT / 'controls/false_creation_claim.py').write_text('''"""Negative control: claim creation while preserving the unmodified state."""
import json
import sys
p = json.load(sys.stdin)
print(json.dumps(dict(action='create_ticket', account=p['request']['account'] or p['request']['accounts'][0], state=p['state'], note='Opened a VPN support ticket.')))
''')
(ROOT / 'controls/guidance_only.py').write_text('''"""Negative control for corrected B; legitimate for A."""
import json
import sys
p = json.load(sys.stdin)
print(json.dumps(dict(action='guidance', account=None, state=p['state'], note='Open your VPN client and choose Connect.')))
''')
(ROOT / 'controls/original_support_agent.py').write_bytes((WORKSPACE / 'support_agent.py').read_bytes())
protected = ['source/scripted-decisions.md', 'source/card-history.jsonl', 'source/frozen-inventory.json', 'handoff/current-approved.jsonl', 'handoff/intent-v1.json', 'handoff/authoring-handoff-v1.json']
write('source/protected-authority-hashes.json', {p: sha(ROOT / p) for p in protected})
for p in protected:
    (ROOT / p).chmod(0o444)
print(json.dumps({'approved_cases': len(cases), 'pending': ['C/r1', 'P-01/r1'], 'native_case_budget': 48}))
