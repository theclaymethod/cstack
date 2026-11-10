import importlib.util, json, pathlib, subprocess, sys
out=pathlib.Path(__file__).resolve().parent
repo=out.parents[2]
spec=importlib.util.spec_from_file_location('native_evaluate', repo/'evaluate.py')
evaluate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluate)
cases={c['id']: c for c in evaluate.load_cases('development')}
alt=[json.loads(s) for s in (out/'native-alternative/traces.jsonl').read_text().splitlines()]
legit=next(t for t in alt if t['id']=='dev-unrelated')
(out/'legitimate-result.json').write_text(json.dumps(legit['output'],indent=2)+'\n')
forged=dict(legit['output'],state=legit['input']['state'])
(out/'matched-forged-result.json').write_text(json.dumps(forged,indent=2)+'\n')
receipts=[]
for name in ('matched-forged-result','legitimate-result'):
    p=subprocess.run([sys.executable,str(out/'verify_claim.original.py'),str(out/(name+'.json'))],text=True,capture_output=True)
    receipts.append({'artifact':name,'original':{'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr},'native_repaired':evaluate.grade(json.loads((out/(name+'.json')).read_text()),cases['dev-unrelated'])})
for receipt in receipts:
    print(json.dumps(receipt))
(out/'replay-results.json').write_text(json.dumps({'source_case':'dev-unrelated','receipts':receipts,'legitimate_all_development_regrades':{t['id']:evaluate.grade(t['output'],cases[t['id']]) for t in alt},'extra_native_candidate_processes':0,'stored_output_regrades':10,'original_proxy_processes':2,'independent_review':'unreviewed'},indent=2)+'\n')
