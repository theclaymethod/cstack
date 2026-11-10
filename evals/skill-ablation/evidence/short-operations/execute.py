import json, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'eval-runs/skill-exercise'
COMMANDS = {
 'baseline': ['evaluate.py','run','--candidate','support_agent.py','--suite','development','--out',str(BASE/'run-baseline')],
 'conforming': ['evaluate.py','run','--candidate','examples/candidates/improved.py','--suite','development','--out',str(BASE/'run-conforming')],
 'compare': ['evaluate.py','compare','--baseline',str(BASE/'run-baseline'),'--candidate',str(BASE/'run-conforming')],
 'start': ['evaluate.py','start','--campaign',str(BASE/'campaign'),'--max-case-runs','48','--reserve-case-runs','8'],
 'regression': ['evaluate.py','try','--campaign',str(BASE/'campaign'),'--candidate','examples/candidates/regression.py','--hypothesis','Route authorization and reuse tickets; risk closed or unrelated ticket incorrectly blocks creation'],
 'improved': ['evaluate.py','try','--campaign',str(BASE/'campaign'),'--candidate','examples/candidates/improved.py','--hypothesis','Require authorized creation and scope existing open VPN tickets to selected account'],
 'finish': ['evaluate.py','finish','--campaign',str(BASE/'campaign')],
 'status': ['evaluate.py','status','--campaign',str(BASE/'campaign')],
 'verify': ['evaluate.py','verify','--campaign',str(BASE/'campaign')],
 'judge': ['-m','judge_calibration.run','--out',str(BASE/'judge')],
 'simplification': ['-m','simplification.run','--out',str(BASE/'simplification')],
 'claim': ['exercises/fixtures/verify_claim.py','exercises/fixtures/forged-result.json'],
}
for label in sys.argv[1:]:
 start=time.time(); argv=[sys.executable]+COMMANDS[label]
 result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True)
 (BASE/f'{label}.stdout').write_text(result.stdout)
 (BASE/f'{label}.stderr').write_text(result.stderr)
 receipt={'label':label,'argv':argv,'cwd':str(ROOT),'start_epoch':start,'end_epoch':time.time(),'exit_code':result.returncode,'stdout':f'{label}.stdout','stderr':f'{label}.stderr'}
 with (BASE/'commands.jsonl').open('a') as f: f.write(json.dumps(receipt)+'\n')
 print(json.dumps({'label':label,'exit_code':result.returncode,'stdout':result.stdout[-1500:],'stderr':result.stderr[-500:]}),flush=True)
 if result.returncode: raise SystemExit(result.returncode)
