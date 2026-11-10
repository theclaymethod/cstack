import copy, hashlib, json, subprocess, sys, time
from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[2]; BASE=ROOT/'eval-runs/skill-exercise'; OUT=BASE/'claim-audit'; OUT.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('native',ROOT/'evaluate.py'); native=importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
for name in ['verify_claim.py','forged-result.json']:
 (OUT/name).write_bytes((ROOT/'exercises/fixtures'/name).read_bytes())
forged=json.loads((OUT/'forged-result.json').read_text())
(OUT/'forged.py').write_text('import json, sys\njson.load(sys.stdin)\nprint('+repr(json.dumps(forged))+')\n')
source=(ROOT/'examples/candidates/improved.py').read_text().replace('ticket-{sequence}','alternative-{sequence}').replace('Opened the requested VPN support ticket.','Your selected account now has a VPN support request.')
(OUT/'legitimate-alternative.py').write_text(source)
# Observational repaired fixture delegates all semantics to the frozen native grader.
(OUT/'repaired-verifier.py').write_text('import importlib.util, json, sys\nfrom pathlib import Path\nroot=Path(__file__).resolve().parents[3]\nspec=importlib.util.spec_from_file_location("native",root/"evaluate.py")\nm=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\ncase=json.loads(Path(sys.argv[1]).read_text()); result=json.loads(Path(sys.argv[2]).read_text())\nprint(json.dumps(m.grade(result,case),sort_keys=True))\n')
def run(label,args):
 argv=[sys.executable]+[str(x) for x in args]; start=time.time(); p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True)
 (OUT/f'{label}.stdout').write_text(p.stdout); (OUT/f'{label}.stderr').write_text(p.stderr)
 with (BASE/'commands.jsonl').open('a') as f: f.write(json.dumps({'label':label,'argv':argv,'cwd':str(ROOT),'start_epoch':start,'end_epoch':time.time(),'exit_code':p.returncode,'stdout':str((OUT/f'{label}.stdout').relative_to(BASE)),'stderr':str((OUT/f'{label}.stderr').relative_to(BASE))})+'\n')
 if p.returncode: raise RuntimeError(p.stderr)
 return p.stdout
run('forged-native',['evaluate.py','run','--candidate',OUT/'forged.py','--suite','development','--out',OUT/'forged-native'])
run('alternative-native',['evaluate.py','run','--candidate',OUT/'legitimate-alternative.py','--suite','development','--out',OUT/'alternative-native'])
case=next(c for c in native.load_cases('development') if c['id']=='dev-explicit'); (OUT/'case.json').write_text(json.dumps(case,indent=2))
traces=[json.loads(x) for x in (OUT/'alternative-native/traces.jsonl').read_text().splitlines()]; valid=next(t['output'] for t in traces if t['id']=='dev-explicit'); (OUT/'alternative-result.json').write_text(json.dumps(valid,indent=2))
run('repaired-forged',[OUT/'repaired-verifier.py',OUT/'case.json',OUT/'forged-result.json'])
run('repaired-alternative',[OUT/'repaired-verifier.py',OUT/'case.json',OUT/'alternative-result.json'])
# Boundary checks exercise the same native grade function, without additional candidate processes.
malformed={}
for kind in ['missing-note','extra-field','blank-note']:
 item=copy.deepcopy(valid)
 if kind=='missing-note': del item['note']
 elif kind=='extra-field': item['unsupported']=True
 else: item['note']=' '
 malformed[kind]=native.grade(item,case)
(OUT/'schema-boundaries.json').write_text(json.dumps(malformed,indent=2))
print(json.dumps({'forged_native':native.grade(forged,case),'alternative_native':native.grade(valid,case),'alternative_id':valid['state']['tickets'][-1]['id'],'native_case_executions':16,'schema_checks':malformed},indent=2))
