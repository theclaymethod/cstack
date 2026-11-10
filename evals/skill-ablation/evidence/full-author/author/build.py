"""Rebuild approved native cases and local standalone controls from frozen handoff."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
handoff = json.loads((ROOT / 'handoff/current.json').read_text())
cases = []
links = []
for card in handoff['approved']:
    expected = card['expectation']
    case = {'id': f"{card['id']}-r{card['revision']}", 'suite': 'development',
            'family': card['family'], 'request': card['request'], 'state': card['state'],
            'expected': {'allowed_actions': [expected['action']],
                         'account': expected['account'], 'ticket_delta': expected['ticket_delta']}}
    cases.append(case)
    links.append({'case_id': case['id'], 'approved_card': f"{card['id']}:r{card['revision']}",
                  'source': 'source/current-approved-cards.json', 'intent_revision': card['intent_revision'],
                  'fidelity': 'exact request, account, account list, complete state, family and approved expected action/account/delta',
                  'preservation_and_new_ticket_checks': 'existing evaluate.py grade; no grader modifications',
                  'authority': 'scripted synthetic expectation requirement, no concrete human outcome label',
                  'partition': 'development'})
(ROOT / 'author/approved.jsonl').write_text(''.join(json.dumps(c,sort_keys=True)+'\n' for c in cases))
(ROOT / 'author/source-map.json').write_text(json.dumps(links,indent=2)+'\n')
clean = (WORKSPACE / 'examples/candidates/improved.py').read_text()
(ROOT / 'controls/clean.py').write_text(clean)
(ROOT / 'controls/alternate-id.py').write_text(clean.replace('f"ticket-{sequence}"','f"allowed-alternative-{sequence}"'))
false_claim = clean.replace('    state["tickets"].append({"id": f"ticket-{sequence}", "account": account,\n                             "status": "open", "issue": "vpn"})\n','')
(ROOT / 'controls/false-creation-claim.py').write_text(false_claim)
(ROOT / 'controls/original-product.py').write_text((WORKSPACE / 'support_agent.py').read_text())
base = copy.deepcopy(cases[1])
changed = copy.deepcopy(base)
changed['id'] = 'proposed-B-account-null'
changed['request']['account'] = None
changed['expected'] = {'allowed_actions':['clarify'],'ticket_delta':0,'account':None}
proposal = {'id':'contrast-account-selection','revision':1,'status':'proposed-unapproved-unexecuted',
    'intent_revision':1,'source':'B:r2 plus synthetic one-field transformation',
    'family':base['family'],'construction_method':'minimal factual contrast; remove explicit account only',
    'hypothesis':'A candidate may guess the first account when several are available.',
    'baseline_approved_case':base,'proposed_changed_case':changed,
    'proposed_expectation':'Clarify with account null and preserve entire state; derived from synthetic existing spec, awaiting scoped approval.',
    'authority':'construction proposal only; no expectation approval and no human outcome label',
    'feasibility':'Both accounts listed, existing ticket for acct-b, no explicit account after change; native schema supports this state.',
    'candidate_access':'Local standalone candidate via evaluate.py; host permissions, fresh subprocess per case; no sandbox claim.',
    'operator_access':'No instrumentation or fault injection used. Core evaluator/spec/rubric/cases protected by scope and hashes, not enforced security.',
    'perturbation':{'kind':'proposed request.account removal','injection':'none','armed':False,'activated':False,'activation_witness':None},
    'execution':{'status':'unrun','case_executions':0,'native_score':None,'observed_outcome':None,'setup_if_approved':'Put separately approved changed case in its own native JSONL and use evaluate.py run --cases; fresh input reset per case.'},
    'controls':'Executed approved B clean and allowed-ID controls exist; changed condition itself has no execution evidence.',
    'minimization':'Constructed one-field contrast; no executed reduction or fault minimization claimed.',
    'limits':['Not in approved authoring package','No independent scenario author or intent reviewer','No injected fault armed or activated; no recovery/failure claim','New case shares B development family; not independent coverage']}
(ROOT / 'proposals/boundary-contrast.json').write_text(json.dumps(proposal,indent=2,sort_keys=True)+'\n')
print('Authored exactly A:r1 and B:r2; wrote four local control candidates and one excluded proposal.')
