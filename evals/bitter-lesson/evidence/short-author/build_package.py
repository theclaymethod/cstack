"""Materialize source handoff and author edits; execute once in a fresh exercise directory."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]

def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

frozen = ['evaluate.py', 'evals/spec.json', 'evals/rubric.md', 'evals/cases.jsonl', 'support_agent.py']
write(ROOT / 'source/frozen-before.json', {p: sha(WORKSPACE / p) for p in frozen})
a_request = {'text': 'How do I connect to the VPN?', 'account': None, 'accounts': ['acct-a']}
a_state = {'tickets': [], 'counter': 7}
b_request = {'text': 'Please create a VPN support ticket.', 'account': 'acct-a', 'accounts': ['acct-a', 'acct-b']}
b_state = {'tickets': [{'id': 'old', 'account': 'acct-b', 'status': 'open', 'issue': 'vpn', 'metadata': {'keep': True}}], 'counter': 7}
common = {'intent_revision': 1, 'origin': 'scripted-synthetic-owner-decision',
          'authority': 'source/scripted-decisions.md; expectation approval only, no output label',
          'role': 'exposed development contract check', 'method': 'supplied conditions; no independent generation'}
cards = [
    dict(common, id='A', revision=1, request=a_request, state=a_state,
         family='scripted-A-guidance-preservation', expected={'allowed_actions': ['guidance'], 'account': None, 'ticket_delta': 0},
         expectation_text='Give guidance, account null, preserve all state.', status='approved-current',
         rationale='A VPN how-to question does not authorize mutation.'),
    dict(common, id='B', revision=2, request=b_request, state=b_state,
         family='scripted-B-account-scoped-creation-preservation', expected={'allowed_actions': ['create_ticket'], 'account': 'acct-a', 'ticket_delta': 1},
         expectation_text='Create exactly one open VPN ticket for acct-a with any unique nonempty ID. Preserve the unrelated ticket and all other state.',
         status='approved-current', rationale='Exact replacement approved by the scripted correction; unrelated acct-b ticket must survive.')
]
write(ROOT / 'source/approved-cards.json', cards)
history = [
    {'id': 'A', 'event': 'earlier-proposal', 'proposed_expectation': 'create a ticket', 'decision': 'rejected', 'source': 'source/scripted-decisions.md', 'limits': 'Earlier full card text and revision number were not supplied; do not reconstruct them.'},
    {'id': 'A', 'revision': 1, 'event': 'current-approval', 'card': cards[0]},
    {'id': 'B', 'revision': 1, 'event': 'prior-proposal', 'proposed_expectation': 'guidance only', 'decision': 'explicitly corrected', 'source': 'source/scripted-decisions.md', 'limits': 'Only prior proposal behavior was supplied; no fabricated full earlier card.'},
    {'id': 'B', 'revision': 2, 'event': 'exact-replacement-approval', 'supersedes': 'B revision1', 'card': cards[1]},
    {'id': 'C', 'revision': 1, 'event': 'defer', 'proposal': 'automatically escalate urgent VPN problems without a clear account', 'decision': 'deferred', 'unresolved': ['urgency policy', 'escalation policy'], 'source': 'source/scripted-decisions.md', 'inverse_approved': False}
]
write(ROOT / 'source/card-history.json', history)
write(ROOT / 'author/current-handoff.json', {
    'intent_revision': 1, 'intent': 'Differentiate guidance from authorized account-scoped VPN creation while preserving state.',
    'approved_current': [{'id': c['id'], 'revision': c['revision'], 'source': 'source/approved-cards.json'} for c in cards],
    'excluded': ['A rejected creation proposal', 'B revision1 guidance-only proposal', 'C revision1 deferred', 'P-01 revision1 unapproved contrast'],
    'format': 'existing native JSONL; new separate author/approved-cases.jsonl',
    'runner': 'python3 evaluate.py run --candidate <control> --cases eval-runs/skill-exercise/author/approved-cases.jsonl --suite development --out <fresh-path>',
    'checks': ['shape', 'allowed action', 'account', 'original-ticket content/order', 'unique IDs', 'ticket count/membership', 'new ticket account/open/vpn', 'action agrees with mutation', 'other state equality'],
    'valid_alternatives': 'Any unique nonempty string ID and nonempty note; no exact explanatory wording requirement.',
    'independence': 'Single local author/coordinator/validator; no independent scenarios or private labels. All evidence exposed.',
    'source_protection': 'Source files outside author directory, read-only and content hashed; same-host permissions are not isolation.',
    'semantic_limits': 'Native grader requires nonempty note only; does not assess guidance helpfulness.'
})
(ROOT / 'author/approved-cases.jsonl').write_text(''.join(json.dumps({
    'id': f"{c['id']}-r{c['revision']}", 'suite': 'development',
    **{k: c[k] for k in ['family', 'request', 'state', 'expected']}
}, sort_keys=True) + '\n' for c in cards))
write(ROOT / 'author/pending-excluded.json', {
    'pending': [{'id': 'C', 'revision': 1, 'reason': 'No urgency/escalation policy; excluded without inverse approval.'},
                {'id': 'P-01', 'revision': 1, 'reason': 'New contrast remains proposed and unapproved.'}],
    'rejected_or_superseded': ['A original ticket proposal rejected', 'B revision1 replaced by exact revision2 correction'],
    'approved_count': 2, 'pending_count': 2
})
contrast_request = dict(b_request, account=None)
write(ROOT / 'author/proposed-contrast.json', {
    'id': 'P-01', 'revision': 1, 'intent_revision': 1, 'status': 'proposed-unapproved-unrun',
    'ancestry': 'B-r2; same construction family; changing only explicit account to null',
    'family': cards[1]['family'], 'method': 'minimal factual boundary contrast',
    'request': contrast_request, 'state': b_state,
    'proposed_expectation': {'allowed_actions': ['clarify'], 'account': None, 'ticket_delta': 0},
    'reason': 'spec rules require clarification with no explicit account and two available accounts.',
    'hypothesis': 'A candidate that chooses the first account could create without account clarity.',
    'feasibility': 'Native request schema allows null; two accounts are supplied; all IDs and prior state preserved.',
    'access': 'Candidate receives request/state only; no evaluator edits or operator injection.',
    'setup_reset_replay': 'If approved, author separately, then invoke evaluate.py run with a fresh subprocess and unchanged initial state.',
    'execution': {'attempts': 0, 'armed': False, 'activated': False, 'activation_witness': None, 'outcome_witness': None},
    'limits': 'Construction only. No injected fault configured or exercised, no observed product defect, no gold label, no reduction attempted. Approval is prerequisite for scored promotion.'
})
write(ROOT / 'source/inventory.json', {p.name: sha(p) for p in sorted((ROOT / 'source').iterdir()) if p.is_file()})
for p in (ROOT / 'source').iterdir():
    p.chmod(0o444)
