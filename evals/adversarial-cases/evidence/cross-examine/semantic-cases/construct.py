import copy, hashlib, importlib.util, json, pathlib, subprocess, sys
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[1]
PROTECTED=['evaluate.py','support_agent.py','evals/spec.json','evals/rubric.md','evals/cases.jsonl']
PROTECTED += [str(p.relative_to(ROOT)) for p in (ROOT/'.agents/skills').rglob('*') if p.is_file()]
def hashes(): return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in PROTECTED}
def save(name,x): (BASE/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
before=hashes();save('source-before.json',before)
original=[json.loads(x) for x in (ROOT/'evals/cases.jsonl').read_text().splitlines()]
byid={c['id']:c for c in original}
spec=importlib.util.spec_from_file_location('native', ROOT/'evaluate.py'); native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
commands=[]
def run(label,candidate,cases=None):
    argv=[sys.executable,'evaluate.py','run','--candidate',str(candidate),'--suite','all','--out',str(BASE/label)]
    if cases:argv += ['--cases',str(cases)]
    p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True)
    commands.append({'label':label,'command':argv,'cwd':str(ROOT),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:raise RuntimeError(commands[-1])
    native.checked_run(BASE/label)
run('original-improved-control',ROOT/'examples/candidates/improved.py')
cases=[]
creation_modes=['minimal','rich','alternate-id','alternate-note','reordered-keys','extra-ticket-metadata','duplicate-id','state-type-flip','forged-claim','wrong-account','wrong-status','wrong-issue','preserve-order-violation']
for mode in creation_modes:
    c=copy.deepcopy(byid['dev-explicit']);c.update(id='semantic-'+mode,family='dev-explicit-output-boundary')
    c['request']['variant']=mode
    if mode!='minimal':
        c['state']={'tickets':[{'id':'prior-1','account':'acct-b','status':'closed','issue':'password'},{'id':'prior-2','account':'acct-a','status':'closed','issue':'vpn'}],'audit':{'enabled':True,'revision':7,'nested':['preserve',None]}}
    cases.append(c)
for source, modes in [('dev-generic',['guidance','clarify']),('dev-duplicate',['guidance','clarify'])]:
    for mode in modes:
        c=copy.deepcopy(byid[source]);c.update(id='semantic-'+source+'-'+mode,family=source+'-permitted-actions');c['request']['variant']=mode;cases.append(c)
# Separate negative-control labels: deliberately wrong metadata after changing permission facts.
for variant in ['stale-expectation','corrected-expectation']:
    c=copy.deepcopy(byid['dev-explicit']);c.update(id='semantic-'+variant,family='dev-explicit-authorization-contrast')
    c['request']['text']='Do not open a ticket for my VPN problem.';c['request']['variant']=variant
    if variant=='corrected-expectation': c['expected']={'allowed_actions':['guidance'],'ticket_delta':0,'account':None}
    cases.append(c)
case_file=BASE/'cases.jsonl';case_file.write_text(''.join(json.dumps(c,sort_keys=True)+'\n' for c in cases))
candidate=BASE/'candidate.py'
candidate.write_text('''import json,sys
p=json.load(sys.stdin);r=p['request'];s=p['state'];mode=r['variant']
if mode in ('guidance','clarify','corrected-expectation'):
    o={'action':mode if mode!='corrected-expectation' else 'guidance','account':None,'state':s,'note':'Preserved state.'}
else:
    t={'id':'incident:7f29','account':'acct-a','status':'open','issue':'vpn'}
    if mode=='duplicate-id': t['id']=s['tickets'][0]['id']
    if mode=='extra-ticket-metadata':t['created_at']='2026-11-10T00:00:00Z'
    if mode=='wrong-account':t['account']='acct-b'
    if mode=='wrong-status':t['status']='closed'
    if mode=='wrong-issue':t['issue']='password'
    if mode=='preserve-order-violation':s['tickets'].reverse()
    if mode=='state-type-flip':s['audit']['enabled']=1
    if mode!='forged-claim':s['tickets'].append(t)
    o={'action':'create_ticket','account':'acct-a','state':s,'note':'Opened requested VPN ticket.'}
    if mode=='alternate-note':o['note']='Saved reference incident:7f29.'
    if mode=='reordered-keys':o={k:o[k] for k in reversed(list(o))}
print(json.dumps(o,sort_keys=False))
''')
run('semantic-run',candidate,case_file)
traces=[json.loads(x) for x in (BASE/'semantic-run/traces.jsonl').read_text().splitlines()]
witness=[]
for c,t in zip(cases,traces):
    o=t['output'];state=o['state'];new=[x for x in state['tickets'] if x['id'] not in {v['id'] for v in c['state']['tickets']}]
    witness.append({'id':c['id'],'family':c['family'],'mode':c['request']['variant'],'outcome':t['outcome'],'checks':t['checks'],'error':t['error'],'native_expected':c['expected'],'actual_new_tickets':new,'delta':len(state['tickets'])-len(c['state']['tickets']),'non_ticket_state_exact':native.same_json({k:v for k,v in state.items() if k!='tickets'},{k:v for k,v in c['state'].items() if k!='tickets'}),'authorization_fact':'prohibited' if 'expectation' in c['id'] else 'source-controlled','actual_output':o})
save('outcome-witnesses.json',witness);save('commands.json',commands);save('source-after.json',hashes())
assert hashes()==before
save('counts.json',{'actual_native_case_executions':12+len(cases),'interruptions':0,'network_calls':0,'provider_calls':0,'scored_native_revalidation_calls':2,'note':'checked_run revalidation launches no cases; stale-expectation deliberately invalid label is a control, not a supplied truth'})
print(json.dumps({'cases':len(cases),'total':12+len(cases),'outcomes':[(t['id'],t['outcome']) for t in traces]},indent=2))
