#!/usr/bin/env python3
"""Bounded native lifecycle controls; operator mutations are explicitly labeled."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from simplification.protocol import Experiment,configuration,UNITS,sources
from methods.native import evaluate
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
OUT.mkdir(parents=True,exist_ok=True)

def put(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def observe(call):
    try:
        result=call()
        return {'accepted':True,'result':result}
    except Exception as error:
        return {'accepted':False,'type':type(error).__name__,'message':str(error)}

put('source-identity-before.json',sources())
full=configuration('old-fixture',set(UNITS))
lean=configuration('old-fixture',{'contract','legacy-auth','duplicate-b'})
experiment=Experiment(OUT/'clean',limit=24,confirmation_reserve=8)
experiment.measure('original',full)
experiment.measure('reduced',lean)
pre=experiment.compare('original','reduced')
plan={'final-original':full,'final-reduced':lean}
experiment.freeze(plan)
# A mutation of the caller's copy must not alter exact final membership.
plan['final-reduced']['retained'].append('example')
experiment.confirm('final-original')
experiment.confirm('final-reduced')
experiment.finish()
post=experiment.compare('final-original','final-reduced')
checks={'legitimate_development':pre,'legitimate_confirmation':post,
        'reserved':experiment.runs.reserved,
        'caller_plan_edit_isolated':experiment.plan['final-reduced']==configuration('old-fixture',{'contract','legacy-auth','duplicate-b'}),
        'late_fit':observe(lambda:experiment.measure('late',lean)),
        'repeat_final':observe(lambda:experiment.confirm('final-reduced'))}
# Extra operator access, not candidate/config access. Corrupt only the disposable ledger.
ledger=experiment.runs.directory/'executions.json'
original_ledger=ledger.read_bytes()
(OUT/'ledger-original.json').write_bytes(original_ledger)
ledger.write_text('{"limit":0,"reserved":0,"actual_completed":0,"calls":[]}\n')
(OUT/'ledger-perturbed.json').write_bytes(ledger.read_bytes())
checks['operator_ledger_zeroed_then_checked']=observe(lambda:experiment.checked('final-reduced'))
checks['operator_ledger_zeroed_then_compared']=observe(lambda:experiment.compare('final-original','final-reduced'))
checks['in_memory_charge_after_ledger_edit']=experiment.runs.reserved
ledger.write_bytes(original_ledger)
# Adjacent immutable evidence and live state controls.
summary=experiment.runs.directory/'final-reduced'/'summary.json'
summary_original=summary.read_bytes()
summary.write_bytes(summary_original+b'\n')
checks['operator_summary_changed']=observe(lambda:experiment.checked('final-reduced'))
(OUT/'summary-perturbed.json').write_bytes(summary.read_bytes())
summary.write_bytes(summary_original)
experiment.plan['final-reduced']['retained'].append('example')
checks['operator_live_plan_changed']=observe(lambda:experiment.checked('final-reduced'))
experiment.plan['final-reduced']['retained'].remove('example')
# Selected source drift must be caught before additional native execution.
source=ROOT/'simplification'/'run.py'
source_original=source.read_bytes()
try:
    source.write_bytes(source_original+b'\n# operator identity perturbation\n')
    checks['operator_source_changed']=observe(lambda:experiment.checked('final-reduced'))
finally:
    source.write_bytes(source_original)
checks['post_restoration']=observe(lambda:experiment.compare('final-original','final-reduced'))
put('observations.json',checks)
# Independent operator stop after one complete, flushed native trace; before second run_case.
worker=OUT/'interrupt-worker.py'
worker.write_text('''import json,os,sys\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nfrom simplification.protocol import Experiment,configuration,UNITS\nfrom methods.native import evaluate\nfolder=Path(sys.argv[2]);marker=Path(sys.argv[3]);seen=0\ndef hook(frame,event,arg):\n global seen\n if event=='call' and frame.f_code is evaluate.run_case.__code__:\n  seen+=1\n  if seen==2:\n   traces=folder/'native'/'interrupted'/'traces.jsonl'\n   marker.write_text(json.dumps({'boundary':'before second run_case','completed_trace_lines':len(traces.read_text().splitlines()),'source_sha256':evaluate.digest(Path(evaluate.__file__))}))\n   os._exit(22)\n return hook\nexperiment=Experiment(folder,limit=12,confirmation_reserve=4)\nsys.settrace(hook)\nexperiment.measure('interrupted',configuration('old-fixture',set(UNITS)))\n''')
process=subprocess.run([sys.executable,str(worker),str(ROOT),str(OUT/'interrupted'),str(OUT/'activation.json')],capture_output=True,text=True)
put('interrupt-process.json',{'exit_code':process.returncode,'stdout':process.stdout,'stderr':process.stderr})
interrupted=OUT/'interrupted'/'native'/'interrupted'
traces=[json.loads(row) for row in (interrupted/'traces.jsonl').read_text().splitlines()]
put('interrupt-observations.json',{'activation':json.loads((OUT/'activation.json').read_text()),'actual_trace_cases':len(traces),'outcomes':[row['outcome'] for row in traces],
    'comparison_rejected':observe(lambda:evaluate.checked_run(interrupted)),
    'state':json.loads((OUT/'interrupted'/'state.json').read_text()),
    'ledger':json.loads((OUT/'interrupted'/'native'/'executions.json').read_text())})
put('source-identity-after.json',sources())
put('usage.json',{'actual_native_cases':24+len(traces),'case_budget':200,'native_reservations':24+8,'provider_calls':0,'attempts':['clean 24-case legitimate workflow','ledger operator perturbation (0 additional cases)','summary operator perturbation (0 additional cases)','live plan operator perturbation (0 additional cases)','source identity operator perturbation (0 additional cases)','targeted operator interruption after first of 8 reserved cases (1 actual case)']})
print(json.dumps({'actual_native_cases':24+len(traces),'observations':str(OUT/'observations.json')},indent=2))
