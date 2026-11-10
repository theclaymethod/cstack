"""Operator-extra-access validator probe; no candidate-access claim, no new execution.
Only copies of generated eval-runs artifacts are mutated; frozen code stays read-only.
"""
import hashlib, importlib.util, json, pathlib, shutil
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OWNER=ROOT.parents[0]
FROZEN=OWNER.parent/'frozen'
PRISTINE=ROOT/'eval-runs/replay-pristine/workspace/eval-runs/case-build'
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
replay=module('frozen_replay', FROZEN/'evals/adversarial-cases/replay.py')
native=module('native_evaluator',ROOT/'eval-runs/replay-pristine/workspace/evaluate.py')
results=[]
for label in ['missing-one-lifecycle-observation','empty-lifecycle-observations','omitted-command-receipt']:
    base=HERE/label
    shutil.copytree(PRISTINE,base)
    mutation=None
    if label=='stdout-output-conflict':
        path=base/'native-legitimate/traces.jsonl'
        rows=[json.loads(x) for x in path.read_text().splitlines()]
        old=rows[0]['stdout'];actual=json.loads(old);actual['state']=rows[0]['input']['state']
        rows[0]['stdout']=json.dumps(actual)+'\n'
        path.write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in rows))
        mutation={'relative_path':'native-legitimate/traces.jsonl','field':'first trace stdout only','before':old,'after':rows[0]['stdout'],'output_field_and_native_outcome_unchanged':True}
    if label=='matched-false-source-inventory':
        mutation={'relative_paths':['source-before.json','source-after.json'],'change':'both inventories replaced by empty object; no protected files changed'}
        for name in ['source-before.json','source-after.json']:(base/name).write_text('{}\n')
    if label in ['missing-one-lifecycle-observation','empty-lifecycle-observations']:
        path=base/'lifecycle-observations.json'
        observations=json.loads(path.read_text())
        retained=[o for o in observations if o['label']!='lifecycle-complete-stop-1'] if label=='missing-one-lifecycle-observation' else []
        path.write_text(json.dumps(retained,indent=2)+'\n')
        mutation={'relative_path':'lifecycle-observations.json','removed_labels':[o['label'] for o in observations if o not in retained],'retained_count':len(retained),'note':'all real trace, campaign, configuration and activation artifacts retained'}
    if label=='omitted-command-receipt':
        path=base/'commands.json';commands=json.loads(path.read_text());retained=[c for c in commands if c['label']!='native-legitimate']
        path.write_text(json.dumps(retained,indent=2)+'\n')
        (base/'native-legitimate.receipt.json').unlink()
        mutation={'relative_paths':['commands.json','native-legitimate.receipt.json'],'change':'removed native-legitimate command list entry and deleted its standalone receipt; actual native run evidence retained','removed_count':len(commands)-len(retained)}
    try:checks=replay.validate(base);verdict={'accepted':True,'check_count':len(checks)}
    except Exception as e:verdict={'accepted':False,'error':str(e)}
    try:native.checked_run(base/'native-legitimate');native_verdict={'accepted':True}
    except Exception as e:native_verdict={'accepted':False,'error':str(e)}
    results.append({'label':label,'access':'explicit operator-extra-access probe on copied eval-runs artifacts; not permitted candidate behavior','mutation':mutation,'frozen_replay_validate':verdict,'native_checked_run_legitimate':native_verdict,'new_case_executions':0,'new_interruptions':0})
(HERE/'coverage-receipts.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
