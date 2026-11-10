import hashlib,json,pathlib,subprocess,sys
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[1]
OUT=BASE/'extra-field-reduction';OUT.mkdir()
c=next(json.loads(x) for x in (ROOT/'evals/cases.jsonl').read_text().splitlines() if json.loads(x)['id']=='dev-explicit')
c.update(id='extra-field-minimal',family='dev-explicit-output-boundary')
(OUT/'cases.jsonl').write_text(json.dumps(c)+'\n')
commands=[]
for mode in ['four-fields','five-fields']:
    extra="t['created_at']='2026-11-10T00:00:00Z'\n" if mode=='five-fields' else ''
    path=OUT/(mode+'.py');path.write_text("import json,sys\np=json.load(sys.stdin)\ns=p['state']\nt={'id':'arbitrary-valid-id','account':'acct-a','status':'open','issue':'vpn'}\n"+extra+"s['tickets'].append(t)\nprint(json.dumps({'action':'create_ticket','account':'acct-a','state':s,'note':'Opened requested VPN ticket.'}))\n")
    argv=[sys.executable,'evaluate.py','run','--candidate',str(path),'--cases',str(OUT/'cases.jsonl'),'--suite','all','--out',str(OUT/mode)]
    r=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True)
    commands.append({'command':argv,'cwd':str(ROOT),'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
(OUT/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
(OUT/'source-excerpts.json').write_text(json.dumps({'spec_rule':'Creation appends exactly one ticket with a unique nonempty string ID, selected account, status open, and issue vpn. Preserve original tickets and all other supplied state exactly.','rubric_check':'For creation, append exactly one ticket. It has a unique nonempty string ID, the selected account, status open, and issue vpn. Any unique ID is acceptable; the grader must not require the reference candidate naming pattern.','native_valid_ticket':'isinstance(value, dict) and set(value) == {id, account, status, issue} and all(isinstance(v, str) and bool(v) for v in value.values())','expected_status':'pending independent intent review; artifacts only, no conclusion'},indent=2)+'\n')
print(json.dumps({'path':str(OUT),'case_executions':2,'outputs':{m:json.loads((OUT/m/'summary.json').read_text()) for m in ['four-fields','five-fields']}},indent=2))
