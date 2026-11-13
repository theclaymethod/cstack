"""Frozen-verifier semantic-integrity probes; all changes restricted to disposable evidence copies."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
BASE=Path(__file__).resolve().parent
SOURCE=BASE/'archive-baseline'
TARGET='capture-forward-signal-1-v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def dump(p,v): p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def refresh_references(value,root):
    if isinstance(value,list):
        for item in value: refresh_references(item,root)
    elif isinstance(value,dict):
        if isinstance(value.get('path'),str) and 'sha256' in value:
            p=root/value['path']
            if p.is_file(): value['sha256']=sha(p)
        for item in value.values(): refresh_references(item,root)
def refresh(archive):
    root=archive/'evidence/workspace';out=root/'eval-runs/capture-forward'
    for p in root.rglob('*.jsonl'):
        # These are serializer-produced annotations, not the frozen native traces.
        if p.name not in {'reviews.jsonl','store-after.jsonl','store-before.jsonl','store-at-checkpoint.jsonl','store-after-replay.jsonl'}: continue
        values=[json.loads(s) for s in p.read_text().splitlines() if s.strip()]
        for v in values: refresh_references(v,root)
        p.write_text(''.join(json.dumps(v,sort_keys=True)+'\n' for v in values))
    # Retain manifest formats and regenerate only real, local file hashes.
    for folder in [out]+[out/f'phase{i}' for i in range(2,7)]:
        p=folder/'checkpoint.json';v=read(p)
        for file in v['files']: v['files'][file]=sha(folder/file)
        dump(p,v);(folder/'checkpoint.sha256').write_text(sha(p)+'  checkpoint.json\n')
    p=out/'final/manifest.json';v=read(p)
    v['store_sha256']=sha(root/'eval-runs/capture-existing/reviews.jsonl')
    for file in v['files']:v['files'][file]=sha(p.parent/file)
    dump(p,v)
def mutate(archive,case):
    root=archive/'evidence/workspace';out=root/'eval-runs/capture-forward'
    if case=='h1-initial-state-mismatch':
        p=out/'artifacts/false-claim-v1/initial-state.json';v=read(p)
        v['tickets']=[{'id':'never-in-native-input','account':'acct-a'}];dump(p,v)
    elif case=='h2-reviewed-output-mismatch':
        p=out/'artifacts/false-claim-v1/output.json';v=read(p)
        v['note']='This is a substituted output, never emitted by the frozen native candidate.';dump(p,v)
        for phase in ['phase2','phase3']:
            p=out/phase/'handoff/runtime-preview.json';preview=read(p);preview[0]['output']=v;dump(p,preview)
    elif case=='h3-unsupported-source-quote':
        for p in root.rglob('*.jsonl'):
            if p.name not in {'reviews.jsonl','store-after.jsonl','store-before.jsonl','store-at-checkpoint.jsonl','store-after-replay.jsonl'}:continue
            values=[json.loads(s) for s in p.read_text().splitlines() if s.strip()]
            for v in values:
                if v.get('record_id')==TARGET:v['statement']='Invented reviewer quote that does not occur in the preserved original source.'
            p.write_text(''.join(json.dumps(v,sort_keys=True)+'\n' for v in values))
    refresh(archive)
def witness(archive,case):
    out=archive/'evidence/workspace/eval-runs/capture-forward'
    native=json.loads((out/'native/false-claim-v1/traces.jsonl').read_text().splitlines()[0])
    if case=='h1-initial-state-mismatch':
        captured=read(out/'artifacts/false-claim-v1/initial-state.json');actual=native['input']['state']
    elif case=='h2-reviewed-output-mismatch':
        captured=read(out/'artifacts/false-claim-v1/output.json');actual=native['output']
    else:
        row=next(json.loads(s) for s in (archive/'evidence/workspace/eval-runs/capture-existing/reviews.jsonl').read_text().splitlines() if json.loads(s).get('record_id')==TARGET)
        captured=row['statement'];actual=(out/'source/FORWARD_TASK.md').read_text()
    return {'captured':captured,'actual_native_or_source':actual,'mismatch':captured!=actual,'source_quote_absent':captured not in actual if isinstance(actual,str) else None}
def main():
    results=[]
    # Baseline receipts and exact protected program identities are preserved.
    for case in ['baseline','h1-initial-state-mismatch','h2-reviewed-output-mismatch','h3-unsupported-source-quote']:
        archive=SOURCE if case=='baseline' else BASE/case
        if case!='baseline':
            shutil.copytree(SOURCE,archive);mutate(archive,case)
        run=subprocess.run([sys.executable,str(archive/'verify_archive.py')],capture_output=True,text=True)
        (BASE/(case+'.stdout.txt')).write_text(run.stdout);(BASE/(case+'.stderr.txt')).write_text(run.stderr)
        result={'case':case,'returncode':run.returncode,'verifier_unchanged':sha(archive/'verify_archive.py')==sha(SOURCE/'verify_archive.py'),'native_trace_unchanged':sha(archive/'evidence/workspace/eval-runs/capture-forward/native/false-claim-v1/traces.jsonl')==sha(SOURCE/'evidence/workspace/eval-runs/capture-forward/native/false-claim-v1/traces.jsonl')}
        if case!='baseline':result['witness']=witness(archive,case)
        results.append(result)
    dump(BASE/'outcomes.json',results)
    dump(BASE/'versions.json',{'verifier_sha256':sha(SOURCE/'verify_archive.py'),'phase2_adapter_sha256':sha(SOURCE/'evidence/workspace/eval-runs/capture-forward/phase2/capture_adapter.py'),'final_driver_sha256':sha(SOURCE/'evidence/workspace/eval-runs/capture-forward/final/finish_phases.py'),'capture_guide_sha256':sha(BASE/'playground/.agents/skills/expert-mode/references/calibration-capture.md'),'native_executions':2,'provider_calls':0,'network_calls':0,'hypotheses_executed':3})
    print(json.dumps([{k:v for k,v in r.items() if k!='witness'} for r in results],indent=2))
if __name__=='__main__':main()
