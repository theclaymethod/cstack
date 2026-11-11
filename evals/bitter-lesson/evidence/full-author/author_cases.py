"""Native case conversion, proposals and bounded control source; no evaluator edits."""
import hashlib, json, shutil
from pathlib import Path
root = Path(__file__).resolve().parent
workspace = root.parents[1]
handoff = json.loads((root/'source/current-handoff-v1.json').read_text())
rows = [{'id':f"approved-{c['id']}-r{c['revision']}", 'suite':'development', 'family':c['family'], 'request':c['request'], 'state':c['state'], 'expected':c['expected']} for c in handoff['approved_cards']]
(root/'author/approved.jsonl').write_text(''.join(json.dumps(c,sort_keys=True)+'\n' for c in rows))
(root/'author/lineage.json').write_text(json.dumps({c['id']:{'source_card':f"{s['id']}:{s['revision']}", 'intent_revision':1,'handoff_revision':1,'source':'../source/current-handoff-v1.json','conversion':'exact deep JSON values; native expected encodes behavioral checks, ID unconstrained'} for c,s in zip(rows,handoff['approved_cards'])},indent=2)+'\n')
b = rows[1]
contrast = {'id':'D','revision':1,'status':'proposed-unapproved','source_requirement':'intent-v1 plus evals/spec.json account-selection rule','family':b['family'],'method':'minimal factual contrast of B:2','hypothesis':'A program may guess acct-a without authorization to choose among two accounts.','request':dict(b['request'],account=None),'state':b['state'],'differing_condition':{'field':'request.account','from':'acct-a','to':None},'proposed_expected':{'allowed_actions':['clarify'],'account':None,'ticket_delta':0},'reason':'Explicit create request still names two available accounts; request no longer selects one. Native fixture supports clarification. This is a proposal, not owner-approved.','feasibility':'same valid native request/state shape as B; two listed accounts remain available','access':{'candidate':'stdin request/state; returns JSON with local host permissions in runner; no strong containment','operator':'case construction only; no lifecycle/dependency injection armed or run'},'execution':{'status':'not run','case_attempts':0,'armed':False,'activation_count':None,'activation_witness':None,'resulting_state':None,'score':None},'controls_plan':'If approved, compare unchanged B explicit account control and D absent account under clean and alternate candidates. No fault activation or observed defect is claimed.','reduction':'one changed field by construction; no executed minimization trials','next_prerequisite':'scoped approval of D:1 before adding to approved native package'}
(root/'author/proposed-boundary-D-r1.json').write_text(json.dumps(contrast,indent=2)+'\n')
shutil.copyfile(workspace/'examples/candidates/improved.py',root/'controls/legitimate.py')
shutil.copyfile(workspace/'support_agent.py',root/'controls/original-baseline.py')
clean=(root/'controls/legitimate.py').read_text()
(root/'controls/alternative-id.py').write_text(clean.replace('ticket-{sequence}', 'valid-alt-{sequence}'))
(root/'controls/false-creation-claim.py').write_text('''"""Targeted control: claims creation but leaves actual state unchanged."""\nimport copy, json, sys\np = json.load(sys.stdin)\ncreate = "create" in p["request"]["text"].lower()\nprint(json.dumps({"action":"create_ticket" if create else "guidance", "account":p["request"]["account"] if create else None, "state":copy.deepcopy(p["state"]), "note":"Opened the requested VPN support ticket." if create else "Check VPN setup instructions."}))\n''')
(root/'controls/guidance-only.py').write_text('''"""Targeted control: old B proposal must fail current B:2."""\nimport copy, json, sys\np=json.load(sys.stdin)\nprint(json.dumps({"action":"guidance", "account":None, "state":copy.deepcopy(p["state"]), "note":"Check VPN settings."}))\n''')
protected=['evaluate.py','evals/spec.json','evals/rubric.md','evals/cases.jsonl','support_agent.py']
(root/'evidence/protected-before.json').write_text(json.dumps({p:hashlib.sha256((workspace/p).read_bytes()).hexdigest() for p in protected},indent=2)+'\n')
