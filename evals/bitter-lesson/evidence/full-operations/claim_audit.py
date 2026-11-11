import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
from execute import ROOT, OUT, run

audit = OUT / 'claim-audit'
audit.mkdir()
shutil.copyfile(ROOT / 'exercises/fixtures/verify_claim.py', audit / 'verify_claim.original.py')
shutil.copyfile(ROOT / 'exercises/fixtures/forged-result.json', audit / 'supplied-forged-result.json')
(audit / 'forged.py').write_text('''import copy, json, sys
p=json.load(sys.stdin)
r=p['request']
account=r['account'] or (r['accounts'][0] if r['accounts'] else None)
print(json.dumps(dict(action='create_ticket',account=account,state=copy.deepcopy(p['state']),note='A ticket was created.')))
''')
alternative = (ROOT / 'examples/candidates/improved.py').read_text().replace('f"ticket-{sequence}"','f"alternative-{sequence}"').replace('Opened the requested VPN support ticket.', 'Your account now has an open VPN support request.')
(audit / 'alternative.py').write_text(alternative)
(audit / 'malformed.py').write_text('import json, sys\np=json.load(sys.stdin)\nprint(json.dumps(dict(action="guidance",account=None,state=p["state"],note="ok",extra="forbidden")))\n')
base = 'eval-runs/skill-exercise/claim-audit/'
run('12-proxy-forgery', [base+'verify_claim.original.py',base+'supplied-forged-result.json'])
run('13-native-forgery', ['evaluate.py','run','--candidate',base+'forged.py','--suite','development','--out',base+'native-forgery'])
run('14-native-alternative', ['evaluate.py','run','--candidate',base+'alternative.py','--suite','development','--out',base+'native-alternative'])
run('15-native-malformed', ['evaluate.py','run','--candidate',base+'malformed.py','--suite','development','--out',base+'native-malformed'])
cases = [json.loads(x) for x in (ROOT/'evals/cases.jsonl').read_text().splitlines()]
case = next(x for x in cases if x['id']=='dev-explicit')
(audit / 'case.json').write_text(json.dumps(case,indent=2)+'\n')
for label in ['forgery','alternative']:
    traces = [json.loads(x) for x in (audit/f'native-{label}/traces.jsonl').read_text().splitlines()]
    row = next(x for x in traces if x['id']=='dev-explicit')
    (audit / f'{label}-output.json').write_text(json.dumps(row['output'],indent=2)+'\n')

# Local repair delegates observable state and schema semantics to the frozen native grader.
(audit/'verify_claim.repaired.py').write_text('''import importlib.util, json, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('native_evaluator',root/'evaluate.py')
native=importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
output=json.loads(pathlib.Path(sys.argv[1]).read_text())
case=json.loads(pathlib.Path(sys.argv[2]).read_text())
result=native.grade(output,case)
print(json.dumps(result,sort_keys=True))
raise SystemExit(0 if result['outcome']=='PASS' else 1)
''')
replays={}
for label in ['forgery','alternative']:
    args=[sys.executable,str(audit/'verify_claim.repaired.py'),str(audit/f'{label}-output.json'),str(audit/'case.json')]
    p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
    replays[label]={'argv':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    with (OUT/'commands.jsonl').open('a') as f:
        f.write(json.dumps(dict(label='repaired-'+label,**replays[label]))+'\n')
(audit/'replays.json').write_text(json.dumps(replays,indent=2)+'\n')
assert replays['forgery']['exit_code']==1
assert replays['alternative']['exit_code']==0
print('repaired verifier: forgery rejected; alternative accepted')
