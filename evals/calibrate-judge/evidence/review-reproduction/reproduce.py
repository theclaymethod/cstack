import json
import shutil
import tempfile
from pathlib import Path
from judge_calibration.adapters import normalize
from judge_calibration.workflow import Campaign, config, sources
from methods.native import evaluate, jsonl, read_rows, write
root=Path('/Users/clayton/Documents/Codex/2026-11-10/in-my-cstack-repo-i-want/work/calibrate-judge-build')
malformed={'answers':{'criterion':{'type':'choice','choice':'PASS','probabilities':['PASS','FAIL']}}}
try:
    print('malformed_choice', normalize(malformed, config('jev')))
except Exception as exc:
    print('malformed_choice_raised',type(exc).__name__,str(exc))

raw={'answers':{'criterion':{'type':'noul','noul':10**400}}}
try:
    print('oversized_probability',normalize(raw,config('jev')))
except Exception as exc:
    print('oversized_probability_raised',type(exc).__name__,str(exc))

# Read existing synthetic dataset and run a single eight-case offline process batch.
scratch=Path(tempfile.mkdtemp(prefix='reproduction-',dir=root/'review-scratch'))
dataset=scratch/'dataset'
shutil.copytree(root/'demo-first/dataset',dataset)
manifest=evaluate.read_json(dataset/'manifest.json')
manifest['sources']=sources()
write(dataset/'manifest.json',manifest)
c=Campaign(dataset,scratch/'campaign')
p=c.predict('original',config('llm'),'validation')
before=c.compare(p)['agreement']['observed_agreement_decided']
records=read_rows(p/'predictions.jsonl')
gold={r['id']:r['gold'] for r in c.rows()}
for r in records:
    r['raw']['text']=json.dumps({'verdict':gold[r['id']]})
    r['stdout']=json.dumps(r['raw'])+'\n'
    r['decision']=normalize(r['raw'],config('llm'),r['exit_code'])
jsonl(p/'predictions.jsonl',records)
man=evaluate.read_json(p/'manifest.json')
man['predictions_sha256']=evaluate.digest(p/'predictions.jsonl')
write(p/'manifest.json',man)
after=c.compare(p)['agreement']['observed_agreement_decided']
print('changed_complete_evidence_accepted',{'before':before,'after':after,'worker_calls':c.state['worker_calls']})
