"""Replay three captured-evidence faults; no candidate execution or model calls."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
ARCHIVE=HERE.parent

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();out=args.out.resolve()
    out.mkdir(parents=True,exist_ok=False)
    spec=importlib.util.spec_from_file_location('captured_probe',HERE/'attacker_replay.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    results=[]
    for case in ['baseline','h1-initial-state-mismatch','h2-reviewed-output-mismatch','h3-unsupported-source-quote']:
        destination=out/case;destination.mkdir()
        shutil.copytree(ARCHIVE/'evidence',destination/'evidence')
        if case!='baseline':module.mutate(destination,case)
        traces=destination/'evidence/workspace/eval-runs/capture-forward/native/false-claim-v1/traces.jsonl'
        original=ARCHIVE/'evidence/workspace/eval-runs/capture-forward/native/false-claim-v1/traces.jsonl'
        assert traces.read_bytes()==original.read_bytes()
        for version,checker in [('before',HERE/'original_verifier.py'),('after',ARCHIVE/'verify_archive.py')]:
            target=destination/'verify_archive.py';shutil.copyfile(checker,target)
            run=subprocess.run([sys.executable,str(target)],capture_output=True,text=True)
            (destination/(version+'.stdout.txt')).write_text(run.stdout)
            (destination/(version+'.stderr.txt')).write_text(run.stderr)
            expected=0 if version=='before' or case=='baseline' else 1
            results.append({'case':case,'checker':version,'exit':run.returncode,'expected_exit':expected,'matches':run.returncode==expected,'checker_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'native_trace_unchanged':True})
    summary={'results':results,'all_expected':all(r['matches'] for r in results),'native_executions':0,'model_calls':0,'scope':'operator corruption resilience; no native candidate write-access claim'}
    (out/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    if not summary['all_expected']:raise SystemExit(1)
if __name__=='__main__':main()
