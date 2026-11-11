"""Recover scripted requirements before authoring; writes source records only."""
import copy, hashlib, json
from pathlib import Path
root = Path(__file__).resolve().parent
source = root / 'source'
def put(name, obj):
    (source / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')
def lines(name, rows):
    (source / name).write_text(''.join(json.dumps(x, sort_keys=True)+'\n' for x in rows))
a = {'text':'How do I connect to the VPN?','account':None,'accounts':['acct-a']}
b = {'text':'Please create a VPN support ticket.','account':'acct-a','accounts':['acct-a','acct-b']}
s_a = {'tickets':[], 'counter':7}
s_b = {'tickets':[{'id':'old','account':'acct-b','status':'open','issue':'vpn','metadata':{'keep':True}}], 'counter':7}
cards = [
 {'id':'A','revision':0,'request':a,'state':s_a,'proposed_behavior':'create a ticket','status':'rejected','source_phrase':'An original proposal to create a ticket was rejected.','history_limit':'Original proposal wording/revision number unspecified; local revision0 records its known meaning only.'},
 {'id':'A','revision':1,'request':a,'state':s_a,'expected':{'allowed_actions':['guidance'],'account':None,'ticket_delta':0},'preserve':'entire state exactly','status':'approved-current','supersedes':'A:0'},
 {'id':'B','revision':1,'request':b,'state':s_b,'proposed_behavior':'guidance only','status':'corrected-superseded','source_phrase':'The prior guidance-only proposal was explicitly corrected','history_limit':'Earlier proposal exact wording and context not separately supplied; request/state are recovered from current exact card, not independently approved earlier facts.'},
 {'id':'B','revision':2,'request':b,'state':s_b,'expected':{'allowed_actions':['create_ticket'],'account':'acct-a','ticket_delta':1},'new_ticket':{'id':'any unique nonempty string','account':'acct-a','status':'open','issue':'vpn'},'preserve':'unrelated ticket including metadata, original ordering, and every other state field exactly','status':'approved-current','supersedes':'B:1'},
 {'id':'C','revision':1,'proposal':'automatically escalate urgent VPN problems without a clear account','status':'deferred','unresolved':['urgency policy','escalation policy'],'expected':None}
]
for card in cards:
    card.update(intent_revision=1, origin='scripted synthetic owner decision supplied by task', source='original-scripted-decisions.md', family=('approved-vpn-authorization-contrast' if card['id'] in ['A','B'] else 'unresolved-urgent-vpn'))
lines('card-history.jsonl', cards)
decisions = [
 {'card':'A','revision':0,'type':'expectation','decision':'reject','scope':'ticket-creation proposal; rejection alone does not approve inverse'},
 {'card':'A','revision':1,'type':'expectation','decision':'approve','scope':'exact supplied request/state and guidance/null/no-mutation behavior'},
 {'card':'B','revision':1,'type':'expectation','decision':'correct','replacement':'B:2'},
 {'card':'B','revision':2,'type':'expectation','decision':'approve-exact-correction','scope':'exact replacement; unique nonempty IDs allowed'},
 {'card':'C','revision':1,'type':'expectation','decision':'defer','scope':'no urgency or escalation policy decided'}
]
for d in decisions:
    d.update(authority='scripted synthetic owner approval, not live human gold', source='original-scripted-decisions.md', concrete_output_reviewed=False)
lines('decisions.jsonl', decisions)
current = [copy.deepcopy(card) for card in cards if card['status']=='approved-current']
put('current-handoff-v1.json', {'intent_revision':1,'handoff_revision':1,'approved_cards':current,'excluded':['A:0 rejected','B:1 superseded','C:1 deferred'],'authority':'scripted synthetic expectation approvals only; no concrete output labels','format':'native JSONL fields id/suite/family/request/state/expected','runner':'python3 evaluate.py run --candidate <file> --cases eval-runs/skill-exercise/author/approved.jsonl --suite development --out <fresh path>','author_scope':'author/ and controls/; source records remain separate and hash frozen','independent_roles':'unavailable; one current agent uses disclosed local fallback','partition':'development; common authorization construction family; no independent holdout','technical_mapping':{'guidance':'guidance','create exactly one':'create_ticket / ticket_delta 1','null account':None,'arbitrary unique ID':'native new_ticket_fields and unique_ticket_ids checks; no exact ID in expected'}})
put('pending-excluded.json', {'pending':[{'card':'C:1','reason':'No urgency/escalation policy; no runnable expectation or inverse approved'}], 'excluded':[{'card':'A:0','reason':'rejected original creation proposal'}, {'card':'B:1','reason':'explicit replacement B:2 supersedes guidance-only proposal'}], 'proposal_queue':['D:1 boundary contrast pending approval; defined separately after handoff']})
(source/'intent-v1.md').write_text('''Intent revision 1: distinguish a VPN how-to from an affirmative ticket request. A:1 must give guidance with null account and preserve all state. B:2 must append one open VPN ticket for acct-a with any unique nonempty ID, preserving acct-b\'s original ticket including metadata and counter=7. Explanatory wording is not semantically graded by the native contract. No invented escalation/urgency policy or inferred inverse approval. Source: exact scripted task decisions, not production traces or concrete outcome labels. No interview questions remain for approved cases. The task supplies only partial history wording; card-history marks recovered predecessor meaning without claiming verbatim earlier cards.\n''')
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source.iterdir())}
(root/'evidence'/'source-freeze-before-author.json').write_text(json.dumps(hashes,indent=2)+'\n')
for p in source.iterdir(): p.chmod(0o444)
