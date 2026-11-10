"""Reproducible bounded case construction; executes only native evaluator and supplied proxy."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
PYTHON = sys.executable
COMMANDS = []
PROTECTED = ['AGENTS.md', 'README.md', 'evaluate.py', 'support_agent.py', 'evals/spec.json', 'evals/cases.jsonl', 'evals/rubric.md',
             'exercises/06-cross-examine.md', 'exercises/fixtures/verify_claim.py', 'exercises/fixtures/forged-result.json',
             'examples/candidates/improved.py']
PROTECTED += [str(p.relative_to(ROOT)) for p in (ROOT/'.agents/skills').rglob('*') if p.is_file()]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def command(label, args):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    receipt = {'label': label, 'argv': args, 'cwd': str(ROOT), 'exit_code': result.returncode,
               'stdout': result.stdout, 'stderr': result.stderr}
    save(BASE / (label + '.receipt.json'), receipt)
    COMMANDS.append(receipt)
    return result

before = {p: sha(ROOT/p) for p in PROTECTED}
save(BASE/'source-before.json', before)
# Freeze provenance before running construction. Installed skill and references are protected.
save(BASE/'access.json', {
    'candidate_access': 'Native candidate subprocess: trusted local host permissions, fresh cwd, Python -I, restricted env; no sandbox is claimed.',
    'operator_access': 'Read protected source and installed skill; create artifacts only eval-runs/case-build; trace and SIGKILL own native process.',
    'writes': str(BASE), 'forbidden_writes': PROTECTED,
    'candidate_behaviors': 'Static stdout generator candidates only; no filesystem, network, process, or source writes.',
    'execution_policy': 'Native deterministic repeats=1; three candidate suite comparisons; lifecycle clean/no-op/two replay/timing reduction.',
    'budgets': {'max_actual_case_executions':120, 'max_process_interruptions':4},
    'source_exposure': 'Original protected source, fixture cases, supplied candidate control, supplied defective verifier, and installed skill; no sibling reports.'})

# Lifecycle family: use the native campaign source, default original cases and candidate.
clean = BASE/'lifecycle-clean'
command('lifecycle-clean', [PYTHON, 'evaluate.py', 'start', '--campaign', str(clean), '--max-case-runs', '24', '--reserve-case-runs', '8'])

lifecycle = []
for label, function, attempt_id, action in [
    ('lifecycle-noop', 'complete_attempt', 99, 'SIGKILL_SELF'),
    ('lifecycle-complete-stop-1', 'complete_attempt', 0, 'SIGKILL_SELF'),
    ('lifecycle-complete-stop-2', 'complete_attempt', 0, 'SIGKILL_SELF'),
    ('lifecycle-before-execute', 'execute_attempt', 0, 'SIGKILL_SELF'),
]:
    campaign = BASE/label
    config = {'root': str(ROOT), 'source_sha256': before['evaluate.py'], 'function':function,
              'attempt_id':attempt_id, 'action':action,
              'activation_log':str(BASE/(label+'.activation.jsonl')),
              'completion_log':str(BASE/(label+'.completion.json')),
              'native_args':['start', '--campaign', str(campaign), '--max-case-runs','24','--reserve-case-runs','8']}
    config_path = BASE/(label+'.config.json')
    save(config_path, config)
    result = command(label,[PYTHON,str(BASE/'inject_native.py'),str(config_path)])
    raw_state = json.loads((campaign/'state.json').read_text())
    save(BASE/(label+'.pre-status-state.json'),raw_state)
    files = {str(p.relative_to(campaign)):sha(p) for p in campaign.rglob('*') if p.is_file()}
    save(BASE/(label+'.pre-status-files.json'),files)
    attempt_path=campaign/'attempts/000-baseline'
    if (attempt_path/'summary.json').exists():
        save(BASE/(label+'.pre-status-summary.json'),json.loads((attempt_path/'summary.json').read_text()))
    command(label+'-status',[PYTHON,'evaluate.py','status','--campaign',str(campaign)])
    save(BASE/(label+'.post-status-state.json'),json.loads((campaign/'state.json').read_text()))
    # A second status establishes that reconciliation is idempotent and does not rerun cases.
    command(label+'-status-repeat',[PYTHON,'evaluate.py','status','--campaign',str(campaign)])
    after_files={str(p.relative_to(campaign)):sha(p) for p in campaign.rglob('*') if p.is_file()}
    activated = Path(config['activation_log'])
    events=[json.loads(s) for s in activated.read_text().splitlines()] if activated.exists() else []
    lifecycle.append({'label':label, 'process_exit':result.returncode, 'activation_count':len(events),
                      'events':events, 'pre_status_state':raw_state,
                      'post_status_state':json.loads((campaign/'state.json').read_text()),
                      'pre_status_files':files, 'post_status_files':after_files})
save(BASE/'lifecycle-observations.json',lifecycle)

# Score boundary family: retain source intent and vary context/legitimate output representation.
source=json.loads(next(s for s in (ROOT/'evals/cases.jsonl').read_text().splitlines() if json.loads(s)['id']=='dev-explicit'))
rich=json.loads(json.dumps(source))
rich.update(id='build-claim-preservation', family='forward-claim-boundary-dev-explicit')
rich['state']={'tickets':[{'id':'prior-password','account':'acct-b','status':'open','issue':'password'}],
               'audit':{'revision':7,'owner':'fixture'}}
small=json.loads(json.dumps(source))
small.update(id='build-claim-minimal',family='forward-claim-boundary-dev-explicit')
case_file=BASE/'score-boundary.jsonl'
case_file.write_text(''.join(json.dumps(c,sort_keys=True)+'\n' for c in [rich,small]))

# Static payload-dependent generators have the same schema. The forge claims creation without state change.
candidates={
    'forged':'''import json,sys\np=json.load(sys.stdin)\nprint(json.dumps({'action':'create_ticket','account':'acct-a','state':p['state'],'note':'A ticket was created.'}))\n''',
    'legitimate':'''import json,sys\np=json.load(sys.stdin)\ns=p['state']\ns['tickets'].append({'id':'ticket-1','account':'acct-a','status':'open','issue':'vpn'})\nprint(json.dumps({'action':'create_ticket','account':'acct-a','state':s,'note':'Opened requested VPN ticket.'}))\n''',
    'legitimate-alternative':'''import json,sys\np=json.load(sys.stdin)\ns=p['state']\ns['tickets'].append({'id':'incident:7f29','account':'acct-a','status':'open','issue':'vpn'})\nprint(json.dumps({'note':'Saved your support request; reference incident:7f29.','state':s,'account':'acct-a','action':'create_ticket'}))\n'''
}
score=[]
for label,text in candidates.items():
    candidate=BASE/(label+'.py')
    candidate.write_text(text)
    out=BASE/('native-'+label)
    command('native-'+label,[PYTHON,'evaluate.py','run','--candidate',str(candidate),'--cases',str(case_file),'--suite','development','--out',str(out)])
    summary=json.loads((out/'summary.json').read_text())
    traces=[json.loads(s) for s in (out/'traces.jsonl').read_text().splitlines()]
    for index,trace in enumerate(traces):
        output=trace['output']
        op=BASE/('proxy-input-'+label+'-'+str(index)+'.json')
        save(op,output)
        receipt=command('proxy-'+label+'-'+str(index),[PYTHON,'exercises/fixtures/verify_claim.py',str(op)])
        original=trace['input']['state']
        actual=output['state']
        old_ids={t['id'] for t in original['tickets']}
        new=[t for t in actual['tickets'] if t['id'] not in old_ids]
        witness={'id':trace['id'],'candidate':label,'native_outcome':trace['outcome'],'native_checks':trace['checks'],
                 'proxy_passed':json.loads(receipt.stdout)['passed'], 'proxy_exit':receipt.returncode,
                 'actual_new_tickets':new,'delta':len(actual['tickets'])-len(original['tickets']),
                 'preserved_original_prefix':actual['tickets'][:len(original['tickets'])]==original['tickets'],
                 'preserved_other_state':{k:v for k,v in actual.items() if k!='tickets'}=={k:v for k,v in original.items() if k!='tickets'},
                 'candidate_output':output,'output_sha256':sha(op)}
        score.append(witness)
save(BASE/'score-observations.json',score)
after={p:sha(ROOT/p) for p in PROTECTED}
save(BASE/'source-after.json',after)
assert before==after,'protected source changed'
# Count actual native candidate subprocess observations. No-op status/recovery do not execute candidates.
native_traces=list(BASE.glob('lifecycle-*/attempts/*/traces.jsonl'))+list(BASE.glob('native-*/traces.jsonl'))
actual=sum(len(p.read_text().splitlines()) for p in native_traces)
interruptions=sum(r['exit_code']==-9 for r in COMMANDS)
reservation_total=sum(json.loads((p/'state.json').read_text())['used_case_runs'] for p in BASE.glob('lifecycle-*') if p.is_dir())
counts={'actual_native_case_executions':actual,'operator_process_interruptions':interruptions,
        'native_campaign_reserved_case_runs':reservation_total, 'proxy_invocations':6,
        'native_case_run_trace_files':{str(p.relative_to(BASE)):len(p.read_text().splitlines()) for p in native_traces},
        'protected_sources_unchanged':before==after, 'network_calls':0,'provider_calls':0,'subagents':0}
assert actual<=120 and interruptions<=4
save(BASE/'counts.json',counts)
save(BASE/'commands.json',COMMANDS)
print(json.dumps(counts,indent=2,sort_keys=True))
